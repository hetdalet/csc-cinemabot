# -*- coding: utf-8 -*-


__all__ = ('fetch',)


import collections
import functools
import os
import random
import re
import sys
import time
import typing
from typing import Dict, List, Union

import bs4
import requests


REQUEST_URL = 'https://www.kinopoisk.ru/index.php'
POSTER = 'https://st.kp.yandex.net/images/film/{}.jpg'
POSTER_BIG = 'https://st.kp.yandex.net/images/film_iphone/iphone360_{}.jpg'
TEST_DATA_PATH = os.path.join(os.path.normpath(sys.path[0]),
                              'test_data',
                              'kinopoisk-plan9-search.html')
DURATION_RE = re.compile(r'.*,\s+([0-9]+)\s+\S*$')
COUNTRY_GEN_RE = re.compile(r'(?P<country>\w+)|(?P<genre>\([\w,. ]+\))')
SEARCH_LIMIT = 3
INFO_FIELDS = ('title',
               'director',
               'year',
               'duration',
               'country',
               'genre',
               'starring',
               'poster',
               'rating')


def fetch(search_srting: str) -> List[Dict]:
    """
    Retrive some film detais by it's title.

    :param search_srting: film title will be passed to external search engine.
        If search_string == 'test' prepared test data will be used
        instead of make actual request to external search engine.
    :return: list of length 3 with dicts contains found films info
    """
    if not search_srting:
        return None
    if search_srting == 'test':
        with open(TEST_DATA_PATH, 'r', encoding='utf-8') as src:
            data = src.read()
    else:
        resp = requests.get(REQUEST_URL, params={'kp_query': search_srting})
        data = resp.text
    soup = bs4.BeautifulSoup(data, 'html.parser')
    result = []
    for e in soup.select('div.element')[:SEARCH_LIMIT]:
        result.append(extract_info(e))

    return check_posters(result)


def extract_info(element: bs4.element.Tag) -> Dict:
    """
    Extracts film details from fetched webpage element.

    There is some dark magic and misterious heuristics under the hood.

    :param element: BeautifulSoup element with film details got
        from search result page
    :return: dict contains film details
    """
    info = dict.fromkeys(INFO_FIELDS)
    getters = {
        'title': lambda e: e.select_one('p.name a').text,
        'director': lambda e: e.select_one('span.gray i.director a').text,
        'year': lambda e: e.select_one('p.name span.year').text,
        'duration': get_duration,
        'poster': get_poster,
        'rating': lambda e: e.select_one('div.rating').text
    }
    for field, getter in getters.items():
        try:
            info[field] = getter(element)
        except (AttributeError, KeyError) as exc:
            log_error(element, exc)

    spans = element.select('span.gray')
    country = None
    genre = None
    try:
        children = spans[1].children
    except (IndexError, AttributeError, TypeError) as exc:
        log_error(element, exc)
    else:
        for tag in children:
            match = COUNTRY_GEN_RE.match(str(tag).strip())
            if match:
                groups = match.groupdict()
                country = country or groups.get('country')
                genre = genre or groups.get('genre')
        if genre:
            genre = genre.strip('()')

    starring = None
    try:
        span = spans[2]
    except IndexError as exc:
        log_error(element, exc)
    else:
        actor_refs = span.find_all(is_actor_ref)
        starring = ', '.join(t.text for t in actor_refs)

    info.update({
        'country':  country,
        'genre':    genre,
        'starring': starring
    })
    return {k: v or None for k, v in info.items()}


def get_duration(element: bs4.element.Tag) -> str:
    orig_tilte = element.select_one('span.gray').text
    return DURATION_RE.search(orig_tilte.strip()).group(1)


def get_poster(element: bs4.element.Tag) -> Union[str, None]:
    film_id = element.select_one('p.name a').attrs['data-id']
    if film_id:
        return POSTER_BIG.format(film_id)
    return None


def is_actor_ref(element: bs4.element.Tag) -> bool:
    """
    Determines if element is link to actor profile.

    :param element: BeautifulSoup element
        from search result page
    :return: True if element is link to actor profile, False otherwise
    """
    return (element.name == 'a' and
            element.has_attr('href') and
            element['href'].startswith('/name'))


def check_posters(info_list: List[Dict]) -> List[Dict]:
    """
    Rmoves not valid poster refs from fetched film details.

    :param info_list: list of dicts with film details
        from search result page
    :return: list of dicts with film details
    """
    for info in info_list:
        resp = requests.get(info['poster'])
        if resp.ok and resp.url.endswith('no-poster.gif'):
            info['poster'] = None
        time.sleep(random.uniform(0.2, 0.6))
    return info_list


def log_error(*args):
    """
    Logger dummy.
    """
    pass
