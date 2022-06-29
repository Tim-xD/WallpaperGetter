if __name__ != "__main__":
    exit()

import argparse
import requests
import json
from PIL import Image
from io import BytesIO
from datetime import datetime
from user_agent import generate_user_agent
import subprocess
import random

# Reddit
class Reddit:

    def GetRequestUrl(sub: str, sort: str, nsfw: bool) -> str:
        """Format Reddit url"""

        if nsfw:
            return f"https://old.reddit.com/r/{sub}/{sort}.json?limit=1&include_over_18=on"
        return f"https://old.reddit.com/r/{sub}/{sort}.json?limit=1"

    def GetImgUrl(json: list) -> str:
        """Get image url from json"""

        # Detect if random sort was used
        rand = False
        
        # Different json format depending on the sort
        try:
            contentType = json["data"]["children"][0]["data"]["post_hint"]
        except:
            try:
                contentType = json[0]["data"]["children"][0]["data"]["post_hint"]
                rand = True
            except:
                # Reddit post didn't have an image
                print("Reddit post was not an image, try with a sub with only images")
                exit(1)
        
        if contentType != "image":
            # Reddit post didn't have an image
            print("Reddit post was not an image, try with a sub with only images")
            exit(1)

        if rand:
            url = json[0]["data"]["children"][0]["data"]["url"]
        else:
            url = json["data"]["children"][0]["data"]["url"]

        return url


def ParseArgs():
    """Parse argument"""
    
    parser = argparse.ArgumentParser()
    parser.add_argument("subreddits", type=str, help="Sub reddits to get image from. Format : [Sub] or [Sub1,Sub2,Sub,...])")
    parser.add_argument("sort", type=str, choices=['top', 'new', 'controversial', 'old', 'random', 'best', 'hot'], help="The sort used to get the image")
    parser.add_argument('--nsfw', nargs='?', choices=['on', 'off'], const='off', help='Include NSFW images (default = False) : --nsfw  {on or off}')
    parser.add_argument('--path', nargs='?', const='', help='Path to save wallpapers : --path {path}')
    args = parser.parse_args()

    return args.subreddits, args.sort, args.nsfw, args.path
    

def CreateUrl(subs: str, sort: str, nsfw: str) -> str:
    """Create URL"""

    # Parse subs
    subs = subs[1:-1]
    subs = list(subs.split(','))

    return Reddit.GetRequestUrl(random.choice(subs), sort, True if nsfw == "on" else False)

def GetRequest(url: str) -> bytes:
    """Make Get request and return json of response"""
    
    try:
        # Make request
        # Doesn't work with Reddit without User-agent, so generate one randomized
        request = requests.get(url, headers = {'User-agent': generate_user_agent(os=('all'), device_type=('all'), navigator=('all'))})
        request.raise_for_status()
    except Exception as e:
        # Error (no internet, bad status code...)
        print(e)
        exit(1)
    
    return request.content

def GetImage(resp: bytes, path: str) -> str:
    """Retrieve image from request response and save it"""

    # Retrieve image url from response
    content = json.loads(resp)
    url = Reddit.GetImgUrl(content)

    # Get image
    try:
        img = Image.open(BytesIO(GetRequest(url)))
    except Exception as e:
        # Reddit post didn't have an image
        print(e)
        exit(1)

    if path is not None and len(path) > 0:
        if path[-1] != '\\':
            path += '\\'
    else:
        path = ".\\"
    
    path += f"Wallpaper_{datetime.timestamp(datetime.now())}.png"

    try:
        img.save(path)
    except:
        print("Invalid path")
        exit(1)

    #img.show()

    return path

import struct
import ctypes

(subs, sort, nsfw, path) = ParseArgs()
PATH = GetImage(GetRequest(CreateUrl(subs, sort, nsfw)), path)
SPI_SETDESKWALLPAPER = 20

def is_64bit_windows():
    """Check if 64 bit Windows OS"""
    return struct.calcsize('P') * 8 == 64

def changeBG(path):
    """Change background depending on bit size"""
    if is_64bit_windows():
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, PATH, 3)
    else:
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, PATH, 3)

changeBG(PATH)
