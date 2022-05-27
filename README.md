# WallpaperGetter

## What is WallpaperGetter ?

WallpaperGetter is a small console script written in python.
It allows the user to easily fetch an image from Reddit and save it to make it as a wallpaper.

## Installation

Download the python file and install some python libraries using this command :
```bash
pip install argparse user_agent
```

## Usage

```bash
$ python main.py -h
usage: main.py [-h] [--nsfw [{on,off}]] [--path [PATH]] subreddits {top,new,controversial,old,random,best,hot}

positional arguments:
  subreddits            Sub reddits to get image from. Format : [Sub] or [Sub1,Sub2,Sub,...])
  {top,new,controversial,old,random,best,hot}
                        The sort used to get the image

options:
  -h, --help            show this help message and exit
  --nsfw [{on,off}]     Include NSFW images (default = False) : --nsfw {on or off}
  --path [PATH]         Path to save wallpapers : --path {path}
```

Some examples:

```bash
python main.py [wallpaper] random # Get random image from r/wallpaper
python main.py [wallpaper,earthporn,pics] hot # Get hot image from one of the three given subs
python main.py [wallpaper] new --path ./ --nsfw on # Get image from new post, save in current directory, and allowing nsfw posts

```

### Windows

On windows, the python script automatically changes your background, however, an absolute path must be provided to the program (``C:\ ...``).

If you want to change wallpaper on Windows startup, follow this guide: https://stackoverflow.com/questions/51622702/windows-10-run-python-program-in-startup

### Linux

The script returns the path where the image is saved, so you can change your wallpaper by giving it to your wallpaper manager.
