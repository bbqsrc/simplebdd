import time
import collections

try:
    from termcolor import colored
except:
    def colored(x, *args, **kwargs):
        return x

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

    def run(self):
        self.test.describe_output(self.__doc__)

        for test_name in self._tests:
            test = getattr(self, test_name)
            it = test.__doc__

            try:
                result = test()
                self.test.it_output(it, result)
                self.test.increment(result)
            except Exception as e:
                self.test.it_output(it, e)
                self.test.increment(e)


class Test(metaclass=_TestMeta):
    def run(self):
        self.passes = 0
        self.fails = 0
        self.pending = 0

        self.start = time.time()
        for description_name in self._descriptions:
            description = getattr(self, description_name)(self)
            description.run()

        self.final_output()

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

