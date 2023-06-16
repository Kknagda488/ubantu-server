from app import db

class LLMJob(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    redis_id = db.Column(db.String())
    user_id = db.Column(db.Integer)
    repo_name = db.Column(db.String())
    repo_user_name = db.Column(db.String())
    branch_name = db.Column(db.String())
    directory_structure = db.Column(db.String())
    model_name = db.Column(db.String())
    framework = db.Column(db.String())


    def __init__(self,redis_id, user_id, repo_name, repo_user_name,branch_name ,directory_structure ,model_name ,framework):
        self.redis_id = redis_id
        self.user_id = user_id
        self.repo_name = repo_name
        self.repo_user_name = repo_user_name
        self.branch_name = branch_name
        self.directory_structure = directory_structure
        self.model_name = model_name
        self.framework = framework

    def __repr__(self):
        return f"<Job {self.redis_id}, {self.repo_name} >"