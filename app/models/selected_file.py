from app import db

class SelectedFile(db.Model):
    __tablename__ = 'selected_files'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer)
    sha = db.Column(db.String())
    path = db.Column(db.String())
    size = db.Column(db.Integer)
    download_url = db.Column(db.String())
    status = db.Column(db.String())
    result = db.Column(db.String())

    def __init__(self, job_id, sha, path, size, download_url, status, result):
        self.job_id = job_id
        self.sha = sha
        self.path = path
        self.size = size
        self.download_url = download_url
        self.status = status
        self.result = result

    def __repr__(self):
        return f"<File {self.path}>"  