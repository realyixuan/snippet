"""

reference:
    https://aosabook.org/en/500L/a-python-interpreter-written-in-python.html
    https://compilerbook.com/


the procedures:

    lexer -> parser -> ast -> compiler -> virtual machine

This is a tiny interpreter for the language:
    - single-digit name and single-digit number
    - only three lindes code
    - two operators: - or +
    - the first line and second line is:
        - asignment statement
        like: 
            a = 1 or
            a = 1 + 1
    - third line of code is expression
    - result of third line of code will be automatically printed

it's like:
    a = 4;
    b = a - 3;
    a + b;

"""

OP_LOAD_CONST   = (0).to_bytes(1, 'big')
OP_STORE_NAME   = (1).to_bytes(1, 'big')
OP_LOAD_NAME    = (2).to_bytes(1, 'big')
OP_ADD          = (3).to_bytes(1, 'big')
OP_SUBTRACT     = (4).to_bytes(1, 'big')
OP_PRINT        = (5).to_bytes(1, 'big')


class Statement:
    def __init__(self, type, left, right):
        self.type = type
        self.left = left
        self.right = right

class Token:
    def __init__(self, letter):
        if letter.isdigit():
            self.type = 'number'
            self.val = int(letter)
        else:
            self.type = 'name'
            self.val = letter


class Lexer:
    def __init__(self, input):
        self.input = input
        self.idx = 0

    def read_char(self):
        self.idx += 1
        return self.input[self.idx-1]

    def read_token(self):
        while (ch := self.read_char()).isspace(): pass
        return Token(ch)


class Parser:
    def __init__(self):
        self.l = None

    def parsing(self, input):
        self.l = Lexer(input)

        return (
            self.parsing_statement1_or_2(),
            self.parsing_statement1_or_2(),
            self.parsing_statement3(),
        )

    def parsing_statement1_or_2(self):
        tok1 = self.l.read_token()

        tok2 = self.l.read_token()
        if tok2.val != '=':
            raise Exception("wrong syntax")

        tok3 = self.l.read_token()

        tok4 = self.l.read_token()
        if tok4.val != ';':
            tok5 = self.l.read_token()
            self.l.read_token()
            if tok4.val == '+':
                right = Statement('add', tok3, tok5)
            elif tok4.val == '-':
                right = Statement('subtract', tok3, tok5)
        else:
            right = tok3
        return Statement('assign', tok1, right)

    def parsing_statement3(self):
        tok1 = self.l.read_token()
        tok2 = self.l.read_token()
        tok3 = self.l.read_token()
        if tok2.val == '+':
            return Statement('add', tok1, tok3)
        elif tok2.val == '-':
            return Statement('subtract', tok1, tok3)
            

parser = Parser()


class Codes:
    def __init__(self, instructions, constants, names):
        self.instructions: bytes = instructions
        self.constants: int = constants
        self.names: str = names


class Compiler:
    def __init__(self):
        self.instructions: bytes = []
        self.constants: int = []
        self.names: str = []

    def compile(self, input):
        stmts = parser.parsing(input)
        for stmt in stmts:
            self._compile(stmt)
        self.emit_PRINT()

        return Codes(
            self.instructions,
            self.constants,
            self.names,
        )

    def _compile(self, target):
        if type(target) == Statement:
            if target.type == 'assign':
                self._compile(target.right)
                self.emit_STORE_NAME(target.left.val)
            elif target.type == 'add':
                self._compile(target.left)
                self._compile(target.right)
                self.emit_ADD()
            elif target.type == 'subtract':
                self._compile(target.left)
                self._compile(target.right)
                self.emit_SUBTRACT()
        elif type(target) == Token:
            if target.type == 'number':
                self.emit_LOAD_CONST(target.val)
            elif target.type == 'name':
                self.emit_LOAD_NAME(target.val)

    def emit_LOAD_CONST(self, val):
        self.constants.append(val)
        self.instructions.append(OP_LOAD_CONST)
        self.instructions.append((len(self.constants)-1).to_bytes(1, 'big'))

    def emit_LOAD_NAME(self, val):
        self.names.append(val)
        self.instructions.append(OP_LOAD_NAME)
        self.instructions.append((len(self.names)-1).to_bytes(1, 'big'))

    def emit_STORE_NAME(self, val):
        self.names.append(val)
        self.instructions.append(OP_STORE_NAME)
        self.instructions.append((len(self.names) - 1).to_bytes(1, 'big'))

    def emit_ADD(self):
        self.instructions.append(OP_ADD)

    def emit_SUBTRACT(self):
        self.instructions.append(OP_SUBTRACT)

    def emit_PRINT(self):
        self.instructions.append(OP_PRINT)


compiler = Compiler()


class VM:
    def __init__(self):
        self.env = {}
        self.stack = []

    def run(self, codes):
        self.codes = codes
        self.ip = 0
        while self.ip < len(codes.instructions):
            if codes.instructions[self.ip] == OP_LOAD_CONST:
                self.run_LOAD_CONST()
            elif codes.instructions[self.ip] == OP_STORE_NAME:
                self.run_STORE_NAME()
            elif codes.instructions[self.ip] == OP_LOAD_NAME:
                self.run_LOAD_NAME()
            elif codes.instructions[self.ip] == OP_ADD:
                self.run_ADD()
            elif codes.instructions[self.ip] == OP_SUBTRACT:
                self.run_SUBTRACT()
            elif codes.instructions[self.ip] == OP_PRINT:
                self.run_PRINT()

    def run_LOAD_CONST(self):
        argint = self.codes.instructions[self.ip+1]
        self.ip += 2
        arg = self.codes.constants[int.from_bytes(argint, 'big')]
        self.stack.append(arg)

    def run_STORE_NAME(self):
        argint = self.codes.instructions[self.ip+1]
        self.ip += 2
        arg = self.codes.names[int.from_bytes(argint, 'big')]
        self.env[arg] = self.stack.pop()

    def run_LOAD_NAME(self):
        argint = self.codes.instructions[self.ip+1]
        self.ip += 2
        arg = self.codes.names[int.from_bytes(argint, 'big')]
        self.stack.append(self.env[arg])

    def run_ADD(self):
        self.ip += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(left + right)

    def run_SUBTRACT(self):
        self.ip += 1
        right = self.stack.pop()
        left = self.stack.pop()
        self.stack.append(left - right)

    def run_PRINT(self):
        self.ip += 1
        item = self.stack.pop()
        print(item)


vm = VM()


def main(input):
    codes = compiler.compile(input)
    vm.run(codes)


main("""

a = 4;
b = a - 3;
a + b;

""")
    

