import argparse
import glob
import os
import sys

from simplebdd import Test


def imports_by_path(path):
    fpath, fn = os.path.split(path)
    if fn.endswith('.py'):
        path = fpath
        fns = [fn[:-3]]
    else:
        fns = [os.path.basename(x) for x in glob.glob(os.path.join(path, '*.py'))]
        
    sys.path.append(path)
    return [__import__(fn[:-3]) for fn in fns]


def cli():
    p = argparse.ArgumentParser()
    p.description = "A simple implementation of a behaviour-driven development style testing framework."
    p.add_argument("test", nargs=1, help="Test file or directory")
    args = p.parse_args()
    modules = imports_by_path(args.test[0])
    for module in modules:
        tests = []
        
        for x in dir(module):
            y = getattr(module, x)
            try:
                if Test in y.__bases__:
                    tests.append(y)
            except:
                pass
        
        for test in tests:
            test().run()

if __name__ == "__main__":
    cli()
