"""
Python Implementation of Pratt's Operator-precedence parser

reference: 
    https://eli.thegreenplace.net/2010/01/02/top-down-operator-precedence-parsing/

"""

class IntegerToken:
    def __init__(self, num: str):
        self._num = int(num)
    
    @property
    def nud(self):
        return self._num


class AddToken:
    level = 10

    @property
    def nud(self):
        return evaluate(100)

    def infix(self, left):
        return left + evaluate(self.level)
        

class MinusToken:
    level = 10

    @property
    def nud(self):
        return -evaluate(100)

    def infix(self, left):
        return left - evaluate(self.level)


class MulToken:
    level = 20

    def infix(self, left):
        return left * evaluate(self.level)

class DivToken:
    level = 20

    def infix(self, left):
        return left / evaluate(self.level)

class LParenToken:
    level = 0
    
    @property
    def nud(self):
        res = evaluate()
        if isinstance(l.cur_token, RParenToken):
            l.next_token()
        return res

    def infix(self, left):
        return left / evaluate(self.level)

class RParenToken:
    level = 0

class EOF:
    level = 0


class Lexer:
    def __init__(self, input_):
        self._input = input_
        self._idx = 0
        self.cur_token = None

        self.next_token()

    def next_token(self):
        self._skip_space()

        token = None
        if self._idx >= len(self._input):
            token = EOF()
        elif self._input[self._idx] ==  '+':
            self._idx += 1
            token = AddToken()
        elif self._input[self._idx] in '*':
            self._idx += 1
            token = MulToken()
        elif self._input[self._idx] in '-':
            self._idx += 1
            token = MinusToken()
        elif self._input[self._idx] in '/':
            self._idx += 1
            token = DivToken()
        elif self._input[self._idx] in '(':
            self._idx += 1
            token = LParenToken()
        elif self._input[self._idx] in ')':
            self._idx += 1
            token = RParenToken()
        elif self._input[self._idx].isdigit():
            token = self._read_number()
        
        self.cur_token = token
        return self.cur_token
            
    def _read_number(self):
        num = ''
        while self._idx < len(self._input) and self._input[self._idx].isdigit():
            num += self._input[self._idx]
            self._idx += 1

        return IntegerToken(num)

    def _skip_space(self):
        while self._idx < len(self._input) and self._input[self._idx].isspace():
            self._idx += 1


def evaluate(level=0):
    left_token = l.cur_token
    
    l.next_token()

    val = left_token.nud

    while l.cur_token.level > level:
        operator = l.cur_token
        l.next_token()
        val = operator.infix(val)

    return val


def calculating(expr):
    """
    >>> s = '(1)'; calculating(s) == eval(s)
    True
    >>> s = '-(1)'; calculating(s) == eval(s)
    True
    >>> s = '(-1)'; calculating(s) == eval(s)
    True
    >>> s = '1+ 1'; calculating(s) == eval(s)
    True
    >>> s = '10 + 210'; calculating(s) == eval(s)
    True
    >>> s = '- 11 + 210'; calculating(s) == eval(s)
    True
    >>> s = '1+ 1-2*7/3'; calculating(s) == eval(s)
    True
    >>> s = '10+ 12-2*7/3'; calculating(s) == eval(s)
    True
    >>> s = '-(1+(4+5+2)-3)+(6+8)'; calculating(s) == eval(s)
    True
    >>> s = '-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54'; calculating(s) == eval(s)
    True
    >>> s = '-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54*-1*-1'; calculating(s) == eval(s)
    True
    >>> s = '-(-10 +--((-100*22/74-50/11*10-1)*3 -2)) + 54*-1*-1'; calculating(s) == eval(s)
    True
    >>> s = '-+---1'; calculating(s) == eval(s)
    True
    >>> s = '---1 + ---+-1'; calculating(s) == eval(s)
    True

    """

    global l
    l = Lexer(expr)
    ans = evaluate()
    return ans


if __name__ == '__main__':
    import doctest
    doctest.testmod()


