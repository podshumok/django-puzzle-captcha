import sys
from httplib import HTTPException
import urllib2
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from django.core.management.base import NoArgsCommand
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.translation import ugettext as _
from pyquery import PyQuery
from puzzle_captcha.models import Puzzle

root_url = 'http://www.public-domain-image.com'

def create_puzzle_from_url(url):
    img_response = urllib2.urlopen(root_url + url)
    filename = img_response.geturl().split('/')[-1]
    f = SimpleUploadedFile(filename, img_response.read(), img_response.headers.gettype())
    puzzle = Puzzle(image=f)
    try:
        puzzle.save()
        yield _("Puzzle saved")
    except Exception as ex:
        puzzle.delete()
        yield str(ex)

def get_links_log_gen(url, url_list, max_items):
    if max_items==0:
        return
    yield _("Getting images from %s\n") % url
    subcategory_links = []
    resp = urllib2.urlopen(url)
    page = PyQuery(resp.read())
    subcategory_list = page('#public_domain_images_center_middle .albums .album a')
    if subcategory_list:
        for item in subcategory_list:
            link_url = PyQuery(item).attr('href')
            if link_url not in url_list:
                url_list.add(link_url)
                for s in get_links_log_gen(link_url, url_list, max_items-1):
                    yield s
            else:
                yield _("Found duplicate %s\n") % link_url
    elif page('h1 strong img'):
        img_url = page('h1 strong img').attr('src')
        if img_url not in url_list:
            url_list.add(img_url)
            yield _("Found image %s\n") % img_url
            for s in create_puzzle_from_url(img_url): yield s    
        else:
            yield _("Found duplicate %s\n") % img_url

def gen(url, url_list, max_items):
    for s in get_links_log_gen(url, url_list, max_items):
        yield s
    yield _("Done\n")

def get_links(url, url_list, max_items):
    for s in get_links_log_gen(url, url_list, max_items):
        print s,
        sys.stdout.flush()

def main(call=gen, max_items=100):
    resp = None
    while not resp and max_items:
        try:
            resp = urllib2.urlopen(root_url)
        except HTTPException:
            max_items -= 1
    home = PyQuery(resp.read())
    menu = home('.style6 .menu:first')
    menu_links = []
    for item in menu('a'):
        menu_links.append(PyQuery(item).attr('href'))
    url_list = set()
    for menu_item in menu_links:
        return call(menu_item, url_list, max_items)

class Command(NoArgsCommand):
    help = _("Pull all scores for each week record")

    def handle_noargs(self, **options):
        main(get_links)
            
