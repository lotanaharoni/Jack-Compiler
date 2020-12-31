import os
from CompilationEngine import CompilationEngine
COMMENT = "//"
MULTILINES_COMMENT_PREFIX = "/*"
MULTILINES_COMMENT_SUFFIX = "*/"
FOLDER = "/"
READ_MODE = "r"
EMPTY = " "
WRITE_MODE = "w"
JACK_FILE = ".jack"
XML_FILE = ".xml"
SPACES = ["\t", "\n", "\r"]
SEGMENT = 1
ACTION = 0
SYMBOLS = {'{', '}', '(',')', '[', ']', '.', ',', ';', '+', '-', '*', '/',
           '&', '|', '<', '>', '=', '~'}

class JackTokenizer:
    """
    The Parser class uses to parses each VM command into it's lexical elements.
    It uses the CodeWriter class.
    """

    files = []


    def parse_line(self, file_name):
        """
        The function gets a file's name, it reads it's content and write it
        in a file with the same name, but in other type: "asm" instead of "vm".

        :param file_name: string
        """
        MULTILINES_COMMENT_FLAG = False
        self.files = []
        new_names = []
        word = ""
        new_name = file_name.replace(JACK_FILE, XML_FILE)
        new_names.append(new_name)
        with open(file_name, READ_MODE) as f:
            for line in f:
                if not MULTILINES_COMMENT_FLAG:
                    for c in SPACES:
                        line = line.replace(c, EMPTY)
                    if COMMENT in line:
                        index_comment = line.find(COMMENT)
                        index_start_string = line.find('"')
                        index_end_string = line.find('"', index_start_string+1)
                        if not(index_comment > index_start_string and index_comment < index_end_string):
                            line = line[:index_comment]
                    if MULTILINES_COMMENT_PREFIX in line:
                        index_comment = line.find(MULTILINES_COMMENT_PREFIX)
                        index_comment_end = len(line)
                        index_start_string = line.find('"')
                        index_end_string = line.find('"', index_start_string + 1)
                        if not(index_comment > index_start_string and index_comment < index_end_string):
                            if MULTILINES_COMMENT_SUFFIX not in line:
                                MULTILINES_COMMENT_FLAG = True
                            else:
                                index_comment_end = line.find(MULTILINES_COMMENT_SUFFIX)
                            line = line[:index_comment] + " " + line[index_comment_end+2:]
                    if line != EMPTY and line != SPACES[1]:
                        temp_x = list(line)
                        flag = False
                        digit_flag = False
                        for c in temp_x:
                            if c == '"' or flag:
                                word += c
                                if c == '"' and flag:
                                    flag = False
                                    self.files.append(word)
                                    word = ""
                                else:
                                    flag = True
                            elif c == " " and word != "":
                                self.files.append(word)
                                word = ""
                                digit_flag = False
                            elif c.isdigit():
                                word += c
                                digit_flag = True
                            elif c in SYMBOLS:
                                if word != "":
                                    self.files.append(word)
                                self.files.append(c)
                                word = ""
                                digit_flag = False
                            else:
                                if c != " ":
                                    word += c
                elif MULTILINES_COMMENT_SUFFIX in line:
                    MULTILINES_COMMENT_FLAG = False
                    index_comment = line.find(MULTILINES_COMMENT_SUFFIX)
                    line = line[index_comment+2:]
                    line = line.lstrip()
                    if line != EMPTY and line != SPACES[1] and line != "\n":
                        temp_x = list(line)
                        flag = False
                        digit_flag = False
                        for c in temp_x:
                            if c == '"' or flag:
                                word += c
                                if c == '"' and flag:
                                    flag = False
                                    self.files.append(word)
                                    word = ""
                                else:
                                    flag = True
                            elif c == " " and word != "":
                                self.files.append(word)
                                word = ""
                                digit_flag = False
                            elif c.isdigit():
                                word += c
                                digit_flag = True
                            elif c in SYMBOLS:
                                if digit_flag and c == ".":
                                    word += c
                                    continue
                                if word != "":
                                    self.files.append(word)
                                self.files.append(c)
                                word = ""
                                digit_flag = False
                            else:
                                if c != " ":
                                    word += c
        f.close()
        writer = CompilationEngine()
        writer.write_file(self.files, new_names)

    def parse_directory(self, directory_name, file_names):
        """
        The function gets a file's name, it reads it's content and write it
        in a file with the same name, but in other type: "asm" instead of "vm".

        :param file_name: string
        """
        files = []
        for name in file_names:
            self.parse_line(directory_name + "/" + name)
