# def calc(string):
#     """ oo way
#     """

# def calc(string):
#     """ recursive way
#     """
#     def get_components(tokens):
#         """
#         divide tokens into several components of same level,
#         the level of + -
#         """
#         components = []
# 
#     def eval(tokens):
#         pass
# 
#     tokens = get_tokens(string)
#     stack = []


def calc(string):
    def eval(tokens):
        """ eval just calculates the same level expression
        """


def get_tokens(s):
    def int(s):
        ans = 0

        for i in range(len(s)):
            ans += (ord(s[-i-1]) - ord('0')) * 10**i
        return ans

    tokens = []
    num = ''
    for c in s:
        if '0' <= c <= '9':
            num += c
        elif c in '+-*/()':
            if num:
                tokens.append(int(num))
            tokens.append(c)
            num = ''
    else:
        if num:
            tokens.append(int(num))

    return tokens


def calc_brutalforce(string):
    """
    >>> calc_brutalforce('(1)')
    1
    >>> calc_brutalforce('-(1)')
    -1
    >>> calc_brutalforce('(-1)')
    -1
    >>> calc_brutalforce('1+ 1')
    2
    >>> calc_brutalforce('10 + 210')
    220
    >>> calc_brutalforce('- 11 + 210')
    199
    >>> calc_brutalforce('1+ 1-2*7/3')
    -2
    >>> calc_brutalforce('10+ 12-2*7/3')
    18
    >>> calc_brutalforce('-(1+(4+5+2)-3)+(6+8)')
    5
    >>> calc_brutalforce('-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54')
    279
    >>> calc_brutalforce('-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54*-1*-1')
    279

    """

    def eval(tokens):
        stack = []
        c = tokens.pop()
        if c == '-':
            v = tokens.pop()
            v = -v
        else:
            v = c
        stack.append(v)
        
        # calculate the level of '*/'
        while tokens:
            c = tokens.pop()

            if c == '*':
                t = tokens.pop()
                if isinstance(t, str):
                    t2 = tokens.pop()
                    if t == '-':
                        v = -t2
                    else:
                        v = t2
                else:
                    v = t
                sv = stack.pop()
                stack.append(sv * v)
            elif c == '/':
                t = tokens.pop()
                if isinstance(t, str):
                    t2 = tokens.pop()
                    if t == '-':
                        v = -t2
                    else:
                        v = t2
                else:
                    v = t
                sv = stack.pop()
                stack.append(sv // v)
            elif c == '-':
                stack.append(c)
                t = tokens.pop()
                if isinstance(t, str):
                    t2 = tokens.pop()
                    if t == '-':
                        v = -t2
                    else:
                        v = t2
                else:
                    v = t
                stack.append(v)
            elif c == '+':
                stack.append(c)
                t = tokens.pop()
                if isinstance(t, str):
                    t2 = tokens.pop()
                    if t == '-':
                        v = -t2
                    else:
                        v = t2
                else:
                    v = t
                stack.append(v)
            else:
                raise Exception("expression error")

        # calculate the level of '-+'
        stack.reverse()
        v = stack.pop()
        while stack:
            operator, operand = stack.pop(), stack.pop()
            if operator == '+':
                v += operand
            elif operator == '-':
                v -= operand
        return v

    tokens = get_tokens(string)
    stack = []

    # calculate the level of '()'
    for tk in tokens:
        if tk == ')':
            expression = []
            while (t := stack.pop()) != '(':
                expression.append(t)
            val = eval(expression)
            stack.append(val)
        else:
            stack.append(tk)

    else:
        expression = list(reversed(stack))
        rv = eval(expression)

    return rv


def calc_by_priority(string):
    """
    >>> calc_by_priority('(1)')
    1
    >>> calc_by_priority('-(1)')
    -1
    >>> calc_by_priority('(-1)')
    -1
    >>> calc_by_priority('1+ 1')
    2
    >>> calc_by_priority('10 + 210')
    220
    >>> calc_by_priority('- 11 + 210')
    199
    >>> calc_by_priority('1+ 1-2*7/3')
    -2
    >>> calc_by_priority('10+ 12-2*7/3')
    18
    >>> calc_by_priority('-(1+(4+5+2)-3)+(6+8)')
    5
    >>> calc_by_priority('-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54')
    279
    >>> calc_by_priority('-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54*-1*-1')
    279
    >>> calc_by_priority('-+---1')
    1
    >>> calc_by_priority('---1 + ---+-1')
    0

    """

    def eval(tokens):
        """ eval expression of the level, say, '*/' and '-+'
        """

        def value(tokens):
            v = tokens.pop()
            while tokens:
                sign = tokens.pop()
                v *= [-1, 1][sign == '+']
            return v

        operators = []
        operands = []

        if isinstance(tokens[-1], int):
            operands.append(tokens.pop())
        else:
            t = []
            while isinstance((tk := tokens.pop()), str):
                t.append(tk)
            else:
                t.append(tk)

            operands.append(value(t))

        while tokens:
            operators.append(tokens.pop())

            t = []
            while isinstance(tk := tokens.pop(), str):
                t.append(tk)
            else:
                t.append(tk)
                operands.append(value(t))

        operators.reverse()
        operands.reverse()
        secondary_operators = []
        secondary_operands = []
        while operators:
            operator = operators.pop()
            if operator in '-+':
                secondary_operators.append(operator)
                secondary_operands.append(operands.pop())
            elif operator == '*':
                left, right = operands.pop(), operands.pop()
                operands.append(left * right)
            elif operator == '/':
                left, right = operands.pop(), operands.pop()
                operands.append(left // right)
        else:
            secondary_operands.append(operands.pop())

        secondary_operators.reverse()
        secondary_operands.reverse()
        while secondary_operators:
            operator = secondary_operators.pop()
            if operator == '+':
                left, right = secondary_operands.pop(), secondary_operands.pop()
                secondary_operands.append(left + right)
            elif operator == '-':
                left, right = secondary_operands.pop(), secondary_operands.pop()
                secondary_operands.append(left - right)

        return secondary_operands[0]

    tokens = get_tokens(string)
    stack = []

    # calculate the level of '()'
    for tk in tokens:
        if tk == ')':
            expression = []
            while (t := stack.pop()) != '(':
                expression.append(t)
            val = eval(expression)
            stack.append(val)
        else:
            stack.append(tk)

    else:
        expression = list(reversed(stack))
        rv = eval(expression)

    return rv


if __name__ == '__main__':
    import doctest
    doctest.testmod()

