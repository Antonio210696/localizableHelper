#!/usr/bin/env python3
from parser import Parser
import sys
if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: python main.py <name of Localizable.strings file> <name of project root> <...extensions to search in...>")
        exit(1)

    parser = Parser(sys.argv[1])
    parser.get_localizable_strings_apple()
    parser.find_unused_localized_strings(sys.argv[2], sys.argv[3:])
