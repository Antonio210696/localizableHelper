import os
import re
import subprocess as sp

class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.strings_in_localizable = {}

    def get_localizable_strings_apple(self):
        with open(self.filename,'r') as stringFile:
            buffer = stringFile.read()
            buffer = buffer.replace('\n', '')
            pairs = buffer.split(';')

            for pair in pairs:
                split = pair.split('=')
                if len(split) > 1:
                    self.strings_in_localizable[split[0].rstrip()] = split[1]

    def gather_source_files(self, directory, extensions):
        list_of_sources = []
        for extension in extensions:
            list_of_sources += sp.Popen('find ' + directory + ' -type f -name "*.' + extension + '"', shell=True, stdout=sp.PIPE).\
            stdout.\
            read().\
            decode("utf-8").\
            split('\n')

        return filter(lambda element: element != '', list_of_sources)

    def find_unused_localized_strings(self, directory, source_extensions):
        count = 0
        for string in self.strings_in_localizable:
            list_of_source_files = self.gather_source_files(directory, source_extensions)
            stringCount = 0
            for source in list_of_source_files:
                with open(source, 'r') as source_file:
                    source_text = source_file.read()
                    matches = re.findall(string, source_text)
                    stringCount += len(matches)

            if stringCount == 0:
                print("String " + string + " can be removed")
                count += 1

        print(str(count) + " strings can be removed")
