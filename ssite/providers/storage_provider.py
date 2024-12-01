from abc import ABC, abstractmethod
from logging import getLogger

from ssite.config import SsiteConfig


class StorageProvider(ABC):
    def __init__(self, config: SsiteConfig):
        self._config = config
        self._logger = getLogger(f"{self._config.bucket_type.value}-provider")

    @property
    def config(self):
        return self._config

    @abstractmethod
    def sync(self):
        pass

    @abstractmethod
    def list_files(self, prefix: str = ""):
        pass
