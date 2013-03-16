import time
import collections
import traceback
import os
import sys

from threading import Thread
from functools import wraps, partial
try:
    from termcolor import colored
except:
    def colored(x, *args, **kwargs):
        return x


class TestThread(Thread):
    def __init__(self, context, func):
        Thread.__init__(self)
        self.context = context
        self.func = partial(func, context)
        self.func.__doc__ = func.__doc__

    def run(self):
        self.context.run_test(self.func)


def async(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        thread = TestThread(self, func)
        self._threads.append(thread)
        return thread
    setattr(wrapper, 'async', True)
    return wrapper


class _DescMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    def __new__(cls, name, bases, classdict):
        result = type.__new__(cls, name, bases, dict(classdict))
        result._tests = tuple([x for x in tuple(classdict) if x.startswith("it_")])
        return result


class _TestMeta(type):
    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    def __new__(cls, name, bases, classdict):
        result = type.__new__(cls, name, bases, dict(classdict))
        result._descriptions = tuple([x for x in tuple(classdict) if isinstance(classdict[x], Description.__class__)])
        return result


class Description(metaclass=_DescMeta):
    def __init__(self, test):
        self.test = test

    def run_test(self, test):
        output = self.output

        before_each = getattr(self, 'before_each_test', None)
        after_each = getattr(self, 'after_each_test', None)
        it = test.__doc__

        try:
            if before_each: before_each()
            result = test()
            if after_each: after_each()

            output.it(it, result)
            self.test.increment(result)
        except Exception as e:
            output.it(it, e)
            self.test.increment(e)

    def run(self, output):
        self.output = output
        self._threads = []

        output.describe(self.__doc__)

        before_all = getattr(self, 'before_tests', None)
        after_all = getattr(self, 'after_tests', None)

        if before_all: before_all()

        for test_name in self._tests:
            test = getattr(self, test_name)
            if getattr(test, 'async', False):
                test().start()
            else:
                self.run_test(test)

        for thread in self._threads:
            thread.join()

        if after_all: after_all()


class Test(metaclass=_TestMeta):
    def run(self, output):
        self.passes = 0
        self.fails = 0
        self.pending = 0

        start = time.time()

        before_each = getattr(self, 'before_each_test', None)
        after_each = getattr(self, 'after_each_test', None)
        before_all = getattr(self, 'before_tests', None)
        after_all = getattr(self, 'after_tests', None)

        if before_all: before_all()

        for description_name in self._descriptions:
            description = getattr(self, description_name)(self)
            if before_each: before_each()
            description.run(output)
            if after_each: after_each()

        if after_all: after_all()

        ts = time.time() - start
        output.final(self.passes, self.fails, self.pending, ts)

    def increment(self, result):
        if result == True:
            self.passes += 1
        elif result == False or isinstance(result, Exception):
            self.fails += 1
        else:
            self.pending += 1

    def describe_output(self, desc):
        print("\n" + desc)

    def it_output(self, it, result):
        if result == True:
            print("  ✓ %s" % colored(it, 'green'))
        elif result == False:
            print("  × %s" % colored(it, 'red'))
        elif isinstance(result, Exception):
            print("  × %s" % (colored("%s [%s]" % (it, result), 'red')))
        else:
            print("  - %s" % colored(it, 'cyan'))

    def final_output(self):
        print()
        ts = colored("(%.3fs)" % (time.time() - self.start), attrs=['bold'])

        if self.fails > 0:
            print("× %s » %s passed • %s failed • %s pending %s" %
                    (colored("FAIL", "red"), self.passes, self.fails, self.pending, ts))
        else:
            print("✓ %s » %s passed • %s pending %s" %
                    (colored("PASS", "green"), self.passes, self.pending, ts))


class Output:
    def describe(self, desc):
        print("\n" + desc)

    def it(self, it, result):
        if result == True:
            print("  ✓ %s" % colored(it, 'green'))
        elif result == False:
            print("  × %s" % colored(it, 'red'))
        elif isinstance(result, Exception):
            tb = traceback.extract_tb(sys.exc_info()[2])
            x = "\n".join(["      {0}:{1}#{2}\n        {3}".format(*x) for x in tb])
            print("  × %s" % (colored("%s [%s (%s)]\n%s" %
                (it, result, type(result).__name__, x), 'red')))
        else:
            print("  - %s" % colored(it, 'cyan'))

    def final(self, passes, fails, pending, ts):
        ts = colored("(%.3fs)" % ts, attrs=['bold'])

        if fails > 0:
            print("\n× %s » %s passed • %s failed • %s pending %s" %
                    (colored("FAIL", "red"), passes, fails, pending, ts))
        else:
            print("\n✓ %s » %s passed • %s pending %s" %
                    (colored("PASS", "green"), passes, pending, ts))

class HTMLOutput(Output):
    def describe(self, desc):
        print("<h2>%s</h2>" % desc)

    def it(self, it, result):
        if result == True:
            print("<p>  ✓ %s</p>" % it)
        elif result == False:
            print("<p>  × %s</p>" % it)
        elif isinstance(result, Exception):
            print("<p>  × %s [%s]</p>" % (it, result))
        else:
            print("<p>  - %s</p>" % it)

    def final(self, passes, fails, pending, ts):
        ts = "(%.3fs)" % ts

        if fails > 0:
            print("<p>× %s » %s passed • %s failed • %s pending %s</p>" %
                    ("FAIL", passes, fails, pending, ts))
        else:
            print("<p>✓ %s » %s passed • %s pending %s</p>" %
                    ("PASS", passes, pending, ts))

def import_path(fullpath):
    """
    Import a file with full path specification. Allows one to
    import from anywhere, something __import__ does not do.
    """
    import os, sys, imp
    path, filename = os.path.split(os.path.realpath(fullpath))
    filename, ext = os.path.splitext(filename)
    sys.path.append(path)
    module = __import__(filename)
    imp.reload(module) # Might be out of date
    del sys.path[-1]
    return module
