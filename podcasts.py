import os.path
from loguru import logger
from datetime import datetime
from feed import get_feed, download_file


def fj_formatter(item):
    file_link = item['link'].split('/')[-1]
    original_file_name, file_extension = os.path.splitext(file_link)

    pub_date = datetime.strptime(item['pubDate'][0:16], '%a, %d %b %Y') if item['pubDate'] else None
    pub_date = pub_date.strftime('%Y-%m-%d') if pub_date else None

    file_name = item['title']
    file_name = file_name.replace(':', ' -')
    file_name = pub_date + ' - ' + file_name + file_extension
    return file_name


PODCAST_FEEDS = [
    ('http://feeds.feedburner.com/filmjunk?format=xml',     # Feed
     '/volume1/media/podcasts/Film Junk Podcast',           # Destionation
     fj_formatter),                                         # Filename formatter
]


if __name__ == '__main__':


    for feed in PODCAST_FEEDS:
        for item in get_feed(feed[0]):
            logger.info('> %s - %s - %s' % (item['pubDate'], item['title'], item['link']))

            formatter = feed[2](item) if feed[1] else None

            download_file(item['link'], destination=feed[1], filename=formatter)