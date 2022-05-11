import requests


class TelegramBot:
    def __init__(self, token, server=None):
        if server is None or server[:4] != 'http':
            server = 'https://api.telegram.org'
        self.__server = server
        self.__token = token

    def request(self, method_name, json=None, files=None, args=None):
        args = '&'.join([f'{k}={v}' for k, v in self.__filter(**args).items()]) if args is not None else ''
        response = requests.post(f'{self.__server}/bot{self.__token}/{method_name}?{args}', json=json, files=files)
        if response.status_code == 200 and (json := response.json()) and \
                'ok' in json and json['ok'] is True and 'result' in json:
            return json['result']
        else:
            return None

    def __filter(self, **kwargs):
        return dict([(k, v) for k, v in kwargs.items() if v is not None])

    def get_me(self):
        """A simple method for testing your bot's authentication token. Requires no parameters. Returns basic information about the bot in form of a User object."""
        return self.request('getMe')

    def get_updates(self, offset=0):
        return self.request('getUpdates', json=dict(
            offset=offset
        ))

    def send_message(self, chat_id, text, parse_mode=None):
        return self.request('sendMessage', json=self.__filter(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode
        ))
