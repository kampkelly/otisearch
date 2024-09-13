import subprocess
import os
from datetime import datetime
from typing import Any, Dict
from src.database.redis import redis_setup
from dotenv import load_dotenv
import threading

load_dotenv()

python_env_path = os.getenv('PYTHON_ENV_PATH', "")
default_path = os.getenv('DEFAULT_PATH', "")
export_paths = os.getenv('EXPORT_PATHS', "")


class PGSync:
    def __init__(self, env_vars: Dict[str, Any], config_path: str, es_index: str):
        self.processes = {}
        self.es_index = es_index
        self.config_path = config_path
        self.python_env_path = python_env_path
        self.env = {k: str(v) for k, v in env_vars.items()}
        self.env['PATH'] = default_path
        self.redis = redis_setup(host="localhost", port="6379")

    def set_env_vars(self, env_vars):
        """
        Set environment variables for pgsync.
        :param env_vars: dict of environment variables to set
        """
        self.env.update({k: str(v) for k, v in env_vars.items()})

    def _run_in_env(self, command: str, run_mode=False):
        bash_command = f"""
        source {self.python_env_path}/bin/activate
        {export_paths}
        {command}
        """
        try:
            if run_mode:
                # add stdout=subprocess.PIPE, stderr=subprocess.PIPE
                return subprocess.run(bash_command, shell=True, env=self.env, executable='/bin/bash', timeout=10)
            return subprocess.Popen(bash_command, shell=True, env=self.env, executable='/bin/bash')
        except subprocess.TimeoutExpired:
            print("Command timed out.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def start_sync(self):
        bootstrap_command = f'bootstrap --config {self.config_path}'
        self._run_in_env(bootstrap_command, True)

        pgsync_command = f'pgsync --config {self.config_path} -d'
        process = self._run_in_env(pgsync_command)

        self.redis.hmset(f'process:{self.es_index}', {
            'pid': process.pid,
            'status': 'running',
            'start_time': datetime.now().isoformat(),
            'stop_time': ''
        })

        if os.path.exists(self.config_path):
            threading.Timer(20, os.remove, [self.config_path]).start()

        print(f"Started {self.es_index} with PID: {process.pid}")

    def stop(self, client_name: str):
        process_info = self.redis.hgetall(f'process:{client_name}')
        process_info = {k.decode('utf-8'): v.decode('utf-8') for k, v in process_info.items()}

        if process_info and process_info['status'] == 'running':
            pid = int(process_info['pid'])
            try:
                subprocess.run(f'kill {pid}', shell=True, check=True)
                self.redis.hmset(f'process:{client_name}', {
                    'status': 'stopped',
                    'stop_time': datetime.now().isoformat()
                })
                print(f"Stopped {client_name} (PID: {pid}).")
            except subprocess.CalledProcessError:
                print(f"Failed to stop {client_name} (PID: {pid}).")
        else:
            print(f"No running process found for {client_name}.")

    def list_processes(self, status: str = None):
        for key in self.redis.scan_iter("process:*"):
            process = self.redis.hgetall(key)
            process = {k.decode('utf-8'): v.decode('utf-8') for k, v in process.items()}
            decoded_key = key.decode('utf-8')
            if status is None or process["status"] == status:
                print(f"Client: {decoded_key.split(':')[1]}, PID: {process['pid']}, Status: {process['status']}, "
                      f"Start Time: {process['start_time']}, Stop Time: {process['stop_time']}")

    def clean_up(self):
        for key in self.redis.scan_iter("process:*"):
            if self.redis.hget(key, 'status') == 'stopped':
                self.redis.delete(key)
        print("Cleaned up stopped processes from Redis.")
