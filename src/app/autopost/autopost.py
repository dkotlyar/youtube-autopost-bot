import shutil
import time
from threading import Thread

from app.bots.YoutubeBot import YoutubeBot
from app.handlers import post_message
from app.models import db
from app.models.youtube_model import VideoPosted


class DefaultAutopostFilter:
    def filter(self, info):
        return True


class DefaultPrepost:
    def prepost(self, info, files, text):
        return info, files, text


class AutopostInstance:
    def __init__(self, channel, chat_id, post_filter=None, prepost=None):
        self.channel = channel
        self.chat_id = chat_id
        if post_filter is None:
            post_filter = DefaultAutopostFilter()
        self.post_filter = post_filter
        if prepost is None:
            prepost = DefaultPrepost()
        self.prepost = prepost


class Autopost:
    def __init__(self, app_ctx, tb, instances):
        self._terminated_ = False
        self.instances = instances
        self.app_ctx = app_ctx
        self.yb = YoutubeBot()
        self.tb = tb

    def terminate(self):
        self._terminated_ = True

    def run(self):
        self._terminated_ = False
        Thread(target=self.__run).start()

    def __run(self):
        with self.app_ctx:
            while not self._terminated_:
                for instance in self.instances:
                    info = self.yb.playlist(url=f'https://www.youtube.com/channel/{instance.channel}/videos', playlistend=5,
                                            override_opts=dict(quiet=True))
                    for entry in info['entries'][::-1]:
                        try:
                            id = entry['id']
                            live_status = entry['live_status']
                            if live_status in ['was_live', 'not_live', None]:
                                posted = VideoPosted.query.filter_by(youtube_id=id).count() > 0
                                if not posted:
                                    meta, _ = self.yb.download(entry['url'], download=False)
                                    if instance.post_filter.filter(meta):
                                        info, files = self.yb.download(entry['url'], download=True)
                                        title = info['title']
                                        description = info['description']
                                        text = f'<strong>{title}</strong>\n\n' \
                                               f'{description}'
                                        info, files, text = instance.prepost.prepost(info, files, text)
                                        post_message(self.tb, instance.chat_id, text, info, files)
                                        if 'folder' in files:
                                            shutil.rmtree(files['folder'])
                                        video_posted = VideoPosted(youtube_id=id)
                                        db.session.add(video_posted)
                                        db.session.commit()
                                        time.sleep(10)  # sleep after every downloaded video
                        except:
                            db.session.rollback()
                    time.sleep(10)  # sleep after every instance
                time.sleep(60)  # sleep at the end
