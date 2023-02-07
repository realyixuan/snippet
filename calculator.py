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


def validate_string(string):
    """
    >>> validate_string('-1000000')
    (True, '')
    >>> validate_string('1000000')
    (True, '')
    >>> validate_string('(1)')
    (True, '')
    >>> validate_string('-(1)')
    (True, '')
    >>> validate_string('10+ 12-2*7/3')
    (True, '')
    >>> validate_string('-(1+(4+5+2)-3)+(6+8)')
    (True, '')
    >>> validate_string('-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54')
    (True, '')
    >>> validate_string('-(-10 + ((-100*   22/74-    50/11*10-1)*3 -2)) + 54*-1*-1')
    (True, '')
    >>> validate_string('---1 + ---+-1')
    (True, '')
    >>> validate_string('((((((1))))))')
    (True, '')
    >>> validate_string('1-')
    (False, 'wrong expression')
    >>> validate_string('10+ 12-2*7/3-')
    (False, 'wrong expression')
    >>> validate_string('(((((())))))')
    (False, 'wrong expression')
    >>> validate_string('-(1+(4+5+2-3)+(6+8)')
    (False, 'wrong expression')
    >>> validate_string('-))(1+(4+5+2-3+(6+8')
    (False, 'wrong expression')
    >>> validate_string('asdf+908+8888')
    (False, 'wrong expression')
    >>> validate_string('asdf+908+8888.999')
    (False, 'wrong expression')
    >>> validate_string('1+2*(((((())))))-1')
    (False, 'wrong expression')
    >>> validate_string('10+ 12-2*7/*3')
    (False, 'wrong expression')
    >>> validate_string('10+ 12-*2*7*3')
    (False, 'wrong expression')

    """

    def validate_characters(string):
        for c in string:
            if c not in '()+-*/0123456789 ':
                return False
        return True
        
    def validate_parentheses(tokens):
        pair = 0
        for token in tokens:
            if token == '(':
                pair += 1
            elif token == ')':
                pair -= 1
        return pair == 0

    def validate_value(tokens):
        signs = tokens[:-1]
        num = tokens[-1:]
        return (
                all(sign in '-+' for sign in signs)
            and len(num) == 1
            and isinstance(num[0], int)
        )

    def validate_expr(tokens):
        if not tokens:
            return False

        operators = []
        operands = []

        stack = []
        for tk in tokens:
            if len(operators) == len(operands):
                if isinstance(tk, int):
                    stack.append(tk)
                    operands.append(stack)
                    stack = []
                else:
                    stack.append(tk)
            else:
                operators.append(tk)
        else:
            if stack:
                operands.append(stack)

        return (
                all(operator in '+-*/' for operator in operators)
            and all(validate_value(operand) for operand in operands)
            and len(operands)-len(operators) == 1
        )


    def validate(tokens):
        stack = []
        pair = 0
        parentheses = []
        for tk in tokens:
            if tk == '(':
                pair += 1

            if pair == 0:
                stack.append(tk)
            else:
                parentheses.append(tk)

            if tk == ')':
                pair -= 1
                if pair == 0:
                    if not validate(parentheses[1:-1]):
                        return False
                    stack.append(0)
                    parentheses = []

        return validate_expr(stack)

    if not validate_characters(string):
        return False, "wrong expression"

    tokens = get_tokens(string)
    if not validate_parentheses(tokens):
        return False, 'wrong expression'
    elif not validate(tokens):
        return False, "wrong expression"

    return True, ''


def calc_recursion(string):
    """
    >>> calc_recursion('(1)')
    1
    >>> calc_recursion('-(1)')
    -1
    >>> calc_recursion('(-1)')
    -1
    >>> calc_recursion('1+ 1')
    2
    >>> calc_recursion('10 + 210')
    220
    >>> calc_recursion('- 11 + 210')
    199
    >>> calc_recursion('1+ 1-2*7/3')
    -2
    >>> calc_recursion('10+ 12-2*7/3')
    18
    >>> calc_recursion('-(1+(4+5+2)-3)+(6+8)')
    5
    >>> calc_recursion('-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54')
    279
    >>> calc_recursion('-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54*-1*-1')
    279
    >>> calc_recursion('-(-10 +--((-100*22/74-50/11*10-1)*3 -2)) + 54*-1*-1')
    279
    >>> calc_recursion('-+---1')
    1
    >>> calc_recursion('---1 + ---+-1')
    0

    """
    
    def eval_expression(tokens):
        operators = tokens[-2::-2]
        operands = tokens[-1::-2]

        # this doesn't seem like a good approach
        # it mixes '*/' and '+-' on a single logical line
        # separating it into different parts could be better
        # because '*/' and '-+' are different though have similar logic, if 
        # the part of same logic needs to be reused, the different part 
        # must be taken out, and there should be a little more complex structure of design
        # in fact, you have to manually operate '*/', and '-+'
        # So, here, though the same logic works for both cases, it's just a trick, which
        # just squeezed two things together, just so. Consequently, program become bloated,
        # with every logic going through some code they never need.
        while operators:
            operator = operators.pop()
            left, right = operands.pop(), operands.pop()

            if operator == '*':
                operands.append(left * right)
            elif operator == '/':
                operands.append(left // right)
            elif operator == '+':
                operands.append(left + right)
            elif operator == '-':
                operands.append(left - right)

        return operands[0]

    def value(tokens):
        v = tokens.pop()
        while tokens:
            sign = tokens.pop()
            v *= [-1, 1][sign == '+']
        return v

    def next_value(tokens):
        stack = []
        while isinstance((tk := tokens.pop()), str):
            stack.append(tk)
        else:
            stack.append(tk)
        return value(stack)

    def eval(tokens):
        stack = []
        i = 0
        t = []
        for tk in tokens:
            if tk == '(':
                i += 1

            if i == 0:
                stack.append(tk)
            else:
                t.append(tk)

            if tk == ')':
                i -= 1
                if i == 0:
                    stack.append(eval(t[1:-1]))
                    t = []

        stack.reverse()
        two_level_stack = [[next_value(stack)]]
        while stack:
            operator, operand = stack.pop(), next_value(stack)
            if operator in '*/':
                two_level_stack[-1].append(operator)
                two_level_stack[-1].append(operand)
            elif operator in '+-':
                two_level_stack.append(operator)
                two_level_stack.append([operand])

        one_level_stack = [eval_expression(two_level_stack[0])]
        for i in range(1, len(two_level_stack), 2):
            one_level_stack.append(two_level_stack[i])
            one_level_stack.append(eval_expression(two_level_stack[i+1]))

        res = eval_expression(one_level_stack)

        return res

    tokens = get_tokens(string)
    ret = eval(tokens)
    return ret


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
    >>> calc_by_priority('-(-10 +--((-100*22/74-50/11*10-1)*3 -2)) + 54*-1*-1')
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

