# -*- coding: utf8 -*-

import hmac
from collections import defaultdict
from flask import current_app, Blueprint, request

from .api import AppResource
from .exception import UnrecognizedHost, UnrecognizedRepo
from .util import urljoin, http_get, http_post


admin_git_bp = Blueprint('admin_git_bp', __name__)


class GitAdminResource(AppResource):

    def __init__(self):
        self._git_repos = current_app.config['GIT_REPOS']
        self._agent_port = int(current_app.config.get('AGENT_PORT', 9101))

    def get_repo_agent_hosts(self, repo: str) -> list:
        return self._get_git_repos_info().get(repo, [])

    def _get_git_repos_info(self):
        host_repos = self._get_git_repos()
        result = defaultdict(list)
        for host_repo in host_repos:
            host, repo = host_repo.rsplit('/', maxsplit=1)
            result[repo].append(host)
        return result

    def _get_git_repos(self):
        result = []
        if self._git_repos and isinstance(self._git_repos, str):
            result = self._git_repos.split(',')
        return result

    def agent_post(self, host: str, url: str = '', json_=None):
        full_url = self._get_full_url(host, url)
        return http_post(full_url, json_)

    def agent_get(self, host: str, url: str = '', params=None):
        full_url = self._get_full_url(host, url)
        return http_get(full_url, params)

    def _get_full_url(self, host: str, url: str) -> str:
        return urljoin(self._get_agent_netloc(host), url)

    def _get_agent_netloc(self, host: str) -> str:
        return f'http://{host}:{self._agent_port}'


class GithubWebhook(GitAdminResource):
    def post(self, repo: str):
        result = self.render_json(None)
        # signature = request.headers.get('X-Hub-Signature')
        # sha, signature = signature.split('=')
        # secret = str.encode(current_app.config.get('GITHUB_SECRET'))
        # hashhex = hmac.new(secret, request.data, digestmod='sha1').hexdigest()
        # if not hmac.compare_digest(hashhex, signature):
        #     return result

        for host in self.get_repo_agent_hosts(repo):
            self.agent_post(host, f'/v1/git/{repo}/github-webhook')

        return result


class RemoteCommits(GitAdminResource):
    def post(self, repo: str):
        hosts = self.get_repo_agent_hosts(repo)
        if not hosts:
            raise UnrecognizedRepo(repo)

        return self.agent_get(hosts[0], f'/v1/git/{repo}/remote-commits')


class ActiveBranch(GitAdminResource):
    def post(self, repo: str):
        host = self.get_argument('host')
        hosts = self.get_repo_agent_hosts(repo)
        if host not in hosts:
            raise UnrecognizedHost(host)

        return self.agent_get(host, f'/v1/git/{repo}/active-branch')


class CheckoutCommit(GitAdminResource):
    def post(self, repo: str):
        host = self.get_argument('host')
        commit = self.get_argument('commit')
        hosts = self.get_repo_agent_hosts(repo)
        if host not in hosts:
            raise UnrecognizedHost(host)

        return self.agent_post(host, f'/v1/git/{repo}/checkout-commit',
                               json_={'commit': commit})
