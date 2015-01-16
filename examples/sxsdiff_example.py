# -*- coding: utf-8 -*-
import codecs
import sys

import six
from sxsdiff import DiffCalculator
from sxsdiff.generators.github import GitHubStyledGenerator


_BOMDICT = {
    codecs.BOM_UTF8: 'UTF-8',
    codecs.BOM_UTF16_LE: 'UTF-16LE',
    codecs.BOM_UTF16_BE: 'UTF-16BE',
}


def readfile_unicode(filename):
    with open(filename, 'rb') as f:
        raw = f.read()
    for bom, encoding in _BOMDICT.items():
        if raw.startswith(bom):
            raw = raw[len(bom):]
            break
    else:
        encoding = 'utf-8'
    return raw.decode(encoding)


def main(argv):
    if len(argv) != 3:
        print("Usage: %s <oldfile> <newfile>" % argv[0])
        sys.exit(1)
    # Read file content as unicode text
    old = readfile_unicode(argv[1])
    new = readfile_unicode(argv[2])
    stdout = sys.stdout
    # Do special handling for windows and python2
    if six.PY2 and sys.platform == 'win32':
        stdout = codecs.getwriter('utf-8')(sys.stdout)
    sxsdiff_result = DiffCalculator().run(old, new)
    GitHubStyledGenerator(file=stdout).run(sxsdiff_result)


if __name__ == '__main__':
    main(sys.argv)
