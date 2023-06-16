import requests
from github import Github
import os
import datetime 

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
g = Github(GITHUB_TOKEN)
def check_if_branch_exist(repo,branch_name):
    branch_list = list(repo.get_branches())
    branch_list = [x.name for x in branch_list]
    if branch_name in branch_list:
        return True
    else:
        return False

def create_branch(repo,source_branch,target_branch):
    sb = repo.get_branch(source_branch)
    repo.create_git_ref(ref='refs/heads/' + target_branch, sha=sb.commit.sha)

def get_timestamp():
    now = datetime.datetime.now()
    return now.strftime('%Y_%m_%d_%H_%M_%S')


def add_file_to_repo(user_name,repo_name,testcase_branch,original_branch,file_name,file_content,testcase_path,framework):
    if framework == 'PYTHON':
        file_name = file_name.replace('.txt','_test.py')
    elif framework == 'REACT':
        file_name = file_name.replace('.txt','.test.jsx')

    repo = g.get_repo(f"{user_name}/{repo_name}")
    if not check_if_branch_exist(repo,testcase_branch):
        create_branch(repo,original_branch,testcase_branch)

    repo = g.get_repo(f"{user_name}/{repo_name}")
    res = repo.create_file(testcase_path+file_name, "adding llm testcase", file_content, branch=testcase_branch)
    return res

    



