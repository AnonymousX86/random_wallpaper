# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from logging import DEBUG, Logger, basicConfig, getLogger
from pathlib import Path
from random import choice
from tempfile import gettempdir, TemporaryDirectory
from typing import Literal
from urllib.request import urlretrieve

from PIL import Image
from requests import get


TIMEFRAMES_VALUES = Literal['hour', 'day', 'week', 'month', 'year', 'all']
TIMEFRAMES_VALUES: tuple[str, ...] = ('hour', 'day', 'week', 'month', 'year', 'all')


def main(log: Logger, save_to: Path, timeframe: TIMEFRAMES_VALUES) -> None:
    log.info(f'Saving to {save_to.resolve()}')
    log.info(f'Searching timeframe {timeframe}')
    base_url = f'https://www.reddit.com/r/wallpaper/top.json?limit=100&t={timeframe}'
    log.debug(f'GET {base_url}')
    res = get(
        base_url,
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'desktop:random_wallpaper:v1.0.0 (by /u/AnonymousX86)'
        }
    )

    if (code := res.status_code) != 200:
        log.critical(f'Error {code}: {res.text}')
        return

    log.debug(res.reason)
    log.debug('Trying to get image URL')
    # Get posts from /r/wallpaper
    posts = res.json().get('data', {}).get('children', [{}])
    # Get random wallpaper URL
    image_url: str = choice(posts).get('data', {}).get('url')

    if not image_url:
        log.critical('Image URL not found')
        return

    file_ext = image_url.split('.')[-1]
    file_path = save_to.joinpath('wallpaper.png')

    with TemporaryDirectory() as temp_dir:
        temp_file = Path(temp_dir, f'wallpaper.{file_ext}')
        log.debug(f'Temp file is {temp_file}')
        # Download the image
        log.debug(f'Downloading {image_url}')
        urlretrieve(image_url, temp_file)
        img = Image.open(temp_file)
        # Convert format if not correct
        if img.mode != 'RGB':
            log.debug('Non RGB format, converting')
            img = img.convert('RGB')
        # Save new file as PNG
        img.save(file_path, 'PNG')
        log.info(f'New file saved as {file_path.resolve()}')


def parse_args() -> tuple[Path, TIMEFRAMES_VALUES]:
    parser = ArgumentParser(description='Saves random image from /r/wallaper')
    parser.add_argument(
        'save_to',
        nargs='?',
        default='.',
        type=str,
        help='Path to directory in which wallapper should be saved',
        metavar='dir'
    )
    parser.add_argument(
        'timeframe',
        nargs='?',
        default='month',
        type=str,
        choices=TIMEFRAMES_VALUES,
        help='Timeframe from which posts should be retrived',
        metavar='timeframe'
    )
    args = parser.parse_args()
    wallpaper_path = Path(args.save_to)

    # Is path valid?
    if not (save_to := wallpaper_path).exists():
        parser.error('Path does not exists')

    # Is path not directory?
    if not save_to.is_dir():
        parser.error('Path has to be directory')

    # Is timeframe valid?
    if (timeframe := args.timeframe) not in TIMEFRAMES_VALUES:
        parser.error('Invalid timeframe')

    return save_to, timeframe


if __name__ == '__main__':
    basicConfig(
        filename=Path(gettempdir(), 'random_wallpaper.log'),
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=DEBUG,
        encoding='UTF-8'
    )
    main(getLogger(), *parse_args())
