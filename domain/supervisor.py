# -*- coding: utf8 -*-

from xmlrpc.client import ServerProxy


class SupervisorProxy:

    def __init__(self, proxy_url: str = 'http://user:123@localhost:9001/RPC2'):
        self.supervisor = ServerProxy(proxy_url).supervisor

    def get_process_info(self, name: str) -> dict:
        return self.supervisor.getProcessInfo(name)

    def get_all_process_info(self) -> list:
        return self.supervisor.getAllProcessInfo()

    def get_all_config_info(self):
        return self.supervisor.getAllConfigInfo()

    def start_process(self, name: str, wait=True):
        return self.supervisor.startProcess(name, wait=wait)

    def start_all_processes(self, wait=True):
        return self.supervisor.startAllProcesses(wait=wait)

    def start_process_group(self, name, wait=True):
        return self.supervisor.startProcessGroup(name, wait=wait)

    def stop_process(self, name: str, wait=True):
        return self.supervisor.stopProcess(name, wait=wait)

    def stop_all_processes(self, wait=True):
        return self.supervisor.stopAllProcesses(wait=wait)

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


if __name__ == '__main__':
    from pprint import pprint
    supervisor = SupervisorProxy("http://user:123@localhost:9001/RPC2")

    pprint(supervisor.get_all_process_info())
    # supervisor.stop_process('coinex_wallet')
    # pprint(supervisor.get_all_process_info())
    print(supervisor.read_process_stdout_log('wallet_manager', 5000, 2000))
