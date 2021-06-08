import base64
import errno
import hashlib
import logging
import os
import pathlib
import typing
from logging import Logger
from os import path

from google.api_core import exceptions as g_exceptions
from google.cloud import storage as g_storage


class GStorageWrapper:
    logger: Logger

    @staticmethod
    def _md5_base64(filename):
        """Returns md5 hash with base of 64"""
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        hash_md5_base64 = base64.b64encode(hash_md5.digest()).decode('utf-8')
        return hash_md5_base64

    def __init__(self):
        self.logger = logging.getLogger(str(GStorageWrapper.__name__))
        self.logger.setLevel(logging.DEBUG)

    def upload_folder(
            self,
            bucket_name: str,
            source_folder: pathlib.Path,
            destination_folder_path: pathlib.PurePosixPath):
        if not destination_folder_path.is_absolute():
            raise ValueError(f"'destination_folder_path' should be absolute path")

        if not source_folder.exists():
            raise ValueError("'source_folder' should exist")
        source_folder = source_folder.absolute()
        if not source_folder.is_dir():
            raise ValueError("'source_folder' should not be a file")

        local_abs_paths = []
        remote_abs_paths = []

        for root, _, filenames in os.walk(str(source_folder)):
            for filename in filenames:
                local_abs_path = (pathlib.Path(root) / filename).absolute()
                local_abs_paths.append(local_abs_path)

                # take filename from local absolute path and append it to remote folder path
                remote_abs_path = destination_folder_path / local_abs_path.relative_to(source_folder)
                # remove heading slash
                # /some/path/file.txt -> some/path/file.txt
                remote_abs_path = remote_abs_path.as_posix()[1:]
                remote_abs_paths.append(remote_abs_path)

        both_paths = zip(local_abs_paths, remote_abs_paths)

        bucket = g_storage.Client().get_bucket(bucket_name)
        for (local_abs_path, remote_abs_path) in both_paths:
            self.lazy_upload_blob(bucket_name, str(local_abs_path), remote_abs_path, bucket)

    def download_folder(self,
                        bucket_name: str,
                        source_folder: pathlib.PurePosixPath,
                        destination_folder: pathlib.Path):
        if not source_folder.is_absolute():
            raise ValueError(f"'source_folder' should be absolute path")
        source_folder_str = str(source_folder)[1:]  # remove heading slash of absolute path

        if not destination_folder.exists():
            raise ValueError("'destination_folder' should exist")
        if not destination_folder.is_dir():
            raise ValueError("'destination_folder' should be a folder")
        bucket = g_storage.Client().get_bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=source_folder_str)

        for blob in blobs:
            without_prefix = pathlib.PurePosixPath(blob.name).relative_to(source_folder_str)
            if len(without_prefix.name) < 1:
                # this means, we took blob folder somehow
                continue
            destination_file = destination_folder / without_prefix
            self.lazy_download_blob(bucket_name, blob.name, destination_file, True, bucket)

    def lazy_upload_blob(self, bucket_name, source_file_name, destination_blob_name, bucket=None):
        """Uploads a file to the bucket if it has different hash."""

        if bucket is None:
            storage_client = g_storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
        remote_blob = bucket.get_blob(destination_blob_name)
        local_md5 = GStorageWrapper._md5_base64(source_file_name)

        if remote_blob is not None:
            remote_md5 = remote_blob.md5_hash
            if remote_md5 == local_md5:
                self.logger.info(f'Blob `{destination_blob_name} is '
                                 f'already in bucket `{bucket_name}`')
                return
            self.logger.info(f'Updating blob `{destination_blob_name}` to '
                             f'bucket `{bucket_name}` from `{source_file_name}`')

        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        # check for integrity of uploaded file
        uploaded_blob = bucket.get_blob(destination_blob_name)
        uploaded_md5 = uploaded_blob.md5_hash
        if uploaded_md5 != local_md5:
            raise g_exceptions.DataLoss('Downloaded file differs from remote')

        self.logger.info(f'File `{source_file_name}` successfully uploaded '
                         f'to `{destination_blob_name}` of bucket `{bucket_name}`')

    def lazy_download_blob(self, bucket_name, source_blob_name, destination_file_name, create_folder=False, bucket=None):
        """Downloads a blob from the bucket if the local version of file differs
        from the remote version (calculated using md5 hash)."""

        if bucket is None:
            storage_client = g_storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
        remote_blob = bucket.get_blob(source_blob_name)
        remote_md5 = remote_blob.md5_hash

        if path.exists(destination_file_name):
            local_md5 = GStorageWrapper._md5_base64(destination_file_name)
            if remote_md5 == local_md5:
                self.logger.info(f'Blob `{source_blob_name}` is already downloaded to `{destination_file_name}`')
                return

        if create_folder and not os.path.exists(os.path.dirname(destination_file_name)):
            try:
                os.makedirs(os.path.dirname(destination_file_name))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        # check for integrity of downloaded file
        downloaded_md5 = GStorageWrapper._md5_base64(destination_file_name)
        if remote_md5 != downloaded_md5:
            raise g_exceptions.DataLoss('Downloaded file differs from remote')

        self.logger.info(f'Blob `{source_blob_name}` successfully downloaded to `{destination_file_name}`')
