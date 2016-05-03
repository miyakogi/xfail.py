#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import unittest

from xfail import xfail, XPassFailure


class TestXFail(unittest.TestCase):
    def test_passes(self):
        @xfail(AssertionError)
        def a():
            raise AssertionError
        a()

    @unittest.skipIf(sys.version_info < (3, 4),
                     'unittest.TestCase.assertLogs is not supported < 3.4')
    def test_log(self):
        @xfail(AssertionError)
        def a(): raise AssertionError
        with self.assertLogs('xfail', 'DEBUG') as log:
            a()
        self.assertEqual(len(log.records), 1)
        self.assertTrue(log.records[0].msg.startswith('passed with'))

    @unittest.skipIf(sys.version_info < (3, 4),
                     'unittest.TestCase.assertLogs is not supported < 3.4')
    def test_log_xpass(self):
        @xfail(AssertionError)
        def a(): pass
        with self.assertLogs('xfail', 'DEBUG') as log:
            a()
        self.assertEqual(len(log.records), 1)
        self.assertTrue(log.records[0].msg.startswith('Unexpectedly passed'))

    def test_unexpected_failure(self):
        @xfail(ValueError)
        def a():
            raise OSError
        with self.assertRaises(OSError):
            a()

    def test_passes_noerror(self):
        @xfail(AssertionError)
        def a(): pass
        with self.assertRaises(unittest.SkipTest):
            a()

    def test_strict(self):
        @xfail(AssertionError, strict=True)
        def a(): raise AssertionError
        a()

    def test_strict_pass(self):
        @xfail(TypeError, strict=True)
        def a(): pass
        with self.assertRaises(XPassFailure):
            a()

    @xfail(AssertionError, strict=True)
    def test_decorator(self):
        assert False

    @xfail(unittest.SkipTest, strict=True)
    @xfail(AssertionError)
    def test_decorator_pass(self):
        assert True

    @xfail(XPassFailure, strict=True)
    @xfail(AssertionError, strict=True)
    def test_decorator_strict(self):
        assert True

    def test_with_args(self):
        @xfail(ZeroDivisionError)
        def a(i, j=1):
            return i / j
        with self.assertRaises(unittest.SkipTest):
            assert a(4, 2) == 2
        a(1, 0)

    def test_multiple_exception(self):
        @xfail((ZeroDivisionError, IndexError))
        def a(i, j=1):
            [1, 2, 3][i]
            return i / j
        with self.assertRaises(unittest.SkipTest):
            a(1)
        a(3)
        a(1, 0)
        with self.assertRaises(TypeError):
            a()

    def test_multiple_exception_strict(self):
        @xfail((ZeroDivisionError, IndexError), strict=True)
        def a(i, j=1):
            [1, 2, 3][i]
            return i / j
        with self.assertRaises(XPassFailure):
            a(1)
        a(3)
        a(1, 0)
        with self.assertRaises(TypeError):
            a()


if __name__ == '__main__':
    unittest.main()
