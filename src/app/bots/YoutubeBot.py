import os.path

import cv2
import numpy as np
import yt_dlp


class YoutubeBot:
    def __init__(self, download_path=None):
        self.download_path = download_path if download_path is not None else './downloads'
        self.__ydl_opts = dict(
            format='bestaudio',
            paths=dict(home=self.download_path),
            outtmpl=dict(default='%(id)s/%(id)s.%(ext)s'),
            postprocessors=[
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3'
            }, {
                'key': 'EmbedThumbnail'
            }
            ],
            writethumbnail=True,
            keepvideo=True,
            windowsfilenames=True
        )

    def playlist(self, url, playlistend=-1, override_opts=None):
        _playlist_opts = dict(
            simulate=True,
            extract_flat=True,
            playlistend=playlistend
        )
        opts = {**self.__ydl_opts, **_playlist_opts}
        opts = {**opts, **override_opts} if isinstance(override_opts, dict) else opts
        with yt_dlp.YoutubeDL(opts) as ydl:
            return ydl.extract_info(url, download=False)

    def download(self, url, download=True, override_opts=None):
        opts = {**self.__ydl_opts, **override_opts} if isinstance(override_opts, dict) else self.__ydl_opts
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=download)
            id = info['id']
            files = dict()
            if os.path.exists(folder := f'{self.download_path}/{id}'):
                files['folder'] = folder
                if os.path.exists(thumbnail := f'{folder}/{id}.png'):
                    files['thumbnail'] = thumbnail
                    im = cv2.imread(thumbnail)
                    size = np.array(im.shape[:2])
                    h, w = map(int, size / np.max(size) * 320)
                    im = cv2.resize(im, (w, h))
                    thumbnail_320 = f'{folder}/{id}.jpeg'
                    cv2.imwrite(thumbnail_320, im)
                    files['thumbnail_320'] = thumbnail_320
                if os.path.exists(audio := f'{folder}/{id}.mp3'):
                    files['audio'] = audio
                if os.path.exists(video := f'{folder}/{id}.webm'):
                    files['video'] = video

            return info, files
