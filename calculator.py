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


# def calc(string):
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
#     ret = get_tokens(string)
#     print(ret)


def calc(string):
    def eval(tokens):
        stack = []
        c = tokens.pop()
        if c == '-':
            v = tokens.pop()
            v = -v
        else:
            v = c
        stack.append(v)
        
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


# calc('-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54*-1')

assert calc('(1)') == 1
assert calc('-(1)') == -1
assert calc('(-1)') == -1
assert calc('1+ 1') == 2
assert calc('10 + 210') == 220
assert calc('- 11 + 210') == 199
assert calc('1+ 1-2*7/3') == -2
assert calc('10+ 12-2*7/3') == 18
assert calc('-(1+(4+5+2)-3)+(6+8)') == 5
assert calc('-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54') == 279
assert calc('-(-10 + ((-100*22/74-50/11*10-1)*3 -2)) + 54*-1*-1') == 279

