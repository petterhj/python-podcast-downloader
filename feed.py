# Imports
import os.path
import xmltodict
import requests
from loguru import logger
from tqdm import tqdm


def get_feed(url):
    logger.debug('Parsing feed, url=%s' % (url))

    feed = xmltodict.parse(requests.get(url).text)
    
    items = feed['rss']['channel']['item']
    # for item in feed['rss']['channel']['item']:
    #     items = 

    logger.debug('Found %d items in feed' % (len(items)))

    return items


def download_file(url, filename=False):
    # Destination
    destination_file = filename if filename else url.split('/')[-1]

    if os.path.exists(destination_file):
        logger.warning('> Skipped: Destination file "%s" already exists' % (destination_file))
        return

    logger.debug('> Downloading %s >>> "%s"' % (url, destination_file))

    r = requests.get(url, stream=True)
    
    file_size = int(r.headers['Content-Length'])
    chunk = 1
    chunk_size=1024
    num_bars = int(file_size / chunk_size)

    with open(destination_file, 'wb') as fp:
        for chunk in tqdm(r.iter_content(chunk_size=chunk_size), **{
                'total': num_bars,
                'unit': 'KB',
                'desc': destination_file,
                'leave': False}):
            fp.write(chunk)

    logger.success('> File saved to %s (%d)' % (destination_file, file_size))


    