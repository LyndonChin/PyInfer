import gitutil
import os

workspace = os.getcwd()
file_path = os.path.join(workspace, 'gitutil.py')

print(gitutil.get_commit(file_path))
