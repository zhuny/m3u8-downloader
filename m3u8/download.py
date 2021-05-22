from pathlib import Path

from m3u8.parse import M3UFile


def download(url: str, target_folder: Path):
    f = M3UFile.from_url(url)
    f.save(target_folder)
