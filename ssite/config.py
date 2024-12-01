import os
from enum import Enum


class ProviderType(Enum):
    GCS = "gcs"


class SsiteConfig:
    @property
    def name(self):
        return os.getenv("SS_SITE_NAME")

    @property
    def bucket_name(self):
        return os.getenv("SS_BUCKET_NAME")

    @property
    def bucket_type(self) -> ProviderType:
        return ProviderType.GCS

    @property
    def local_storage_path(self):
        return os.getenv("SS_LOCAL_STORAGE_PATH", "./tmp")

    @property
    def bucket_prefix(self):
        return os.getenv("SS_BUCKET_PREFIX", "")

    @property
    def install_dir(self):
        return os.path.dirname(os.path.realpath(__file__))

    @property
    def resource_dir(self):
        return f"{self.install_dir}/resources"
