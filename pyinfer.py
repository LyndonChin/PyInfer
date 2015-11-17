#!/usr/bin/python

"""
    Pyinfer
    ~~~~~~~

    An infer wrapper to produce well-formatted analyzed result

    :copyright: (c) 2015 liangfeizc.com
    :license: MIT, see LICENSE for more details

"""

import argparse
import csv
import json
import uuid
import os
import re
from subprocess import check_output

import requests


class Infer:
    def __init__(self, repo, branch):
        self.repo = repo
        self.branch = branch
        self.report_path = 'infer-out/report.csv'
        self.server = 'http://127.0.0.1:8000/staticscan/issues/'
        self.workspace = ''
        self.scan_id = ''

    def run_infer(self, workspace=os.getcwd()):
        print('run infer...')
        self.workspace = workspace
        self.scan_id = self.generate_scan_id()
        project = self.clone_source()
        os.chdir(os.path.join(self.workspace, project))
        check_output(['./gradlew', 'clean'])
        check_output(['infer', '--', './gradlew', 'build'])
        self.upload_report()

    def clone_source(self):
        print('clone source...')
        os.chdir(self.workspace)
        project = re.search(r'([^/]+)(?=\.git)', self.repo).group(0)
        if os.path.exists(project):
            # shutil.rmtree(project)
            os.chdir(project)
            check_output(['git', 'reset', '--hard'])
            check_output(['git', 'pull'])
        else:
            check_output(['git', 'clone', '--single-branch', '-b', self.branch, self.repo])
        return project

    def upload_report(self):
        print('upload report...')
        report = self.parse_result()
        if not report:
            return
        data = {'data': json.dumps(report)}
        ret = ''
        try:
            r = requests.post(self.server, data=data)
            ret = r.text
        except Exception as e:
            print(e)
        return ret

    def parse_result(self):
        print('parse result...')
        with open(self.report_path, 'rU') as report:
            reader = csv.DictReader(report)
            report_list = []
            for row in reader:
                report_list.append(
                    {
                        'error': row['type'] + ":" + row['qualifier'],
                        'source': row['procedure_id'],
                        'scan_id': self.scan_id,
                        'line_no': row['line'],
                        'file_name': row['file'],
                        'repo': self.repo,
                        'branch': self.branch
                    })
            return report_list

    def generate_scan_id(self):
        return str(uuid.uuid1())


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--repo', help='Your repository')
    parser.add_argument('-b', '--branch', default='master', help='Branch of the repository')
    parser.add_argument('-w', '--workspace', default=os.getcwd(), help='Workspace to run infer')
    args = parser.parse_args()
    return args.repo, args.branch, args.workspace


def main():
    repo, branch, workspace = parse_args()
    infer = Infer(repo, branch)
    infer.run_infer(workspace)

if __name__ == '__main__':
    main()

