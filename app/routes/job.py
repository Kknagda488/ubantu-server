from app import app, db
from flask import jsonify, request,session
from rq import Queue
from worker import conn

from app.util.web_request import get_file_content_from_url,create_directory_structure
from app.util.github_util import add_file_to_repo,get_timestamp
from app.util.llm import make_llm_call_langchain
from app.models.llm_job import LLMJob
from app.models.selected_file import SelectedFile
from rq.job import Job
from rq.registry import FinishedJobRegistry,FailedJobRegistry, StartedJobRegistry


q = Queue(connection=conn)

@app.route('/create_job', methods=['POST'])
def create_job():
    model_name = request.form['model_name']
    framework = request.form['framework']

    repo_link = session['repo_link']
    branch_name = session['branch_name']
    user_name = session['user_name']
    repo_name = session['repo_name']
    selected_data = session['selected_data']

    app.logger.info("{}{}{}{}{}{}{}".format(model_name,framework,repo_link,branch_name,user_name,repo_name,selected_data))
    if repo_link and branch_name and user_name and repo_name and model_name and framework:
        #creare directory structure
        directory_structure = create_directory_structure(user_name,repo_name,branch_name)
        #create object
        new_job = LLMJob(redis_id=None,user_id=1,repo_name=repo_name,
                         repo_user_name=user_name,branch_name=branch_name,directory_structure=directory_structure
                         ,model_name=model_name,framework=framework)
        db.session.add(new_job)
        db.session.commit()
        insert_id = new_job.id


        #start long running redis job
        redis_job = q.enqueue_call(
            func=run_llm_job, args=(insert_id,selected_data,repo_name,user_name,branch_name,
                directory_structure,model_name,framework), result_ttl=5000
        )

        #update the redis id in the db
        redis_id = redis_job.get_id()
        new_job1 = LLMJob.query.filter_by(id=insert_id).first()
        new_job1.redis_id = redis_id
        db.session.commit()
        return jsonify({'message': f"Started Job with the ID = {redis_id}"})
    else:
        return jsonify({'message': 'error.'})
    

@app.route("/job", methods=['GET'])
def get_all_jobs():
    running_registry = StartedJobRegistry('default', connection=conn)
    success_registry = FinishedJobRegistry('default', connection=conn)
    failure_registry = FailedJobRegistry('default', connection=conn)

    return jsonify({"running": f"jobs: {running_registry.get_job_ids()}",
                    "sucesss": f"jobs: {success_registry.get_job_ids()}",
                    "failure": f"jobs: {failure_registry.get_job_ids()}"})
    
@app.route("/job/<job_key>", methods=['GET'])
def get_results(job_key):

    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        return jsonify({'message': 'success!!','result':job.result, 'id': job.get_id(), 'status':job.get_status})
    else:
       return jsonify({'message': 'running!!'})
    

def run_llm_job(job_id,selected_data,repo_name,repo_user_name,branch_name,
                directory_structure,model_name,framework):
     testcase_path = f"llm_testcase_{get_timestamp()}/"
     testcase_branch = "llm_testcase"
     counter=1
     for data in selected_data:
            result = None
            file_content = get_file_content_from_url(data['url'])
            if file_content:
                if framework == 'PYTHON':
                    p= '#root/'+data['path'] + '\n'
                elif framework == 'REACT':
                    p= '//root/'+data['path'] + '\n'
                try:
                    result = make_llm_call_langchain(p+file_content,framework,directory_structure,model_name)
                except Exception as e:
                    result = None
                    app.logger.error(e)


            if result:                 
                sf = SelectedFile(job_id=job_id,sha=None,path=data['path'],
                                    size=data['size'],download_url=data['url'],status='PASS',result=result)
            else:
                sf = SelectedFile(job_id=job_id,sha=None,path=data['path'],
                                    size=data['size'],download_url=data['url'],status='FAIL',result=None)
            with app.app_context():
                db.session.add(sf)
                db.session.commit()

            if result:
                #push file to github
                add_file_to_repo(user_name=repo_user_name,repo_name=repo_name,testcase_branch=testcase_branch,
                        original_branch=branch_name,file_name=f"testcase{counter}.txt",file_content=result,testcase_path=testcase_path,framework=framework)
            #push file to github
            # except Exception as e:
            #     app.logger.info(f"failed to add file={data['path']} to github")
            #     app.logger.error(e)

            counter+=1