import time
import subprocess
import socket
import logging
from pymetasploit3.msfrpc import MsfRpcClient

logger = logging.getLogger(__name__)

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 55553
DEFAULT_RPC_USER = 'msf'
DEFAULT_RPC_PASS = 'msf'
DEFAULT_DOCKER_IMAGE = 'metasploitframework/metasploit-framework'
DEFAULT_CONTAINER_NAME = 'msf-ci-instance'

def _port_open(host, port, timeout=0.5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((host, port))
            return True
        except Exception:
            return False


class MetasploitManager:
    \"\"\"Manage a Metasploit RPC connection, starting a Docker container if needed.\"\"\"

    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT, user=DEFAULT_RPC_USER, password=DEFAULT_RPC_PASS,
                 auto_start_container=True, container_name=DEFAULT_CONTAINER_NAME, image=DEFAULT_DOCKER_IMAGE,
                 connect_timeout=30):
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.container_name = container_name
        self.image = image
        self.client = None
        self._container_started = False
        self.auto_start_container = auto_start_container
        self.connect_timeout = connect_timeout

        self.connect_or_start(timeout=self.connect_timeout)

    def connect_or_start(self, timeout=30):
        if self._try_connect():
            return
        if not self.auto_start_container:
            raise RuntimeError('No Metasploit RPC available and auto_start_container is False.')
        self._start_msf_container()
        start = time.time()
        while time.time() - start < timeout:
            if self._try_connect():
                return
            time.sleep(0.5)
        raise RuntimeError('Could not connect to msfrpcd after starting container')

    def _try_connect(self):
        if not _port_open(self.host, self.port):
            return False
        try:
            self.client = MsfRpcClient(self.password, server=self.host, port=self.port, ssl=False)
            return True
        except Exception as exc:
            logger.debug('Failed to connect to msfrpcd: %s', exc)
            self.client = None
            return False

    def _start_msf_container(self):
        subprocess.run(["docker", "rm", "-f", self.container_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cmd = [
            "docker", "run", "-d", "--name", self.container_name,
            "-p", f"{self.port}:{self.port}",
            self.image,
            "msfrpcd", "-U", self.user, "-P", self.password, "-S", "-a", "0.0.0.0", "-p", str(self.port)
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError(f"Failed to start Metasploit container: {proc.stderr.strip()}")
        self._container_started = True

    def stop_container(self):
        if self._container_started:
            subprocess.run(["docker", "rm", "-f", self.container_name], check=False)
            self._container_started = False

    def close(self):
        try:
            if self.client:
                self.client = None
        finally:
            self.stop_container()

    def use_module(self, module_type, module_name, options=None):
        if not self.client:
            raise RuntimeError('Not connected to Metasploit')
        mod = self.client.modules.use(module_type, module_name)
        if options:
            for k, v in options.items():
                mod[k] = v
        return mod

    def run_module(self, module_type, module_name, options=None):
        mod = self.use_module(module_type, module_name, options)
        job_id = mod.execute()
        return job_id

    def list_sessions(self):
        if not self.client:
            return {}
        return self.client.sessions.list

    def kill_session(self, sid):
        if not self.client:
            raise RuntimeError('Not connected to Metasploit')
        return self.client.sessions.kill(sid)
