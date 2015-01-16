# -*- coding: utf-8 -*-
import sys

from sxsdiff import DiffCalculator
from sxsdiff.generators.github import GitHubStyledGenerator


def main(argv):
    if len(argv) != 3:
        print("Usage: %s <oldfile> <newfile>" % argv[0])
        sys.exit(1)
    old_file = argv[1]
    new_file = argv[2]
    with open(old_file) as f:
        old = f.read()
    with open(new_file) as f:
        new = f.read()
    sxsdiff_result = DiffCalculator().run(old, new)
    GitHubStyledGenerator(file=sys.stdout).run(sxsdiff_result)


if __name__ == '__main__':
    main(sys.argv)
