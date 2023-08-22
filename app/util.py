# -*- coding: utf8 -*-

import requests
from datetime import datetime
from urllib.parse import urlparse


def dt_to_str(dt: datetime, fmt='%Y-%m-%d %H:%M:%S') -> str:
    return dt.strftime(fmt)


def ts_to_str(ts: int, fmt='%Y-%m-%d %H:%M:%S') -> str:
    return datetime.fromtimestamp(ts).strftime(fmt)


def get_url_hostname(url: str) -> str:
    return urlparse(url).hostname


def urljoin(url1: str, url2: str) -> str:
    url1 = url1.rstrip('/')
    url2 = url2.lstrip('/')
    return f'{url1}/{url2}'


def http_get(full_url, params=None):
    return requests.get(full_url, params).json()


def http_post(full_url, json_=None):
    return requests.post(full_url, json=json_).json()
