from JackTranslator import *

ASM_FILE = "asm"
WRITE_MODE = "w"
POP_COMMAND = "pop"
PUSH_COMMAND = "push"
VM_FILE = "vm"
NUMBER = 2
SEGMENT = 1
ACTION = 0
new_text = []
INLINE = "  "

CLASS_VAR_DEC = {"static", "field"}

TYPES = {"int", "char", "boolean", "void"}

SUBROUTINE_DEC = {"function", "method", "constructor"}

STATEMENTS = {"let", "if", "while", "do", "return"}

KEYWORDS = {"class", "constructor", "function", "method", "field", "static",
            "var", "int", "char", "boolean", "void", "true", "false", "null",
            "this", "let", "do", "if", "else", "while", "return"}

BINARY_OPERATORS = {"+", "-", "*", "/", "&", "|", "<", ">", "="}

UNARY_OPERATORS = {"-", "~"}

SYMBOLS = {'{', '}', '(',')', '[', ']' '.', ',', ';', '+', '-', '*', '/'
                                                                     '&', '|', '<', '>', '=', '~'}

SPECIAL_SYMBOLS = {'<': "&lt;", '>': "&gt;", '"': "&quot;", '&': "&amp;"}


class CompilationEngine:
    """
    The CodeWriter class uses for writing the assembly code that implements
    the parsed commands.
    """

    def write_file(self, tokens, file_names):
        """
        The function gets a file name and a text and
        translates the content of the file and writes
        it in a new file.

        :param tokens: string
        :param file_name: string
        """
        new_line = ""
        function_name = ""
        xmlLines = []
        self.write_class(xmlLines, tokens)
        x = JackTranslator()
        x.translate(xmlLines, file_names[0])

    def write_term(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * (tabs) + "<term>\n")
        if tokens[i][0].isdigit():
            xmlLines.append(INLINE * (tabs + 1) + "<integerConstant> " + tokens[i] + " </integerConstant>\n")
            i += 1
        elif tokens[i][0] == '"':
            xmlLines.append(
                INLINE * (tabs + 1) + "<stringConstant> " + tokens[i][1:len(tokens[i]) - 1] + " </stringConstant>\n")
            i += 1
        elif tokens[i] in KEYWORDS:
            xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
            i += 1
        elif tokens[i][0].isalpha() or tokens[i][0] == "_":
            if tokens[i+1] == "(":
                i = self.write_subroutineCall(xmlLines, tokens, i, tabs)
            elif tokens[i+1] == ".":
                if tokens[i+3] == "(":
                    i = self.write_subroutineCall(xmlLines, tokens, i, tabs)
                else:
                    xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
                    i += 1
                    xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
                    i+= 1
                    xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
                    i += 1
            else:
                xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
                i += 1
                if tokens[i] == "[":
                    xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
                    i = self.write_expression(xmlLines, tokens, i + 1, tabs + 1)
                    xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
                    i += 1
        elif tokens[i][0] == "(":
            xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            i = self.write_expression(xmlLines, tokens, i + 1, tabs + 1)
            xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            i += 1
        elif tokens[i] in UNARY_OPERATORS:
            xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            i = self.write_term(xmlLines, tokens, i + 1, tabs + 1)
        xmlLines.append(INLINE * (tabs) + "</term>\n")
        return i

    def write_expression(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<expression>\n")
        i = self.write_term(xmlLines, tokens, i, tabs + 1)
        while tokens[i] in BINARY_OPERATORS:
            if tokens[i] in SPECIAL_SYMBOLS:
                xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + SPECIAL_SYMBOLS[tokens[i]] + " </symbol>\n")
            else:
                xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            i += 1
            i = self.write_term(xmlLines, tokens, i, tabs + 1)

        xmlLines.append(INLINE * tabs + "</expression>\n")
        return i

    def write_class(self, xmlLines, tokens):
        xmlLines.append("<class>\n")
        xmlLines.append(INLINE + "<keyword> class </keyword>\n")
        xmlLines.append(INLINE + "<identifier> " + tokens[1] + " </identifier>\n")
        xmlLines.append(INLINE + "<symbol> { </symbol>\n")
        i = 3
        while tokens[i] != "}":
            while tokens[i] in CLASS_VAR_DEC:
                i = self.write_classVarDec(xmlLines, tokens, i, 1)
            while tokens[i] in SUBROUTINE_DEC:
                i = self.write_subroutineDec(xmlLines, tokens, i, 1)
        xmlLines.append(INLINE + "<symbol> } </symbol>\n")
        xmlLines.append("</class>\n")

    def write_classVarDec(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<classVarDec>\n")
        while tokens[i] != ";":
            # write fields
            if tokens[i] in CLASS_VAR_DEC or tokens[i] in TYPES:
                xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
            elif tokens[i] in SYMBOLS:
                xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            else:
                xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
            i += 1
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        xmlLines.append(INLINE * tabs + "</classVarDec>\n")
        return i

    def write_subroutineDec(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<subroutineDec>\n")
        xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
        i += 1
        if tokens[i-1] == "constructor":
            xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
        elif tokens[i] in TYPES:
            xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
        else:
            xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
        i += 1
        xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
        i += 1
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        i = self.write_parameterList(xmlLines, tokens, i, tabs + 1)
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        i = self.write_subroutineBody(xmlLines, tokens, i, tabs + 1)
        xmlLines.append(INLINE * tabs + "</subroutineDec>\n")
        return i

    def write_parameterList(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<parameterList>\n")
        while tokens[i] != ")":
            if tokens[i] in SYMBOLS:
                xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            elif tokens[i] in TYPES:
                xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
            else:
                xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
            i += 1
        xmlLines.append(INLINE * tabs + "</parameterList>\n")
        return i

    def write_subroutineBody(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<subroutineBody>\n")
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        while tokens[i] == "var":
            i = self.write_varDec(xmlLines, tokens, i, tabs + 1)
        i = self.write_statements(xmlLines, tokens, i, tabs + 1)
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        xmlLines.append(INLINE * tabs + "</subroutineBody>\n")
        return i

    def write_varDec(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<varDec>\n")
        xmlLines.append(INLINE * (tabs + 1) + "<keyword> var </keyword>\n")
        i += 1
        while tokens[i] != ";":
            if tokens[i] == "var":
                xmlLines.append(INLINE * tabs + "</varDec>\n")
                xmlLines.append(INLINE * tabs + "<varDec>\n")
                xmlLines.append(INLINE * (tabs + 1) + "<keyword> var </keyword>\n")
            elif tokens[i] in SYMBOLS:
                xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            elif tokens[i] in TYPES:
                xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
            else:
                xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
            i += 1
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        xmlLines.append(INLINE * tabs + "</varDec>\n")
        return i

    def write_statements(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<statements>\n")
        while tokens[i] in STATEMENTS:
            if tokens[i] == "let":
                i = self.write_letStatement(xmlLines, tokens, i, tabs + 1)
            elif tokens[i] == "if":
                i = self.write_ifStatement(xmlLines, tokens, i, tabs + 1)
            elif tokens[i] == "while":
                i = self.write_whileStatement(xmlLines, tokens, i, tabs + 1)
            elif tokens[i] == "return":
                i = self.write_returnStatement(xmlLines, tokens, i, tabs + 1)
            elif tokens[i] == "do":
                i = self.write_doStatement(xmlLines, tokens, i, tabs + 1)
        xmlLines.append(INLINE * tabs + "</statements>\n")
        return i

    def write_letStatement(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<letStatement>\n")
        xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
        i += 1
        xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
        i += 1
        if (tokens[i] == "["):
            xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            i = self.write_expression(xmlLines, tokens, i + 1, tabs + 1)
            xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            i += 1
        if tokens[i] == ".":
            xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            i += 1
            xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </symbol>\n")
            i += 1
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i = self.write_expression(xmlLines, tokens, i + 1, tabs + 1)
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        xmlLines.append(INLINE * tabs + "</letStatement>\n")
        return i

    def write_ifStatement(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<ifStatement>\n")
        xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
        i += 1
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        i = self.write_expression(xmlLines, tokens, i, tabs + 1)
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i = self.write_statements(xmlLines, tokens, i + 1, tabs + 1)
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        if tokens[i] == "else":
            xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
            i += 1
            xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            i = self.write_statements(xmlLines, tokens, i + 1, tabs + 1)
            xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            i += 1
        xmlLines.append(INLINE * tabs + "</ifStatement>\n")
        return i

    def write_whileStatement(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<whileStatement>\n")
        xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
        i += 1
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        i = self.write_expression(xmlLines, tokens, i, tabs + 1)
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i = self.write_statements(xmlLines, tokens, i + 1, tabs + 1)
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        xmlLines.append(INLINE * tabs + "</whileStatement>\n")
        return i

    def write_returnStatement(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<returnStatement>\n")
        xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
        i += 1
        if (tokens[i] != ";"):
            i = self.write_expression(xmlLines, tokens, i, tabs + 1)
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        xmlLines.append(INLINE * tabs + "</returnStatement>\n")
        return i

    def write_doStatement(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<doStatement>\n")
        xmlLines.append(INLINE * (tabs + 1) + "<keyword> " + tokens[i] + " </keyword>\n")
        i = self.write_subroutineCall(xmlLines, tokens, i + 1, tabs)
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        xmlLines.append(INLINE * tabs + "</doStatement>\n")
        return i

    def write_subroutineCall(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
        i += 1
        if tokens[i] == ".":
            xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
            i += 1
            xmlLines.append(INLINE * (tabs + 1) + "<identifier> " + tokens[i] + " </identifier>\n")
            i += 1
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i = self.write_expressionList(xmlLines, tokens, i + 1, tabs + 1)
        xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
        i += 1
        return i

    def write_expressionList(self, xmlLines, tokens, i, tabs):
        xmlLines.append(INLINE * tabs + "<expressionList>\n")
        if tokens[i] != ")":
            i = self.write_expression(xmlLines, tokens, i, tabs + 1)
            while tokens[i] == ",":
                xmlLines.append(INLINE * (tabs + 1) + "<symbol> " + tokens[i] + " </symbol>\n")
                i = self.write_expression(xmlLines, tokens, i + 1, tabs + 1)
        xmlLines.append(INLINE * tabs + "</expressionList>\n")
        return i

