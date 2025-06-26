import json
from json import JSONDecodeError
from pathlib import Path


class HonulabsToken:
    FILE_PATH = Path.home() / '.honulabsrc'

    def __init__(self, token: str | None = None):
        if token is None:
            token = self._get_token_from_file()
        else:
            self._save_token(token)
        self.token = token

    def _get_token_from_file(self) -> str | None:
        if not self.FILE_PATH.exists():
            self.FILE_PATH.touch(exist_ok=True)

        with open(self.FILE_PATH) as f:
            try:
                data = json.load(f)
                return data.get('token')
            except JSONDecodeError:
                return None

    def _save_token(self, token: str):
        if not self.FILE_PATH.exists():
            self.FILE_PATH.touch(exist_ok=True)

        with open(self.FILE_PATH) as f:
            try:
                data = json.load(f)
            except JSONDecodeError:
                data = {}

        data['token'] = token

        with open(self.FILE_PATH, 'w') as f:
            json.dump(data, f)
