from logging import getLogger
from subprocess import run


class ShellClient:
    def __init__(
        self, cmd: str, common_args: list[str] = None, shell=False, as_str=False
    ):
        self._logger = getLogger(cmd)
        self.cmd = cmd
        self.common_args = common_args if common_args else []
        self.shell = shell
        self.as_str = as_str

    def run(self, args: list[str], cwd: str = None, supress_error=False):
        full_cmd = [self.cmd] + args + self.common_args
        str_cmd = " ".join(full_cmd)
        self._logger.debug(f"Command: {str_cmd}")
        cmd = str_cmd if self.as_str else full_cmd
        result = run(
            cmd,
            capture_output=True,
            shell=self.shell,
            cwd=cwd,
        )
        self._logger.debug(f"Command output: {result.stdout}")
        if result.returncode != 0 and not supress_error:
            self._logger.error(f"Failed to run command: {cmd}")
            self._logger.error(f"Command error: {result.stderr}")
            raise RuntimeError("Failed to run command")
        return result
