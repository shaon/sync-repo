import os
import re
import subprocess
from subprocess import PIPE

__author__ = 'shaon'


class CommandManager(object):
    def __init__(self, cmd, shell=True):
        self.cmd = cmd
        self.shell = shell

    def execute(self):
        p = subprocess.Popen(self.cmd, shell=self.shell, stdout=PIPE)
        print "Executing: " + self.cmd
        output, error = p.communicate()
        return output


class SyncRepo(object):
    def __init__(self, repo, name):
        self.name = name
        self.github_repo = repo['github']
        self.internal_repo = repo['internal']
        self.saved_path = os.getcwd()

    def run_sync(self, remote_name='upstream'):
        repo_manager = RepoManager(github_repo=self.github_repo, repo_name=self.name)
        repo_manager.get_master_repo()
        repo_manager.add_remote_repository(remote_name, self.internal_repo)
        repo_manager.push_to_remotes(remote_name)
        os.chdir(self.saved_path)


class RepoManager(object):
    def __init__(self,
                 github_repo=None,
                 repo_name=None):
        self.github_repo = github_repo
        self.name = repo_name

        self.all_branches = None
        self.last_commit = None
        self.active_branch = None
        self.inactive_branches = None

    def get_master_repo(self):
        cmd = CommandManager("git clone " + self.github_repo)
        cmd.execute()
        os.chdir(self.name)

        cmd = CommandManager("git rev-parse HEAD")
        self.last_commit = cmd.execute()

        cmd = CommandManager("git branch -a")
        branches = (cmd.execute()).decode('ascii').splitlines()
        self.all_branches = [str(branch).strip() for branch in branches]

        cmd = CommandManager("git rev-parse --abbrev-ref HEAD")
        self.active_branch = (cmd.execute()).decode('ascii').splitlines()[0]

        self.inactive_branches = []
        for branch in self.all_branches:
            m = re.search('origin\/'+self.active_branch, branch)
            n = re.search('\*', branch)
            if not m and not n:
                self.inactive_branches.append(branch.replace('remotes/origin/', ''))

    def push_to_remotes(self, remote_name, push_to_all=True):
        cmd = CommandManager("git push " + remote_name + " " + self.active_branch)
        cmd.execute()

        if push_to_all:
            for ib in self.inactive_branches:
                cmd = CommandManager("git checkout " + ib)
                cmd.execute()
                cmd = CommandManager("git push " + remote_name + " " + ib)
                cmd.execute()

    def add_remote_repository(self, remote_name, remote_url):
        cmd = CommandManager("git remote add " + remote_name + " " + remote_url)
        cmd.execute()