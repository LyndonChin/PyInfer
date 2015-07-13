"""
    Pyinfer
    ~~~~~~~

    A infer wrapper to produce well-formatted analyzed result

    :copyright: (c) 2015 liangfeizc
    :license: MIT, see LICENSE for more details

"""

import subprocess
import argparse
import shutil
import re
import os


def parse_args():
    """
    Parse command line arguments
    :return: git repo and project type
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--infer',
                        help='Path to the infer. If not specified it assumes infer is in your path',
                        default='infer')

    parser.add_argument('--repo',
                        help='git repository for the project to be inferred.')

    parser.add_argument('--type',
                        help='Android or iOS',
                        default='Android')

    args = parser.parse_args()

    return args.infer, args.repo, args.type


def run_infer_cmd():
    """
    Run infer command in the shell
    :return:
    """

    infer, project_repo, project_type = parse_args()
    if not project_repo:
        print('You must specify the git repo address')
        return

    project_dir = re.search(r'([^/]+)(?=\.git)', project_repo).group(0)
    if os.path.exists(project_dir):
        print(project_dir + ' exists')
    else:
        # clone git repo to local
        call_result = subprocess.call(['git', 'clone', project_repo])
        if call_result > 0:
            print('failed to clone the repo ' + project_repo)
            return

    # Enter the project directory
    working_dir = os.path.join(os.getcwd(), project_dir)

    # Use gradle to build android project
    if project_type.lower() == 'android':
        p = subprocess.Popen([infer, '--', './gradlew', 'clean', 'build'], cwd=working_dir)
        p.wait()


def main():
    run_infer_cmd()


if __name__ == '__main__':
    main()
