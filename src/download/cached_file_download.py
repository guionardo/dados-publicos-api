import datetime
import logging
import os
import time

import filelock
import requests


class CachedFileDownload:

    def __init__(self, cache_folder: str, url: str, extraction_date: datetime.datetime):
        self.log = logging.getLogger(self.__class__.__name__)
        self.cache_folder = cache_folder
        self.url = url
        self.cache_file_dir = os.path.join(
            cache_folder, extraction_date.strftime('%Y%m%d'))
        self.cache_file_name = os.path.join(
            self.cache_file_dir, os.path.basename(url))

    def is_in_cache(self) -> bool:
        return os.path.isfile(self.cache_file_name)

    def download_file(self) -> str:
        if self.is_in_cache():
            self.log.info('Download file %s (cached) -> %s',
                          self.url, self.cache_file_name)
            return self.cache_file_name
        try:
            start_time = time.time()
            os.makedirs(self.cache_file_dir, exist_ok=True)
            lock = filelock.FileLock(self.cache_file_name+'.lck')
            with lock.acquire(timeout=5):
                temp_file_name = self.cache_file_name+'.tmp'
                if os.path.isfile(temp_file_name):
                    os.remove(temp_file_name)
                self.log.info('Downloading %s', self.url)
                with requests.get(self.url, stream=True) as r:
                    handshake_time = time.time()

                    r.raise_for_status()
                    content_length = int(r.headers.get('Content-Length', '-1'))
                    self.log.info('Handshake after %s - Content-Length: %s', datetime.timedelta(
                        seconds=handshake_time-start_time), content_length)
                    bytes_written = 0
                    with open(temp_file_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            # If you have chunk encoded response uncomment if
                            # and set chunk_size parameter to None.
                            # if chunk:
                            f.write(chunk)
                            bytes_written += len(chunk)
                os.rename(temp_file_name, self.cache_file_name)
                self.log.info('Download file %s (%s bytes) -> %s (%sB/s)',
                              self.url, self.cache_file_name, bytes_written, bytes_written/(time.time()-start_time))
            lock.release()
            return self.cache_file_name
        except filelock.Timeout as exc:
            self.log.error('Downloading operation in progress - %s', exc)
        except Exception as exc:
            self.log.error('Exception on downloading %s -> %s', self.url, exc)

        return ''
