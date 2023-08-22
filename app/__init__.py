# -*- coding: utf8 -*-

from flask import Flask

from .api import AppApi
from .config import init_config
from .git_api import (
    git_bp,
    GithubWebhook,
    RemoteCommits,
    ActiveBranch,
    CheckoutCommit
)
from .git_admin_api import (
    admin_git_bp,
    GithubWebhook as AdminGithubWebhook,
    RemoteCommits as AdminRemoteCommits,
    ActiveBranch as AdminActiveBranch,
    CheckoutCommit as AdminCheckoutCommit
)
from .supervisor_api import (
    supervisor_bp,
    ProcessInfo,
    AllProcessInfo,
    StartProcess,
    StartAllProcess,
    StopProcess,
    StopAllProcess,
    RestartProcess,
    RestartAllProcess,
    ProcessStdoutLog,
    ProcessStderrLog
)


def create_app():

    app = Flask(__name__)

    init_config(app)

    register_bp(app)

    return app


def register_bp(app):
    if app.config.get('APP_ROLE') == 'admin':
        register_admin_git(app)
        register_supervisor(app)
    else:
        register_git(app)


def register_admin_git(app):
    admin_git_api = AppApi(admin_git_bp, prefix='/v1/admin-git')

    admin_git_api.add_resource(AdminGithubWebhook, '/<repo>/github-webhook')
    admin_git_api.add_resource(AdminRemoteCommits, '/<repo>/remote-commits')
    admin_git_api.add_resource(AdminActiveBranch, '/<repo>/active-branch')
    admin_git_api.add_resource(AdminCheckoutCommit, '/<repo>/checkout-commit')

    app.register_blueprint(admin_git_bp)


def register_git(app):
    agent_git_api = AppApi(git_bp, prefix='/v1/git')

    agent_git_api.add_resource(GithubWebhook, '/<repo>/github-webhook')
    agent_git_api.add_resource(RemoteCommits, '/<repo>/remote-commits')
    agent_git_api.add_resource(ActiveBranch, '/<repo>/active-branch')
    agent_git_api.add_resource(CheckoutCommit, '/<repo>/checkout-commit')

    app.register_blueprint(git_bp)


def register_supervisor(app):
    sp_api = AppApi(supervisor_bp, prefix='/v1/supervisor')

    sp_api.add_resource(ProcessInfo, '/process-info/<name>')
    sp_api.add_resource(AllProcessInfo, '/process-info')
    sp_api.add_resource(StartProcess, '/start-process')
    sp_api.add_resource(StartAllProcess, '/start-all-process')
    sp_api.add_resource(StopProcess, '/stop-process')
    sp_api.add_resource(StopAllProcess, '/stop-all-process')
    sp_api.add_resource(RestartProcess, '/restart-process')
    sp_api.add_resource(RestartAllProcess, '/restart-all-process')
    sp_api.add_resource(ProcessStdoutLog, '/process-stdout-log/<name>')
    sp_api.add_resource(ProcessStderrLog, '/process-stderr-log/<name>')

    app.register_blueprint(supervisor_bp)
