import gitutil
import os

repo_url = 'git@github.com:LyndonChin/PyInfer.git'
workspace = os.getcwd()
file_path = os.path.join(workspace, 'gitutil.py')
project_path = '/Users/rufi/github/liangfeizc/AndroidFlowLayout'

print('commit test')
print(gitutil.get_commit(file_path))

print('project_name test')
print(gitutil.get_project_name(repo_url))

print('get_repo_and_branch test')
print('#'.join(map(str, gitutil.get_repo_and_branch(file_path))))

print('update_source test')
print(gitutil.update_source(project_path))

print('clone source')
os.chdir('/Users/rufi/Downloads')
print(gitutil.clone_source('git@github.com:LyndonChin/AndroidFlowLayout.git', 'master'))
