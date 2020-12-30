import sys
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

files = []
directory = []
NO_ARGUMENTS = 1
FILE_OR_DIRECTORY_NAME = 1
JACK_FILE = ".jack"


if len(sys.argv) != NO_ARGUMENTS:
    if os.path.isfile(sys.argv[FILE_OR_DIRECTORY_NAME]):
        files.append(sys.argv[FILE_OR_DIRECTORY_NAME])

    if os.path.isdir(sys.argv[FILE_OR_DIRECTORY_NAME]):
        directory.append(sys.argv[FILE_OR_DIRECTORY_NAME])
        for filename in os.listdir(sys.argv[FILE_OR_DIRECTORY_NAME]):
            if filename.endswith(JACK_FILE):
                files.append(filename)

    engine = JackTokenizer()
    writer = CompilationEngine()
    if len(directory) == 0:
        for file in files:
            file2 = engine.parse_line(file)
    else:
        engine.parse_directory(sys.argv[FILE_OR_DIRECTORY_NAME], files)
