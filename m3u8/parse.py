import re
import urllib.parse
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import List

import requests


@dataclass
class EXTINF:
    runtime: Decimal
    resource: str


class M3UFile:
    def __init__(self, track_list, url: str, extra_info: dict = None):
        self.track_list: List[EXTINF] = track_list
        self.extra_info = extra_info or dict()
        self.url = url

    @classmethod
    def _parse_line(cls, line):
        g = re.fullmatch('#(.+?)(?::(.*?))?', line)
        if g:
            return g.groups()
        else:
            return None, None

    @classmethod
    def _check_header(cls, lines):
        directive, argv = cls._parse_line(next(lines))
        if directive == 'EXTM3U' and argv is None:
            pass
        else:
            raise ValueError("Header Check Error")

    @classmethod
    def _from_text(cls, url: str, content: str):
        lines = iter(content.splitlines())
        cls._check_header(lines)
        extra_info = {}
        track_list = []
        for line in lines:
            directive, argv = cls._parse_line(line)
            if directive == 'EXTINF':
                track_list.append(EXTINF(Decimal(argv.strip(',')), next(lines)))
            else:
                extra_info[directive] = argv
        return cls(track_list, url, extra_info)

    @classmethod
    def from_url(cls, url: str):
        return cls._from_text(url, requests.get(url).text)

    def save(self, target: Path):
        target.mkdir(parents=True, exist_ok=True)

        for track in self.track_list:
            local_file_path = target / track.resource
            if local_file_path.is_file():
                print(track.resource, 'is skipped')
                continue

            with (target / track.resource).open('wb') as f:
                resource_url = urllib.parse.urljoin(self.url, track.resource)
                resource_response = requests.get(resource_url)
                f.write(resource_response.content)
                print(track.resource, 'is loaded')
