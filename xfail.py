#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
import logging
from typing import Callable, Any, Type  # noqa: F401
import unittest

logger = logging.getLogger(__name__)  # type: logging.Logger


class XPassFailure(AssertionError):
    pass


def xfail(exceptions, strict=False):
    # type: (Type[BaseException], bool) -> Callable[..., Callable[..., Any]]
    def decorator(func):
        # type: (Callable[..., Any]) -> Callable[..., Any]
        @wraps(func)
        def wrapper(*args, **kwargs):
            # type: (...) -> Callable[..., Any]
            res = None
            err = None
            try:
                res = func(*args, **kwargs)
            except exceptions as e:
                logger.debug('passed with expected failure:', type(e))
            except BaseException as e:
                err = e
            else:
                if strict:
                    err = XPassFailure(
                        'Unexpectedly Passed: {}'.format(func.__name__))
                else:
                    logger.debug(
                        'Unexpectedly passed:', func.__name__)
                    err = unittest.SkipTest(
                        'Unexpectedly passed in non-strict mode')
            finally:
                if err is not None:
                    raise err
                else:
                    return res
        return wrapper
    return decorator
