import requests
from github import Github
from app.models.repo_info import RepoInfo
import base64
from bigtree import list_to_tree, yield_tree
import os

GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
g = Github(GITHUB_TOKEN)

def get_repo_text(url):
    try:
        url = 'https://api.github.com/repos/hamzaavvan/library-management-system/contents/blob/60c798187a6678623224c72c3ea90fa618b9c657/App/User.py'
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        })
        r = requests.get(url, headers=headers,verify=True)
        if r.status_code == 200:
            return r.text
        else:
            return "Invalid request with the code={}".format(r.status_code)
    except Exception as e:
        return 'Invalid URL.'
    
def get_all_repo_files(user_name,repo_name,branch_name):
        # all_file_names = [] 
        # repo = g.get_repo("{}/{}".format(user_name,repo_name))
        # contents = repo.get_contents("")
        # while contents:
        #     file_content = contents.pop(0)
        #     if file_content.type == "dir":
        #         contents.extend(repo.get_contents(file_content.path))
        #     else:
        #         # r = RepoInfo(path=file_content.path, name=file_content.name, 
        #         #                 content=file_content.content, html_url=file_content.html_url, download_url=file_content.download_url)
        #         all_file_names.append(file_content.path)
        # logging.info(all_file_names)
        # return all_file_names
        
        all_file_names = [] 
        url = f"https:////api.github.com//repos//{user_name}//{repo_name}//git/trees/{branch_name}?recursive=1".format(user_name=user_name, repo_name=repo_name,branch_name=branch_name)
        r = requests.get(url)
        res = r.json()
        for file in res["tree"]:
             r = RepoInfo(file['path'],file['type'],file.get('size',None),file['url'])
             if r.type != 'tree':
                all_file_names.append(r)
        return all_file_names

def get_file_content_from_url(url):
    try:
        req = requests.get(url)
        if req.status_code == requests.codes.ok:
            res = req.json()  # the response is a JSON
            # req is now a dict with keys: name, encoding, url, size ...
            # and content. But it is encoded with base64.
            content = base64.b64decode(res['content']).decode('utf-8')
            return(content)
        else:
            return None
    except Exception as e:
        return None

def create_directory_structure(user_name,repo_name,branch_name):
    path_list_data = get_all_repo_files(user_name,repo_name,branch_name)
    path_list = [s.path for s in path_list_data]

    path_list = ["root/"+s for s in path_list]

    root = list_to_tree(path_list, sep="/")
    res= ''
    for branch, stem, node in yield_tree(root):
        res += f"{branch}{stem}{node.node_name}\n"
    return res


           

