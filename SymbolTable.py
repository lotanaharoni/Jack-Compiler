class SymbolTable:

    __classTable = {}
    __methodTable = {}
    __fieldCounter = 0
    __staticCounter = 0
    __argCounter = 0
    __localCounter = 0

    def addToMethodTable(self, name, type, kind):
        if name == "this":
            self.__methodTable[name] = [type, "pointer", self.__argCounter]
            self.__argCounter += 1
        elif name not in self.__methodTable:
            if kind == "argument":
                self.__methodTable[name] = [type, kind, self.__argCounter]
                self.__argCounter += 1
            else:
                self.__methodTable[name] = [type, kind, self.__localCounter]
                self.__localCounter += 1

    def addToClassTable(self, name, type, kind):
        if name not in self.__classTable:
            if kind == "field":
                self.__classTable[name] = [type, "field", self.__fieldCounter]
                self.__fieldCounter += 1
            else:
                self.__classTable[name] = [type, kind, self.__staticCounter]
                self.__staticCounter += 1

    def clearMethodTable(self):
        self.__methodTable.clear()
        self.__argCounter = 0
        self.__localCounter = 0

    def clearClassTable(self):
        self.__classTable.clear()
        self.__fieldCounter = 0
        self.__staticCounter = 0

    def searchInTable(self, name):
        if name in self.__methodTable:
            return 1
        if name in self.__classTable:
            return 0
        return -1

    def getKind(self, name):
        if name in self.__methodTable:
            return self.__methodTable[name][1]
        elif name in self.__classTable:
            return self.__classTable[name][1]

    def getType(self, name):
        if name in self.__methodTable:
            return self.__methodTable[name][0]
        elif name in self.__classTable:
            return self.__classTable[name][0]

    def getCounter(self, name):
        if name in self.__methodTable:
            return self.__methodTable[name][2]
        elif name in self.__classTable:
            return self.__classTable[name][2]

    def printTable(self):
        print("name\ttype\tkind\t#")
        for name in self.__classTable:
            print(name + "\t", self.__classTable[name])
        print()
        for name in self.__methodTable:
            print(name + "\t", self.__methodTable[name])

    def getNumOfLocals(self):
        localCounter = 0
        for name in self.__methodTable:
            if self.__methodTable[name][1] == "local":
                localCounter += 1
        return localCounter

    def getNumOfFields(self):
        fieldCounter = 0
        for name in self.__classTable:
            if self.__classTable[name][1] == "field":
                fieldCounter += 1
        return fieldCounter
