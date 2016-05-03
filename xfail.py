#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps
import logging
import unittest

logger = logging.getLogger(__name__)


class XPassFailure(AssertionError):
    pass


def xfail(exceptions, strict=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            res = None
            err = None
            try:
                res = func(*args, **kwargs)
            except exceptions as e:
                logger.debug('passed with expected failure:', type(e))
            except Exception as e:
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
