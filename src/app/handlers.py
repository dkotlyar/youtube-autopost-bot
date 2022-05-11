import os
import re
import shutil
import time
import urllib
from threading import Thread

import cv2
import numpy as np

from app.bots.YoutubeBot import YoutubeBot


def post_message(tb, chat_id, text, info, files):
    chat_action = AsyncSendChatAction(tb, chat_id)
    chat_action.send('typing')

    id = info['id']
    channel = info['channel']
    title = info['title']

    messages = []
    msg = ''
    for paragraph in text.split('\n'):
        if (len(msg) + len(paragraph)) < (4000 if len(messages) > 0 else 1000):
            msg += '\n' + paragraph
        else:
            messages.append(msg.strip())
            msg = paragraph
    if len(msg) > 0:
        messages.append(msg.strip())

    tb.request('sendPhoto', dict(
        chat_id=chat_id,
        parse_mode='html',
        caption=messages[0],
        photo=f'https://img.youtube.com/vi/{id}/maxresdefault.jpg'
    ))

    for msg in messages[1:]:
        tb.request('sendMessage', dict(
            chat_id=chat_id,
            parse_mode='html',
            text=msg
        ))

    chat_action.terminate()

    if 'folder' in files:
        if 'audio' in files:
            folder = files['folder']

            chat_action.send('upload_document')

            tb.request('sendAudio', args=dict(
                chat_id=chat_id,
                caption=urllib.parse.quote_plus(f'<strong>{title}</strong>'),
                parse_mode='html',
                performer=urllib.parse.quote_plus(channel),
                title=urllib.parse.quote_plus(title)
            ), files=dict(
                audio=open(files['audio'], 'rb'),
                thumb=open(files['thumbnail_320'], 'rb') if 'thumbnail_320' in files else None
            ))
            chat_action.terminate()


class Handler:
    def __init__(self, tb):
        self.tb = tb
        self.__yb = YoutubeBot()

    def __is_start_youtube_link(self, text):
        return text.startswith('https://www.youtube.com/watch?') or text.startswith('https://youtu.be/')

    def update(self, data):
        if 'channel_post' in data:
            self.__channel_post(data['channel_post'])
        elif 'message' in data:
            self.__message(data['message'])

    def __channel_post(self, post):
        chat_id = post['chat']['id']
        if 'text' in post:
            text = post['text']
            if self.__is_start_youtube_link(text):
                url = re.split('[\s]', text)[0]

                self.tb.request('deleteMessage', dict(
                    chat_id=post['chat']['id'],
                    message_id=post['message_id']
                ))

                info, files = self.__yb.download(url, download=True)

                if 'folder' in files:
                    id = info['id']
                    channel = info['channel']
                    title = info['title']
                    description = info['description']

                    if len(description) + len(title) > 1000:
                        new_description = ''
                        for paragraph in filter(None, description.split('\n')):
                            if len(paragraph) > len(new_description):
                                new_description = paragraph
                        description = new_description

                    if 'thumbnail' in files:
                        self.tb.request('sendPhoto', args=dict(
                            chat_id=chat_id,
                            parse_mode='html',
                            caption=urllib.parse.quote_plus(f'<strong>{title}</strong>\n\n{description}')
                        ), files=dict(
                            photo=open(files['thumbnail'], 'rb')
                        ))

                    if 'audio' in files:
                        self.tb.request('sendAudio', args=dict(
                            chat_id=chat_id,
                            caption=urllib.parse.quote_plus(f'<strong>{title}</strong>'),
                            parse_mode='html',
                            performer=urllib.parse.quote_plus(channel),
                            title=urllib.parse.quote_plus(title)
                        ), files=dict(
                            audio=open(files['audio'], 'rb'),
                            thumb=open(files['thumbnail_320'], 'rb') if 'thumbnail_320' in files else None
                        ))

                    shutil.rmtree(files['folder'])

    def __message(self, message):
        chat_id = message['chat']['id']
        if 'text' in message:
            text = message['text']
            if self.__is_start_youtube_link(text):
                chat_action = AsyncSendChatAction(self.tb, chat_id)
                chat_action.send('typing')

                url = re.split('[\s]', text)[0]
                info, files = self.__yb.download(url, download=False, override_opts=dict(
                    format='best'
                ))
                video_url = info['url']
                info, files = self.__yb.download(url, download=True)

                id = info['id']
                channel = info['channel']
                title = info['title']
                description = info['description']

                text = f'<strong>{title}</strong>\n\n' \
                       f'{description}\n\n' \
                       f'<a href="{video_url}">Скачать видео</a>\n\n' \
                       f'https://www.youtube.com/watch?v={id}'

                messages = []
                msg = ''
                for paragraph in text.split('\n'):
                    if (len(msg) + len(paragraph)) < (4000 if len(messages) > 0 else 1000):
                        msg += '\n' + paragraph
                    else:
                        messages.append(msg.strip())
                        msg = paragraph
                if len(msg) > 0:
                    messages.append(msg.strip())

                self.tb.request('sendPhoto', dict(
                    chat_id=chat_id,
                    parse_mode='html',
                    caption=messages[0],
                    photo=f'https://img.youtube.com/vi/{id}/maxresdefault.jpg'
                ))

                for msg in messages[1:]:
                    self.tb.request('sendMessage', dict(
                        chat_id=chat_id,
                        parse_mode='html',
                        text=msg
                    ))

                chat_action.terminate()

                if 'folder' in files:
                    if 'audio' in files:
                        folder = files['folder']
                        if 'thumbnail' in files:
                            im = cv2.imread(files['thumbnail'])
                            size = np.array(im.shape[:2])
                            h, w = map(int, size / np.max(size) * 320)
                            im = cv2.resize(im, (w, h))
                            thumbnail_320 = f'{folder}/{id}.jpeg'
                            cv2.imwrite(thumbnail_320, im)
                            files['thumbnail_320'] = thumbnail_320

                        chat_action.send('upload_document')

                        self.tb.request('sendAudio', args=dict(
                            chat_id=chat_id,
                            caption=urllib.parse.quote_plus(f'<strong>{title}</strong>'),
                            parse_mode='html',
                            performer=urllib.parse.quote_plus(channel),
                            title=urllib.parse.quote_plus(title)
                        ), files=dict(
                            audio=open(files['audio'], 'rb'),
                            thumb=open(files['thumbnail_320'], 'rb') if 'thumbnail_320' in files else None
                        ))
                        chat_action.terminate()

                    shutil.rmtree(files['folder'])
            else:
                self.tb.request('sendMessage', dict(
                    chat_id=chat_id,
                    text='Сейчас я умею обрабатывать только ссылки платформы YouTube'
                ))


class AsyncHandler:
    def __init__(self, tb):
        self.tb = tb
        self.handler = Handler(tb)

    def update(self, data):
        Thread(target=self.handler.update, kwargs=dict(data=data)).start()


class AsyncSendChatAction:
    def __init__(self, tb, chat_id):
        self.action = 'typing'
        self.tb = tb
        self.chat_id = chat_id
        self.__terminate = False

    def send_once(self, action):
        self.tb.request('sendChatAction', dict(
            chat_id=self.chat_id,
            action=action
        ))

    def send(self, action):
        self.action = action
        self.__terminate = False
        Thread(target=self.__send).start()

    def terminate(self):
        self.__terminate = True

    def __send(self):
        while not self.__terminate:
            self.send_once(self.action)
            time.sleep(5)
