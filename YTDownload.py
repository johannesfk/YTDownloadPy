import json
import yt_dlp
import re

from os import path, remove

class MyLogger:
    def debug(self, msg):
        # For compatibility with youtube-dl, both debug and info are passed into debug
        # You can distinguish them by the prefix '[debug] '
        if msg.startswith('[debug] '):
            pass
        else:
            self.info(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


# ℹ️ See the docstring of yt_dlp.postprocessor.common.PostProcessor
class MyCustomPP(yt_dlp.postprocessor.PostProcessor):
    # ℹ️ See docstring of yt_dlp.postprocessor.common.PostProcessor.run
    def run(self, info):
        self.to_screen('Doing stuff')
        return [], info


# ℹ️ See "progress_hooks" in the docstring of yt_dlp.YoutubeDL
def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

codecInput = input('Sound codec:\n0: WAV\n1: MP3\n')
vidInput = input('Enter Youtube links or Ids:\n')

outputCodec = 'wav'

if codecInput == "0":
    outputCodec = "wav"
if codecInput == "1":
    outputCodec = "mp3"

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': outputCodec,
        'preferredquality': '320',
    }],
    'logger': MyLogger(),
    'progress_hooks': [my_hook],
    # Add custom headers
    'http_headers': {'Referer': 'https://www.google.com'}
}


vidIds = vidInput.split(',')
print(vidIds)

for i in vidIds:
    
    text = i
    try:
        # found = re.search('(?<=v=).*?(?=&feature)', text).group(0)
        found = re.search('(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})', text).group(0)
    except AttributeError:
            found = 'error' # apply your error handling
    print(found)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.add_post_processor(MyCustomPP())
        info = ydl.extract_info(text)

        # ℹ️ ydl.sanitize_info makes the info json-serializable
        # print(json.dumps(ydl.sanitize_info(info)))