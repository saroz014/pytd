#!/usr/bin/env python3

import os
import re
from pytube import YouTube, Playlist
from tqdm import tqdm


class YTD:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def save_to():
        home_dir = os.path.expanduser('~')
        return os.path.join(home_dir, 'Downloads')

    def progress(self, stream, chunk, bytes_remaining):
        # percent = (100*(filesize - bytes_remaining)) / filesize
        # downloaded = (self.file_size * 1000 * 1000 - bytes_remaining) / (1000 * 1000)
        # pbar.update(downloaded)
        self.pbar.update()
        # print(f"{percent}% downloaded")

    def download_video(self):
        video = YouTube(self.url, on_progress_callback=self.progress)
        video_type = video.streams.get_highest_resolution()
        # video_type = video.streams.filter(progressive = True, file_extension = "mp4").first()
        video_title = video.title
        self.file_size = video_type.filesize
        # print(file_size)
        self.pbar = tqdm(total=self.file_size / (1024 * 4))
        # self.pbar = tqdm(total=self.file_size / (1000 * 1000))
        # self.pbar = tqdm(total=self.file_size)
        # self.pbar.set_description(f"Downloading {video_title}")
        print(f"Downloading {video_title}({self.file_size / (1000 * 1000)} MB)")
        video_type.download(self.save_to())
        print('completed')
        self.pbar.close()

    def download_playlist(self):
        try:
            playlist = Playlist(self.url)
        except KeyError:
            print('Not a playlist link!!!')
            return
        playlist._video_regex = re.compile(r"\"url\":\"(/watch\?v=[\w-]*)")
        # print(len(playlist.video_urls))
        for url in playlist:
            self.url = url
            self.download_video()


def get_downloader_attr(download_type):
    downloader_attr_dict = {'1': 'download_video',
                            '2': 'download_playlist'}
    return downloader_attr_dict.get(download_type)


def main():
    download_type = input("Enter 1 for video. 2 for entire playlist: ")
    if download_type != '1' and download_type != '2':
        print('Invalid input!!!')
        main()
    url = input("Enter youtube url: ")
    downloader_attr = get_downloader_attr(download_type)
    if downloader_attr:
        ytd = YTD(url)
        getattr(ytd, downloader_attr)()


if __name__ == '__main__':
    main()
