from app import app
from flask import render_template, request, session, jsonify
from app.util.web_request import get_all_repo_files
import json

@app.route('/', methods=['GET', 'POST'])
def get_all_files():
    if request.method == 'POST':
        result = ""
        error = ""
        repo_link = request.form['repo'].strip()
        branch_name = request.form['branch_name'].strip()

        if repo_link:
            try:
                # Extracting reponame and username from input
                path = repo_link.split("github.com/")[1]
                names = path.split("/")
                user_name = names[0].strip()
                repo_name = names[1].strip()
                if not branch_name:
                    branch_name = 'master'

                app.logger.info("yash---" + user_name + repo_name + branch_name)

                # Getting all file names of the repo
                repo_data_list = get_all_repo_files(user_name, repo_name, branch_name)
                result = json.dumps([ob.__dict__ for ob in repo_data_list])
                app.logger.info(result)
                
                #storing in session
                session['repo_link'] = repo_link
                session['branch_name'] = branch_name
                session['user_name'] = user_name
                session['repo_name'] = repo_name
            except Exception as e:
                app.logger.info(e)
                error = "Please enter a valid GitHub repository and branch."
        else:
            error = 'Please fill all the fields.'
        
        return jsonify({'result': result, 'error': error})

    else:
        return render_template('home.html')