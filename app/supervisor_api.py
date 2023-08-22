# -*- coding: utf8 -*-

from flask import current_app, Blueprint

from .exception import InvalidArgument
from .util import get_url_hostname
from .api import AppResource
from .supervisor_ import Supervisor


supervisor_bp = Blueprint('supervisor_bp', __name__)


class SupervisorResource(AppResource):

    def __init__(self):
        self._supervisor_urls = current_app.config['SUPERVISOR_URLS']
        self._Supervisor = Supervisor

    def get_arg_hosts(self):
        hosts = self.get_argument('hosts', strict=False, default='')
        if hosts:
            hosts = hosts.split(',')
        self.validate_hosts(hosts)
        return hosts or self._get_sp_hosts()

    def validate_hosts(self, hosts: list):
        if not hosts:
            return True
        all_hosts = self._get_sp_hosts()
        for host in hosts:
            if host not in all_hosts:
                raise InvalidArgument(f'{host}')
        return True

    def supervisor_hosts_info(self) -> dict:
        return {get_url_hostname(url): url for url in self._get_sp_urls()}

    def _get_sp_hosts(self) -> list:
        return [get_url_hostname(url) for url in self._get_sp_urls()]

    def _get_sp_urls(self) -> list:
        return self._supervisor_urls.split(',')


class ProcessInfo(SupervisorResource):
    def get(self, name: str):
        result = []
        hosts = self.get_arg_hosts()
        hosts_info = self.supervisor_hosts_info()
        for host in hosts:
            sp = self._Supervisor(hosts_info[host])
            info = sp.get_process_info(name)
            result.append({'host': host, 'info': info})

        return self.render_json(result)


class AllProcessInfo(SupervisorResource):
    def get(self):
        result = []
        hosts = self.get_arg_hosts()
        hosts_info = self.supervisor_hosts_info()
        for host in hosts:
            sp = self._Supervisor(hosts_info[host])
            info = sp.get_all_process_info()
            result.append({'host': host, 'info': info})

        return self.render_json(result)


class StartProcess(SupervisorResource):
    def post(self):
        result = []
        name = self.get_argument('name')
        hosts = self.get_arg_hosts()
        hosts_info = self.supervisor_hosts_info()
        for host in hosts:
            sp = self._Supervisor(hosts_info[host])
            info = sp.start_process(name)
            result.append({'host': host, 'info': info})

        return self.render_json(result)


class StartAllProcess(SupervisorResource):
    def post(self):
        result = []
        hosts = self.get_arg_hosts()
        hosts_info = self.supervisor_hosts_info()
        for host in hosts:
            sp = self._Supervisor(hosts_info[host])
            info = sp.start_all_processes()
            result.append({'host': host, 'info': info})

        return self.render_json(result)


class StopProcess(SupervisorResource):
    def post(self):
        result = []
        name = self.get_argument('name')
        hosts = self.get_arg_hosts()
        hosts_info = self.supervisor_hosts_info()
        for host in hosts:
            sp = self._Supervisor(hosts_info[host])
            info = sp.stop_process(name)
            result.append({'host': host, 'info': info})

        return self.render_json(result)


class StopAllProcess(SupervisorResource):
    def post(self):
        result = []
        hosts = self.get_arg_hosts()
        hosts_info = self.supervisor_hosts_info()
        for host in hosts:
            sp = self._Supervisor(hosts_info[host])
            info = sp.stop_all_processes()
            result.append({'host': host, 'info': info})

        return self.render_json(result)


class RestartProcess(SupervisorResource):
    def post(self):
        result = []
        name = self.get_argument('name')
        hosts = self.get_arg_hosts()
        hosts_info = self.supervisor_hosts_info()
        for host in hosts:
            sp = self._Supervisor(hosts_info[host])
            info = sp.restart_process(name)
            result.append({'host': host, 'info': info})

        return self.render_json(result)


class RestartAllProcess(SupervisorResource):
    def post(self):
        result = []
        hosts = self.get_arg_hosts()
        hosts_info = self.supervisor_hosts_info()
        for host in hosts:
            sp = self._Supervisor(hosts_info[host])
            info = sp.restart_all_processes()
            result.append({'host': host, 'info': info})

        return self.render_json(result)


class ProcessStdoutLog(SupervisorResource):
    def get(self, name: str):
        result = []
        offset = self.get_argument('offset', type_=int, default=0)
        length = self.get_argument('length', type_=int, default=2048)
        hosts = self.get_arg_hosts()
        hosts_info = self.supervisor_hosts_info()
        for host in hosts:
            sp = self._Supervisor(hosts_info[host])
            info = sp.tail_process_stdout_log(name, offset, length)
            result.append({'host': host, 'info': info})

        return self.render_json(result)


class ProcessStderrLog(SupervisorResource):
    def get(self, name: str):
        result = []
        offset = self.get_argument('offset', type_=int, default=0)
        length = self.get_argument('length', type_=int, default=2048)
        hosts = self.get_arg_hosts()
        hosts_info = self.supervisor_hosts_info()
        for host in hosts:
            sp = self._Supervisor(hosts_info[host])
            info = sp.tail_process_stderr_log(name, offset, length)
            result.append({'host': host, 'info': info})

        return self.render_json(result)
