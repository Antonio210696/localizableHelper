import os
import re
import subprocess as sp
from progressPrint import printProgressBar

class Helper:
    def __init__(self, localizableFilename):
        self.localizableFilename = localizableFilename
        self.strings_in_localizable = {}

    def get_localizable_strings_apple(self):
        with open(self.localizableFilename, 'r') as stringFile:
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
        iteration = 0
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

            iteration += 1
            printProgressBar(iteration, len(self.strings_in_localizable))

        print(str(count) + " strings can be removed")

    def purge_localizable_file(self, removableKeysFilename, output="output.strings"):
        removableKeysFile = open(removableKeysFilename, 'r')
        localizableFile = open(self.localizableFilename, 'r')
        outputFile = open(output, 'w')

        iteration = 0
        totalIterations = sum(1 for line in localizableFile)
        localizableFile.seek(0, 0)
        for line in localizableFile:
            printProgressBar(iteration, totalIterations)
            if not self.is_line_to_be_removed(line, removableKeysFile):
                outputFile.write(line)
            iteration += 1

        removableKeysFile.close()
        outputFile.close()
        localizableFile.close()

    def is_line_to_be_removed(self, line, keys):
        keys.seek(0, 0)
        for key in keys:
            if re.match(key.rstrip(), line) is not None:
                return True

        return False
