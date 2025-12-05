import zipfile
from pathlib import Path

import requests
from tqdm import tqdm
from loguru import logger


class FileDownloader:
    @staticmethod
    def download_file(file_url: str, file_path: str | Path) -> None:
        response = requests.get(file_url, stream=True)
        if response.status_code != 200:
            raise Exception(f'The file is not available for download at the link: {file_url}')
        total_size = int(response.headers.get('content-length', 0))
        progress_tqdm = tqdm(desc='Loading file', total=total_size, unit='iB', unit_scale=True)
        with open(file_path, 'wb') as file:
            for data in response.iter_content(chunk_size=4096):
                size = file.write(data)
                progress_tqdm.update(size)


    @staticmethod
    def extract_zip(zip_path: Path) -> None:
        with zipfile.ZipFile(zip_path, 'r') as archive:
            archive.extractall(path=zip_path.parent.parent)


    @classmethod
    def download_and_extract_zip(
        cls,
        zip_url: str,
        base_dir: Path,
        override: bool = False,
    ) -> Path:
        file_dir = base_dir / Path(Path(zip_url).stem)
        if file_dir.is_dir() and not override:
            return file_dir
        file_dir.mkdir(exist_ok=True, parents=True)
        zip_path = file_dir / Path(zip_url).name
        logger.info(f'Loading file {zip_url} to path {zip_path}')
        cls.download_file(file_url=zip_url, file_path=zip_path)
        cls.extract_zip(zip_path=zip_path)
        return file_dir
