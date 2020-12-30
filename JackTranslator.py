from SymbolTable import *

INLINE = "  "
EMPTY = ""
NEWLINE = "\n"
OPERATORS = {"+": "add", "-": "sub", "*": "call Math.multiply 2", "/": "call Math.divide 2",
             "=": "eq", "&gt;" : "gt", "&lt;": "lt", "&amp;": "and", "|": "or"}
KINDS = {"static": "static", "field": "this", "local": "local", "argument": "argument", "pointer": "pointer"}
UNARY_OPERATOR = {"-": "neg", "~": "not"}

class JackTranslator:

    __xmlLines = []
    __lineNumber = 0
    __symbolTable = SymbolTable()
    __className = 0
    __methodName = 0
    __methodKind = 0
    __methodWhileCounter = 0
    __methodIfCounter = 0

    def translate(self, xmlLines, filename):
        self.__xmlLines = xmlLines
        vmLines = []
        self.increaseLineNumberBy(2)
        self.__className = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
        self.increaseLineNumberBy(2)
        while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<classVarDec>":
            self.createClassSymbolTable()
        while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<subroutineDec>":
            self.__methodName = self.__xmlLines[self.__lineNumber + 3].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
            self.__methodKind = self.__xmlLines[self.__lineNumber + 1].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
            self.__methodWhileCounter = 0
            self.__methodIfCounter = 0
            self.createMethodSymbolTable()
            self.compileMethod(vmLines)
            self.increaseLineNumberBy(1)
            self.__symbolTable.clearMethodTable()
            vmLines.append("")
        with open(filename.replace(".xml", ".vm"), "w") as vmFile:
            for line in vmLines:
                vmFile.write("%s\n" % line)


    def increaseLineNumberBy(self, incerement):
        self.__lineNumber += incerement

    def createClassSymbolTable(self):
        self.increaseLineNumberBy(1)
        kind = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
        self.increaseLineNumberBy(1)
        type = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
        self.increaseLineNumberBy(1)
        while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) != "</classVarDec>":
            name = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
            self.__symbolTable.addToClassTable(name, type, kind)
            self.increaseLineNumberBy(2)
        self.increaseLineNumberBy(1)

    def createMethodSymbolTable(self):
        self.increaseLineNumberBy(1)
        if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1] == "method":
            self.__symbolTable.addToMethodTable("this", self.__className, "argument")
        self.increaseLineNumberBy(5)
        while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) != "</parameterList>":
            type = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
            self.increaseLineNumberBy(1)
            name = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
            self.increaseLineNumberBy(1)
            self.__symbolTable.addToMethodTable(name, type, "argument")
            if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[0] == "<symbol>":
                self.increaseLineNumberBy(1)
        self.increaseLineNumberBy(4)
        while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<varDec>":
            self.addVarDecToMethodTable()

    def addVarDecToMethodTable(self):
        self.increaseLineNumberBy(2)
        type = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
        self.increaseLineNumberBy(1)
        while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) != "</varDec>":
            name = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
            self.__symbolTable.addToMethodTable(name, type, "local")
            self.increaseLineNumberBy(2)
        self.increaseLineNumberBy(1)

    def compileMethod(self, vmLines):
        vmLines.append("function " + self.__className + "." + self.__methodName + " " + str(self.__symbolTable.getNumOfLocals()))
        if self.__methodKind == "method":
            vmLines.append("push argument 0")
            vmLines.append("pop pointer 0")
        elif self.__methodKind == "constructor":
            vmLines.append("push constant " + str(self.__symbolTable.getNumOfFields()))
            vmLines.append("call Memory.alloc 1")
            vmLines.append("pop pointer 0")
        self.increaseLineNumberBy(1)
        while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) != "</statements>":
            if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<letStatement>":
                self.compileLetStatements(vmLines)
            if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<doStatement>":
                self.compileDoStatement(vmLines)
            if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<returnStatement>":
                self.compileReturnStatement(vmLines)
            if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<whileStatement>":
                self.compileWhileStatement(vmLines)
            if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<ifStatement>":
                self.compileIfStatement(vmLines)
        self.increaseLineNumberBy(3)

    def compileLetStatements(self, vmLines):
        self.increaseLineNumberBy(2)
        flag = 0
        if self.__xmlLines[self.__lineNumber + 1].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1] == "[":
            flag = 1
            savedIndex = self.__lineNumber
            i = savedIndex
            while True:
                if len(self.__xmlLines[i].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()) == 3:
                    if self.__xmlLines[i].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1] == "=":
                        break
                i += 1
            self.__lineNumber = i - 1
        elif self.__xmlLines[self.__lineNumber + 1].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1] == ".":
            flag = 2
            savedIndex = self.__lineNumber
            self.increaseLineNumberBy(2)
        else:
            popTo = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
        self.increaseLineNumberBy(2)
        self.compileExpression(vmLines, True)
        if flag == 1:
            self.__lineNumber, savedIndex = savedIndex, self.__lineNumber
            self.compileIndex(vmLines, False)
            self.__lineNumber = savedIndex
        elif flag == 2:
            self.__lineNumber, savedIndex = savedIndex, self.__lineNumber
            self.compileSubroutineCall(vmLines, False)
            self.__lineNumber = savedIndex
        else:
            vmLines.append("pop " + KINDS[self.__symbolTable.getKind(popTo)] + " " + str(self.__symbolTable.getCounter(popTo)))
        self.increaseLineNumberBy(3)



    def compileExpression(self, vmLines, assigned):
        self.increaseLineNumberBy(1)
        self.compileTerm(vmLines, assigned)
        while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) != "</expression>":
            if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1] in OPERATORS:
                op = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
                self.increaseLineNumberBy(1)
                self.compileTerm(vmLines, assigned)
                vmLines.append(OPERATORS[op])
            else:
                self.increaseLineNumberBy(1)



    def compileTerm(self, vmLines, assigned):
        self.increaseLineNumberBy(1)
        if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[0] == "<integerConstant>":
            vmLines.append("push constant " + self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1])
            self.increaseLineNumberBy(2)
        elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[0] == "<identifier>":
            if self.__xmlLines[self.__lineNumber + 1].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[0] == "<symbol>":
                if self.__xmlLines[self.__lineNumber + 1].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1] != "[":
                    self.compileSubroutineCall(vmLines, assigned)
                    self.increaseLineNumberBy(1)
                else:
                    self.compileIndex(vmLines, assigned)
                    self.increaseLineNumberBy(1)
            else:  # To be continued
                name = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
                vmLines.append("push " + KINDS[self.__symbolTable.getKind(name)] + " " + str(self.__symbolTable.getCounter(name)))
                self.increaseLineNumberBy(2)
        elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[0] == "<stringConstant>":
            self.compileString(vmLines, assigned)
            self.increaseLineNumberBy(1)
        elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[0] == "<keyword>":
            self.compileKeyword(vmLines, assigned)
            self.increaseLineNumberBy(2)
        elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[0] == "<symbol>":
            if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1] in UNARY_OPERATOR:
                op = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
                self.increaseLineNumberBy(1)
                self.compileTerm(vmLines, assigned)
                vmLines.append(UNARY_OPERATOR[op])
                self.increaseLineNumberBy(1)
            else:
                self.increaseLineNumberBy(1)
                self.compileExpression(vmLines, assigned)
                self.increaseLineNumberBy(3)

    def compileString(self, vmLines, assigned):
        x = len(self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY))
        stringToAppend = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY)[17:x-18]
        stringLen = len(stringToAppend)
        vmLines.append("push constant " + str(stringLen))
        vmLines.append("call String.new 1")
        for i in range(stringLen):
            vmLines.append("push constant " + str(ord(stringToAppend[i])))
            vmLines.append("call String.appendChar 2")
        self.increaseLineNumberBy(1)

    def compileKeyword(self, vmLines, assigned):
        if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1] == "true":
            vmLines.append("push constant 0")
            vmLines.append("not")
        elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1] == "this":
            vmLines.append("push pointer 0")
        else:
            vmLines.append("push constant 0")

    def compileSubroutineCall(self, vmLines, assigned):
        flag = False
        if self.__xmlLines[self.__lineNumber + 1].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1] == "(":
            argsCounter = 1
            vmLines.append("push pointer 0")
            functionName = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
            className = self.__className
        elif self.__symbolTable.searchInTable(self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]) != -1:
            if self.__symbolTable.searchInTable(self.__xmlLines[self.__lineNumber + 2].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]) != 0:
                argsCounter = 1
                vmLines.append("push "+ self.__symbolTable.getKind(self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]) + " " +
                               str(self.__symbolTable.getCounter(self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1])))
                className = self.__symbolTable.getType(self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1])
                self.increaseLineNumberBy(2)
                functionName = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
            else:
                flag = True
                self.compileFieldCall(vmLines, assigned)
        else:
            className = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
            self.increaseLineNumberBy(2)
            functionName = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
            argsCounter = 0
        self.increaseLineNumberBy(3)
        if not flag:
            while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) != "</expressionList>":
                argsCounter += 1
                self.compileExpression(vmLines, not assigned)
                self.increaseLineNumberBy(1)
                if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[0] == "<symbol>":
                    self.increaseLineNumberBy(1)
            self.increaseLineNumberBy(2)
            vmLines.append("call " + className + "." + functionName + " " + str(argsCounter))

    def compileDoStatement(self, vmLines):
        self.increaseLineNumberBy(2)
        self.compileSubroutineCall(vmLines, False)
        vmLines.append("pop temp 0")
        self.increaseLineNumberBy(2)

    def compileReturnStatement(self, vmLines):
        self.increaseLineNumberBy(2)
        if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[0] == "<symbol>":
            vmLines.append("push constant 0")
        else:
            self.compileExpression(vmLines, False)
            self.increaseLineNumberBy(1)
        self.increaseLineNumberBy(2)
        vmLines.append("return")

    def compileWhileStatement(self, vmLines):
        loopCounter = str(self.__methodWhileCounter)
        self.__methodWhileCounter += 1
        self.increaseLineNumberBy(3)
        vmLines.append("label WHILE_" + loopCounter)
        self.compileExpression(vmLines, False)
        vmLines.append("not")
        vmLines.append("if-goto END_WHILE_" + loopCounter)
        self.increaseLineNumberBy(4)
        while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) != "</statements>":
            if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<letStatement>":
                self.compileLetStatements(vmLines)
            elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<doStatement>":
                self.compileDoStatement(vmLines)
            elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<returnStatement>":
                self.compileReturnStatement(vmLines)
            elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<whileStatement>":
                self.compileWhileStatement(vmLines)
            elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<ifStatement>":
                self.compileIfStatement(vmLines)
        vmLines.append("goto WHILE_" + loopCounter)
        vmLines.append("label END_WHILE_" + loopCounter)
        self.increaseLineNumberBy(3)

    def compileIfStatement(self, vmLines):
        ifCounter = str(self.__methodIfCounter)
        self.__methodIfCounter += 1
        self.increaseLineNumberBy(3)
        self.compileExpression(vmLines, False)
        vmLines.append("not")
        vmLines.append("if-goto ELSE_" + ifCounter)
        self.increaseLineNumberBy(4)
        while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) != "</statements>":
            if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<letStatement>":
                self.compileLetStatements(vmLines)
            elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<doStatement>":
                self.compileDoStatement(vmLines)
            elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<returnStatement>":
                self.compileReturnStatement(vmLines)
            elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<whileStatement>":
                self.compileWhileStatement(vmLines)
            elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<ifStatement>":
                self.compileIfStatement(vmLines)
        vmLines.append("goto ENDIF_" + ifCounter)
        vmLines.append("label ELSE_" + ifCounter)
        self.increaseLineNumberBy(2)
        if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[0] == "<keyword>":
            if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1] == "else":
                self.increaseLineNumberBy(3)
                while self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) != "</statements>":
                    if self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<letStatement>":
                        self.compileLetStatements(vmLines)
                    elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<doStatement>":
                        self.compileDoStatement(vmLines)
                    elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<returnStatement>":
                        self.compileReturnStatement(vmLines)
                    elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<whileStatement>":
                        self.compileWhileStatement(vmLines)
                    elif self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY) == "<ifStatement>":
                        self.compileIfStatement(vmLines)
            self.increaseLineNumberBy(2)
        vmLines.append("goto ENDIF_" + ifCounter)
        vmLines.append("label ENDIF_" + ifCounter)
        self.increaseLineNumberBy(1)

    def compileIndex(self, vmLines, assigned):
        varName = self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
        self.increaseLineNumberBy(2)
        self.compileExpression(vmLines, True)
        self.increaseLineNumberBy(2)
        vmLines.append("push " + self.__symbolTable.getKind(varName) + " " + str(self.__symbolTable.getCounter(varName)))
        vmLines.append("add")
        vmLines.append("pop pointer 1")
        if assigned:
            vmLines.append("push that 0")
        else:
            vmLines.append("pop that 0")

    def compileFieldCall(self, vmLines, assigned):
        fieldName = self.__xmlLines[self.__lineNumber + 2].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1]
        vmLines.append("push " + KINDS[self.__symbolTable.getKind(self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1])] + " " +
                       str(self.__symbolTable.getCounter(self.__xmlLines[self.__lineNumber].replace(INLINE, EMPTY).replace(NEWLINE, EMPTY).split()[1])))
        vmLines.append("push " + KINDS[self.__symbolTable.getKind(fieldName)] + " " + str(self.__symbolTable.getCounter(fieldName)))
        vmLines.append("add")
        vmLines.append("pop pointer 1")
        if assigned:
            vmLines.append("push that 0")
        else:
            vmLines.append("pop that 0")
