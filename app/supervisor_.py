# -*- coding: utf8 -*-

from xmlrpc.client import ServerProxy

from .exception import InvalidArgument
from .util import ts_to_str


class Supervisor:

    def __init__(self, host_url: str):
        self.proxy = SupervisorProxy(host_url)

    def get_process_info(self, name: str) -> dict:
        self.validate_name(name)
        return self.process_info(self.proxy.get_process_info(name))

    def validate_name(self, name: str):
        if name not in self.get_all_process_name():
            raise InvalidArgument(name)

    def validate_group(self, name: str):
        if name not in self.get_all_group_name():
            raise InvalidArgument(name)

    def get_all_process_name(self) -> set:
        processes = self.get_all_process_info()
        return {p['name'] for p in processes}

    def get_all_group_name(self) -> set:
        processes = self.get_all_process_info()
        return {p['group'] for p in processes}

    def get_all_process_info(self) -> list:
        processes = self.proxy.get_all_process_info()
        return [self.process_info(p) for p in processes]

    def get_all_config_info(self):
        return self.proxy.get_all_config_info()

    def start_process(self, name: str):
        self.validate_name(name)
        process = self.get_process_info(name)
        if process['statename'] != 'RUNNING':
            self.proxy.start_process(name)
        return

    def start_all_processes(self):
        return self.proxy.start_all_processes()

    def start_process_group(self, name):
        self.validate_group(name)
        return self.proxy.start_process_group(name)

    def stop_process(self, name: str):
        self.validate_name(name)
        process = self.get_process_info(name)
        if process['statename'] == 'RUNNING':
            self.proxy.stop_process(name)
        return

    def stop_all_processes(self):
        return self.proxy.stop_all_processes()

    def restart_process(self, name: str):
        self.validate_name(name)
        self.stop_process(name)
        self.start_process(name)
        return

    def restart_all_processes(self):
        self.stop_all_processes()
        self.start_all_processes()
        return

    def signal_process(self, name, signal):
        self.validate_name(name)
        return self.proxy.signal_process(name, signal)

    def signal_process_group(self, name: str, signal: str):
        self.validate_group(name)
        return self.proxy.signal_process_group(name, signal)

    def signal_all_processes(self, signal: str):
        return self.proxy.signal_all_processes(signal)

    def reload_config(self):
        return self.proxy.reload_config()

    def read_process_stdout_log(self, name, offset, length):
        self.validate_name(name)
        return self.proxy.read_process_stdout_log(name, offset, length)

    def read_process_stderr_log(self, name, offset, length):
        self.validate_name(name)
        return self.proxy.read_process_stderr_log(name, offset, length)

    def tail_process_stdout_log(self, name, offset, length):
        self.validate_name(name)
        return self.proxy.tail_process_stdout_log(name, offset, length)

    def tail_process_stderr_log(self, name, offset, length):
        self.validate_name(name)
        return self.proxy.tail_process_stderr_log(name, offset, length)

    @staticmethod
    def process_info(info: dict) -> dict:
        return {
            'name': info['name'],
            'group': info['group'],
            'start': ts_to_str(info['start']),
            'stop': ts_to_str(info['stop']),
            'exitstatus': info['exitstatus'],
            'statename': info['statename']
        }


class SupervisorProxy:

    def __init__(self, proxy_url: str):
        self.supervisor = ServerProxy(proxy_url).supervisor

    def get_process_info(self, name: str) -> dict:
        return self.supervisor.getProcessInfo(name)

    def get_all_process_info(self) -> list:
        return self.supervisor.getAllProcessInfo()

    def get_all_config_info(self):
        return self.supervisor.getAllConfigInfo()

    def start_process(self, name: str):
        return self.supervisor.startProcess(name)

    def start_all_processes(self):
        return self.supervisor.startAllProcesses()

    def start_process_group(self, name):
        return self.supervisor.startProcessGroup(name)

    def stop_process(self, name: str):
        return self.supervisor.stopProcess(name)

    def stop_all_processes(self):
        return self.supervisor.stopAllProcesses()

    def signal_process(self, name, signal):
        return self.supervisor.signalProcess(name, signal)

    def signal_process_group(self, name: str, signal: str):
        return self.supervisor.signalProcessGroup(name, signal)

    def signal_all_processes(self, signal: str):
        return self.supervisor.signalAllProcesses(signal)

    def reload_config(self):
        return self.supervisor.reloadConfig()

    def read_process_stdout_log(self, name, offset, length):
        return self.supervisor.readProcessStdoutLog(name, offset, length)

    def read_process_stderr_log(self, name, offset, length):
        return self.supervisor.readProcessStderrLog(name, offset, length)

    def tail_process_stdout_log(self, name, offset, length):
        return self.supervisor.tailProcessStdoutLog(name, offset, length)

    def tail_process_stderr_log(self, name, offset, length):
        return self.supervisor.tailProcessStderrLog(name, offset, length)
