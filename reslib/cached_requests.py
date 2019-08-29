# -*- coding: utf-8 -*-
import os
from functools import lru_cache
from pprint import pprint
import random

import requests


class OverusedToken(Exception):
    pass


class InvalidToken(Exception):
    pass


class NotEnoughTokens(Exception):
    pass


def shuffle(alist):
    """Return a new shuffled list.

    >>> a = ["a", "b", "c", "d", "e"]
    >>> b = shuffle(a)
    >>> a
    ["a", "b", "c", "d", "e"]
    >>> b
    [...]
    """
    blist = alist.copy()
    random.shuffle(blist)
    return blist


def round_coords(*coords, res=0.5, ndigits=1):
    """Return rounded coordinates.

    >>> round_coords(45.4451574, 11.1331589)
    (45.0, 11.0)
    """
    return tuple([(round(coord, ndigits=ndigits) // res) * res for coord in coords])


def g_requests(url, params, headers):
    """Return the text of a GET requests.
    Raise:
        - OverusedToken exception if the status code == 429,
        - InvalidToken exception if the status code == 403,
        - ValueError exception if the status code is not in (420, 403)
    """
    if os.environ.get("DEBUG", "false").lower() == "true":
        print("-" * 80)
        print(f"URL:\n{url}")
        print("HEADERS:")
        pprint(headers)
        print("PARAMS:")
        pprint(params)
        print("-" * 80)
    req = requests.get(url, params=params, headers=headers)
    if req.status_code == 200:
        return req.text
    elif req.status_code == 429:
        # invalid token
        raise OverusedToken
        # go to next token in the list
    elif req.status_code == 403:
        # wrong token
        raise InvalidToken
    else:
        raise ValueError(f"Status code not handled: {req.status_code}")


def get(
    url,
    params,
    tokens=shuffle(os.environ.get("RES_NINJA_TOKENS", "").split(os.pathsep)),
):
    """Return the text of a GET requests.
    The request is cached.
    Use the environmental variable: `LRU_CACHE_MAXSIZE` to set the maximum size
    of the LRU cache, the default value is 2048

    The environmental variable `RES_NINJA_TOKENS` set the tokens available
    to be used.
    The function raise a NotEnoughTokens exception when all the available tokens
    has been used.
    """

    @lru_cache(maxsize=os.environ.get("LRU_CACHE_MAXSIZE", 2048))
    def get_requests(url, **params):
        while len(tokens) > 0:
            token = tokens[0]
            headers = {"Authorization": "Token " + token}
            try:
                return g_requests(url, params, headers)
            except OverusedToken:
                # go to next token in the list
                tokens.pop(0)
            except InvalidToken:
                raise InvalidToken(f"Token {token!r} is not valid, return code: 403")
        # TODO: the list of tokens is finished
        # log the issue somewhere
        raise NotEnoughTokens(
            "Not enough tokens add more tokens to `RES_NINJA_TOKENS` "
            "environmental variable"
        )

    return get_requests(url, **params)


if __name__ == "__main__":
    import doctest

    optionflags = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE | doctest.REPORT_NDIFF
    doctest.testmod(optionflags=optionflags)
