import os
import re
import subprocess


def get_commit(file_path):
    cwd = os.getcwd()
    os.chdir(os.path.dirname(file_path))
    commit = subprocess.check_output(['git', 'log', '--follow', '-1', file_path]).split()[1]
    os.chdir(cwd)
    return commit


def get_project_name(repo_url):
    return re.search(r'([^/]+)(?=\.git)', repo_url).group(0)


def get_repo_and_branch(file_path):
    cwd = os.getcwd()

    if os.path.isfile(file_path):
        os.chdir(os.path.dirname(file_path))
    elif os.path.isdir(file_path):
        os.chdir(file_path)
    else:
        raise Exception()

    repo = subprocess.check_output(['git', 'remote', '-v']).split()[1]
    branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).strip()

    os.chdir(cwd)

    return repo, branch


def update_source(project_path):
    if not os.path.isdir(project_path):
        raise Exception()
    cwd = os.getcwd()

    os.chdir(project_path)
    subprocess.check_output(['git', 'reset', '--hard'])
    subprocess.check_output(['git', 'pull'])

    os.chdir(cwd)


def clone_source(repo, branch):
    print(subprocess.check_output(['git', 'clone', '--single-branch', '-b', branch, repo]))
