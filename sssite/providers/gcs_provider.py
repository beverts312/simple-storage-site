import os

from google.cloud import storage

from sssite.providers.storage_provider import StorageProvider
from sssite.utils import ShellClient


class GCSProvider(StorageProvider):
    def __init__(self, config):
        super().__init__(config)
        self._client = storage.Client()
        self._gsutil = ShellClient("gsutil")

    @property
    def full_name(self):
        return f"gs://{self._config.bucket_name}"

    def _get_full_path(self, prefix=""):
        return "".join([self.full_name, self.config.bucket_prefix, prefix])

    def sync(self, path: str = ""):
        destination = "".join([self.config.local_storage_path, path])
        os.makedirs(destination, exist_ok=True)
        self._gsutil.run(["rsync", "-r", self._get_full_path(path), destination])

    def list_files(self, prefix: str = ""):
        result = self._gsutil.run(["ls", self._get_full_path(prefix)])
        result_array = result.stdout.decode("utf-8").splitlines()
        return [item.replace(f"{self.full_name}/", "") for item in result_array]
