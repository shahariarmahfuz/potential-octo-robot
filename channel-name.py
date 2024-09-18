#!/usr/bin/python3

import os
import requests
import sys

windows = False
if 'win' in sys.platform:
    windows = True

def grab_youtube_m3u8(url):
    """Extract .m3u8 link from YouTube Live using yt-dlp."""
    command = f'yt-dlp -g {url}'
    m3u8_link = os.popen(command).read().strip()
    if m3u8_link:
        print(m3u8_link)
    else:
        print(f"No m3u8 link found for {url}.")

def grab(url):
    """Extract .m3u8 link from non-YouTube sources."""
    try:
        response = requests.get(url, timeout=15).text
        if '.m3u8' not in response:
            response = requests.get(url).text
            if '.m3u8' not in response:
                if windows:
                    print('https://raw.githubusercontent.com/user-name/repo-name/main/assets/info.m3u8')
                    return
                os.system(f'curl "{url}" > temp.txt')
                response = ''.join(open('temp.txt').readlines())
                if '.m3u8' not in response:
                    print('https://raw.githubusercontent.com/user-name/repo-name/main/assets/info.m3u8')
                    return
        end = response.find('.m3u8') + 5
        tuner = 100
        while True:
            if 'https://' in response[end-tuner : end]:
                link = response[end-tuner : end]
                start = link.find('https://')
                end = link.find('.m3u8') + 5
                break
            else:
                tuner += 5
        streams = requests.get(link[start:end]).text.split('#EXT')
        hd = streams[-1].strip()
        st = hd.find('http')
        print(hd[st:].strip())
    except Exception as e:
        print(f"Error processing URL: {url}, Error: {e}")

print('#EXTM3U')
print('#EXT-X-VERSION:3')
print('#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=2560000')

with open('channel-name.txt') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('~~'):
            continue
        if not line.startswith('https:'):
            # Channel info - Not needed for extracting .m3u8, just skip this
            continue
        else:
            if 'youtube.com' in line or 'youtu.be' in line:
                # Use yt-dlp to extract .m3u8 from YouTube live streams
                grab_youtube_m3u8(line)
            else:
                # Use standard method for other URLs
                grab(line)

# Cleanup temporary files
if 'temp.txt' in os.listdir():
    os.system('rm temp.txt')
    os.system('rm watch*')
