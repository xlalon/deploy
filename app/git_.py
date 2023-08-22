# -*- coding: utf8 -*-

from git import Repo, Commit, Head
from typing import Iterable

from .util import dt_to_str


class GitRepo:

    def __init__(self, repo_path: str):
        self.git_proxy = GitProxy(repo_path)

    def pull(self, remote_name: str = 'origin'):
        self.git_proxy.pull(remote_name)

    def fetch(self, remote_name: str = 'origin'):
        self.git_proxy.fetch(remote_name)

    def is_dirty(self) -> bool:
        return self.git_proxy.is_dirty()

    def checkout_branch(self, branch_or_commit_or_tag: str):
        return self.git_proxy.checkout(branch_or_commit_or_tag)

    def checkout_commit(self, commit: str):
        return self.git_proxy.reset(commit)

    def active_branch(self):
        branch = self.git_proxy.active_branch()
        return self.commit_info(branch.commit)

    def remote_commits(self,
                       branch: str = 'origin',
                       max_count: int = 10) -> list:
        result = [
            self.commit_info(commit)
            for commit in self.git_proxy.remote_commits(branch, max_count)
        ]
        return result

    @staticmethod
    def commit_info(commit: Commit) -> dict:
        hexsha, name = commit.name_rev.split(' ')
        return {
            'name': name,
            'committed_datetime': dt_to_str(commit.committed_datetime),
            'message': commit.message.rstrip('\n'),
            'hexsha': hexsha[:8],
        }


class GitProxy:

    def __init__(self, repo_path: str):
        self.repo = Repo(repo_path)

    def pull(self, remote_name: str):
        self.repo.remote(remote_name).pull()

    def fetch(self, remote_name: str):
        self.repo.remote(remote_name).fetch()

    def active_branch(self) -> Head:
        return self.repo.active_branch

    def is_dirty(self):
        return self.repo.is_dirty()

    def remote_commits(self, branch: str, max_count: int) -> Iterable[Commit]:
        head_commit = self.repo.remote(branch).refs.HEAD.commit
        yield head_commit
        yield from head_commit.iter_parents(max_count=max_count - 1)

    def checkout(self, branch: str):
        return self.repo.git.checkout(branch)

    def reset(self, commit: str, typ: str = 'hard'):
        return self.repo.git.reset(f'--{typ}', commit)
