from threading import Thread
from tasks.mgn_scraper import get_images

def start_image_scrape(sid, image_ids):
    thread = Thread(target=get_images, args=(sid, image_ids))
    thread.start()