# -*- coding: utf-8 -*-

import bs4
import pytest
from . import scraper


class Case:
    def __init__(self, name, html, expected):
        self.name = name
        self.input = bs4.BeautifulSoup(html, 'html.parser')
        self.expected = expected

    def __str__(self):
        return self.name


FULL_INFO = """
    <div class="element">
    <div class="right">
    <div class="rating" title="5.164 (2 309)">5.2</div>
    <ul class="links">
    <li><a class="js-serp-metrika" data-id="32251" data-type="film" data-url="/film/32251/cast/#actor" href="/film/32251/cast/#actor">актеры</a><s></s></li>
    <li><a class="js-serp-metrika" data-id="32251" data-type="film" data-url="/film/32251/video/" href="/film/32251/video/">трейлеры</a><s></s></li>
    <li><a class="js-serp-metrika" data-id="32251" data-type="film" data-url="/film/32251/stills/" href="/film/32251/stills/">кадры</a><s></s></li>
    <li><a class="js-serp-metrika" data-id="32251" data-type="film" data-url="/film/32251/posters/" href="/film/32251/posters/">постеры</a><s></s></li>
    <li class="inactive">сеансы<s></s></li>
    <li class="inactive">сайты<s></s></li>
    </ul>
    </div>
    <p class="pic"><a class="js-serp-metrika" data-id="32251" data-type="film" data-url="/film/32251" href="/level/1/film/32251/sr/1/"><img alt="План 9 из открытого космоса" class="flap_img" src="https://st.kp.yandex.net/images/spacer.gif" title="План 9 из открытого космоса"/></a></p>
    <div class="info">
    <p class="name"><a class="js-serp-metrika" data-id="32251" data-type="film" data-url="/film/32251" href="/level/1/film/32251/sr/1/">План 9 из открытого космоса</a> <span class="year">1959</span></p>
    <span class="gray">Plan 9 from Outer Space, 79 мин</span>
    <span class="gray">США, <i class="director">реж. <a class="lined js-serp-metrika" data-id="32251" data-type="film" data-url="/name/9136/" href="/name/9136/">Эдвард Д. Вуд мл.</a></i>
    <br/>(ужасы, фантастика)
         </span>
    <span class="gray">
    <a class="lined js-serp-metrika" data-id="32251" data-type="film" data-url="/name/101533/" href="/name/101533/">Грегори Уэлкотт</a>, <a class="lined js-serp-metrika" data-id="32251" data-type="film" data-url="/name/200834/" href="/name/200834/">Мона МакКиннон</a>, <a class="lined js-serp-metrika" data-id="32251" data-type="film" data-url="/film/32251/cast/#actor" href="/film/32251/cast/#actor">...</a>
    </span>
    </div>
    <div class="clear"></div>
    <span class="num">1</span>
    </div>
"""
PARTIAL_INFO = """
    <div class="element">
    <div class="right">
    <ul class="links">
    <li><a class="js-serp-metrika" data-id="1330784" data-type="film" data-url="/film/1330784/cast/#actor" href="/film/1330784/cast/#actor">актеры</a><s></s></li>
    <li class="inactive">трейлеры<s></s></li>
    <li class="inactive">кадры<s></s></li>
    <li class="inactive">постеры<s></s></li>
    <li class="inactive">сеансы<s></s></li>
    <li class="inactive">сайты<s></s></li>
    </ul>
    </div>
    <p class="pic"><a class="js-serp-metrika" data-id="1330784" data-type="film" data-url="/film/1330784" href="/level/1/film/1330784/sr/1/"><img alt="The Falcon" class="flap_img" src="https://st.kp.yandex.net/images/spacer.gif" title="The Falcon"/></a></p>
    <div class="info">
    <p class="name"><a class="js-serp-metrika" data-id="1330784" data-type="film" data-url="/film/1330784" href="/level/1/film/1330784/sr/1/">The Falcon</a> <span class="year">1989</span></p>
    <span class="gray"></span>
    <span class="gray">Тайвань
            <br/>(боевик)
         </span>
    <span class="gray">
    <a class="lined js-serp-metrika" data-id="1330784" data-type="film" data-url="/name/165341/" href="/name/165341/">Эдди Чан</a>, <a class="lined js-serp-metrika" data-id="1330784" data-type="film" data-url="/name/1535951/" href="/name/1535951/">Лью Хсюнг Чанг</a>, <a class="lined js-serp-metrika" data-id="1330784" data-type="film" data-url="/film/1330784/cast/#actor" href="/film/1330784/cast/#actor">...</a>
    </span>
    </div>
    <div class="clear"></div>
    <span class="num">1</span>
    </div>
"""
MIN_INFO = """
    <div class="element">
    <div class="right">
    <ul class="links">
    <li class="inactive">актеры<s></s></li>
    <li class="inactive">трейлеры<s></s></li>
    <li class="inactive">кадры<s></s></li>
    <li class="inactive">постеры<s></s></li>
    <li class="inactive">сеансы<s></s></li>
    <li class="inactive">сайты<s></s></li>
    </ul>
    </div>
    <p class="pic"><a class="js-serp-metrika" data-id="1122168" data-type="series" data-url="/film/1122168" href="/level/1/film/1122168/sr/1/"><img alt="Shaheen" class="flap_img" src="https://st.kp.yandex.net/images/spacer.gif" title="Shaheen"/></a></p>
    <div class="info">
    <p class="name"><a class="js-serp-metrika" data-id="1122168" data-type="series" data-url="/film/1122168" href="/level/1/film/1122168/sr/1/">Shaheen (сериал)</a> <span class="year">1980</span></p>
    <span class="gray"></span>
    <span class="gray">
    <br/>
    </span>
    <span class="gray">
    </span>
    </div>
    <div class="clear"></div>
    <span class="num">5</span>
    </div>
"""

CASES = (
    Case(
        'Plan 9',
        FULL_INFO,
        {
            'title': 'План 9 из открытого космоса',
            'director': 'Эдвард Д. Вуд мл.',
            'year': '1959',
            'duration': '79',
            'country': 'США',
            'genre': 'ужасы, фантастика',
            'starring': 'Грегори Уэлкотт, Мона МакКиннон',
            'poster': 'https://st.kp.yandex.net/images/film_iphone/iphone360_32251.jpg',
            'rating': '5.2'
        }
    ),
    Case(
        'The Falcon',
        PARTIAL_INFO,
        {
            'title': 'The Falcon',
            'director': None,
            'year': '1989',
            'duration': None,
            'country': 'Тайвань',
            'genre': 'боевик',
            'starring': 'Эдди Чан, Лью Хсюнг Чанг',
            'poster': 'https://st.kp.yandex.net/images/film_iphone/iphone360_1330784.jpg',
            'rating': None
        }
    ),
    Case(
        'Shaheen',
        MIN_INFO,
        {
            'title': 'Shaheen (сериал)',
            'director': None,
            'year': '1980',
            'duration': None,
            'country': None,
            'genre': None,
            'starring': None,
            'poster': 'https://st.kp.yandex.net/images/film_iphone/iphone360_1122168.jpg',
            'rating': None
        }
    ),
)


@pytest.mark.parametrize('test_case', CASES, ids=lambda c: str(c))
def test_extract_info(test_case: Case):
    assert scraper.extract_info(test_case.input) == test_case.expected
