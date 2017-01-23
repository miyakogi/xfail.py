XFail
=====

.. image:: https://img.shields.io/pypi/v/xfail.svg
        :target: https://pypi.python.org/pypi/xfail

.. image:: https://img.shields.io/pypi/pyversions/xfail.svg
        :target: https://pypi.python.org/pypi/xfail

.. image:: https://img.shields.io/travis/miyakogi/xfail.py.svg
        :target: https://travis-ci.org/miyakogi/xfail.py

.. image:: https://codecov.io/github/miyakogi/xfail.py/coverage.svg?branch=master
    :target: https://codecov.io/github/miyakogi/xfail.py?branch=master


XFail provides a decorator function ``xfail`` to skip expected exceptions.
Similar to unittest.skipIf, but ``xfail`` can specify which exception should be
skipped, and raise if the decorated function is unexpectedly passed (only if
``strict`` is ``True``).

Install
-------

Supported python versions are: 2.7, 3.4, 3.5, 3.6

Can be installed from PyPI by pip::

    pip install xfail

Usage
-----

xfail decorator
^^^^^^^^^^^^^^^

``xfail`` accepts two arguments, ``exceptions`` and ``strict``.

The first argument (``exceptions``) should be an Exception class to skip (Ex.
``Exception``, ``AssertionError``, and so on). If you want to skip multiple
exceptions, use tuple of them, for example, ``@xfail((AssertionError,
ValueError))``.

The second argument ``strict`` should be a boolean. If ``strict`` is ``False``
(by default) and passed unexpectedly, raise ``unittest.SkipTest`` exception,
which will mark the test is skipped. This case is very similar to the function
is decorated by ``uniteest.skip`` function and the test will be counted as
skipped.

 If it is ``True`` and the decorated function did not raise (any of) the
 expected exception(s), ``XPassFailure`` exception would be raised.
 In this case, the test will be counted as fail.

.. code-block:: py

    from xfail import xfail

    @xfail(IndexError)
    def get(l, index):
        return l[index]

    l = [1, 2, 3]
    get(4)  # no error

Also supports multiple exceptions:

.. code-block:: py

    @xfail((IndexError, ValueError))
    def a():
        '''This function passes IndexError and ValueError
        ...

In test script, similar to ``unittest.TestCase.assertRaises``:

.. code-block:: py

    from unittest import TestCase
    from xfail import xfail

    class MyTest(TestCase):
        def test_1(self):
            @xfail(AssertionError)
            def should_raise_error():
                assert False
            a()  # test passes

        def test_2(self):
            @xfail(AssertionError, strict=True)
            def should_raise_error():
                assert True
            a()  # test failes, since this function should raise AssertionError

        # Can be used for test function
        @xfail(AssertionError, strict=True)
        def test_3(self)
            assert False

        # This test will fail
        @xfail(AssertionError, strict=True)
        def test_3(self)
            assert True

For more exapmles, see `test_xfail.py <https://github.com/miyakogi/xfail.py/blob/master/test_xfail.py>`_.
