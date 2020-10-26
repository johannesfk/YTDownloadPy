import pafy
import re
import datetime

from os import path, remove
from pydub import AudioSegment
from pydub.utils import mediainfo

pafy.set_api_key('AIzaSyCB7wHEvZyWRGzx69UDFe7CnUlPYYf3LLo')

input = input('Enter Youtube links or Ids:\n')
vidIds = input.split(',')
print(vidIds)

for i in vidIds:
    
    text = i
    try:
        found = re.search('(?<=v=).*?(?=&feature)', text).group(0)
    except AttributeError:
        # AAA, ZZZ not found in the original string
        found = 'error' # apply your error handling
    print(found)
    
    video = pafy.new(found)
    bestaudio = video.getbestaudio()
    bestaudio.bitrate #get bit rate
    bestaudio.extension #extension of audio fileurl
    ...
    bestaudio.url #get url
    ...
    #download if you want
    bestaudio.download()

    # Convert to wav                                                                       
    src = bestaudio.title + "." + bestaudio.extension

    artist = video.author
    if artist.endswith("Topic"):
        artist = artist[:-8]
    dst = artist + " - " + bestaudio.title + ".wav"

    srcMetadata = {
        "artist": artist,
        "title": video.title,
        "date": video.published[0:4]
    }
    print(srcMetadata)
    # convert webm to wav                                                            
    sound = AudioSegment.from_file(src, "webm", )
    sound.export(dst,
        format="wav",
        codec="pcm_s24le",
        id3v2_version="4",
        tags={
            "artist": artist,
            "title": video.title,
            "date": video.published[0:4]
        }
    )
    print("Track Downloaded")
    # remove(src)