#!/usr/bin/env python3
from helper import Helper
import sys
if __name__ == '__main__':

    if sys.argv[1] == "--dry-run":
        helper = Helper(sys.argv[2])
        helper.get_localizable_strings_apple()
        helper.find_unused_localized_strings(sys.argv[3], sys.argv[4:])

    elif sys.argv[1] == "--purge":
        helper = Helper(sys.argv[2])
        helper.purge_localizable_file(sys.argv[3], output=sys.argv[4])

    else:
        print("""
        Usage: python main.py --dry-run <name of Localizable.strings file> <name of project root> <...extensions to search in...>
        or
        python main.py --purge <name of strings file> <name of file of strings to be removed> <output filename>
        """)
        exit(1)


