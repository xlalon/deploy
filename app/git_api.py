# -*- coding: utf8 -*-

import hmac
from collections import defaultdict
from flask import current_app, Blueprint, request

from .api import AppResource
from .git_ import GitRepo


git_bp = Blueprint('git_bp', __name__)


class GitResource(AppResource):

    def __init__(self):
        self._local_git_repos = current_app.config['LOCAL_GIT_REPOS']
        self._GitRepo = GitRepo

    def git_repo_dirs(self, repo: str) -> list:
        return self._get_git_repo_info().get(repo, [])

    def _get_git_repo_info(self, ) -> dict:
        result = defaultdict(list)
        git_repos = self._local_git_repos.split(',')
        for repo_info in git_repos:
            repo, repo_dir = repo_info.split(':', maxsplit=1)
            result[repo].append(repo_dir)
        return result


class GithubWebhook(GitResource):
    def post(self, repo):
        result = []

        # signature = request.headers.get('X-Hub-Signature')
        # sha, signature = signature.split('=')
        # secret = str.encode(current_app.config.get('GITHUB_SECRET'))
        # hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()
        # if not hmac.compare_digest(hashhex, signature):
        #     return result

        for repo_dir in self.git_repo_dirs(repo):
            git_repo = self._GitRepo(repo_dir)
            git_repo.fetch()
            info = git_repo.checkout_commit('origin/master')
            result.append({'repo': repo, 'repo_dir': repo_dir, 'info': info})

        return self.render_json(result)


class RemoteCommits(GitResource):
    def get(self, repo):
        result = []
        for repo_dir in self.git_repo_dirs(repo):
            git_repo = self._GitRepo(repo_dir)
            git_repo.fetch()
            info = git_repo.remote_commits()
            result.append({'repo': repo, 'info': info})
            break

        return self.render_json(result)


class ActiveBranch(GitResource):
    def get(self, repo):
        result = []
        for repo_dir in self.git_repo_dirs(repo):
            git_repo = self._GitRepo(repo_dir)
            info = git_repo.active_branch()
            result.append({'repo': repo, 'repo_dir': repo_dir, 'info': info})

        return self.render_json(result)


class CheckoutCommit(GitResource):
    def post(self, repo):
        result = []
        commit = self.get_argument('commit')
        for repo_dir in self.git_repo_dirs(repo):
            git_repo = self._GitRepo(repo_dir)
            info = git_repo.checkout_commit(commit)
            result.append({'repo': repo, 'repo_dir': repo_dir, 'info': info})

        return self.render_json(result)
