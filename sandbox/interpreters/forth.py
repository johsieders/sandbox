# Johannes Siedersleben
# QAware GmbH
# 6.2.2022

# This is a partial implementation of Forth as described in
# Forth Programmer's Handbook,
# Edward K. Conklin, Elizabeth D. Rather, Forth Inc,, 2007
#
# This how to use it:
# F = Forth()
# F(any legal Forth program)
# str(F) returns the stack
# F('.') returns the top of stack
#
# A simple example: Squaring
# F('7 DUP *')  # 49
# F(': SQUARE ( a - a2 ) DUP * ; ')     # defines SQUARE
# F('7 SQUARE')                         # calls SQUARE on 7
# F(': SQUARE ( a - a2 ) DUP * ; 7 SQUARE')    # defines SQUARE and calls it

# The Euclidean algorithm
# F(': GCD ( b a - gcd) BEGIN DUP -ROT MOD DUP NOT UNTIL DROP ;')
# F('80 90 GCD')            # returns 10
#
# The recursive version works quite as well
# F(': GCD ( b a - gcd) DUP -ROT MOD DUP IF GCD ELSE DROP THEN ;')
#
# The Horner algorithm
# F(': HORNER ( a0 a1 .. an n x - p(x) ) SWAP DUP NOT IF DROP ELSE 0 DO DUP >R * +  R> LOOP THEN DROP ;')
# F('1 2 3 2 10 HORNER')    # computes p(10) = 1 + 2*10 + 3*100 = 321


class Forth(object):
    def __init__(self):
        self.stack = []  # data and words. Survives call, available for next call
        self.return_stack = []  # data only. Must be empty at end of call
        self.stdout = []  # Standard out. Survives call, available for documentation
        self.stderr = []  # Standard error. Survives call, available for documentation

        self.words = {'.': self.dot,
                      ':': self.colon,
                      'IF': self._if,
                      'BEGIN': self.begin,
                      'DO': self.do,
                      '+': self.plus,
                      '-': self.minus,
                      '1-': self.one_minus,
                      '*': self.star,
                      '/': self.slash,
                      '<': self.less_than,
                      'NOT': self._not,
                      '>R': self.to_R,
                      'R>': self.R_from,
                      'DROP': self.drop,
                      'DUP': self.dup,
                      '?DUP': self.q_dup,
                      '2DUP': self.dup2,
                      'MOD': self.mod,
                      'PICK': self.pick,
                      'ROT': self.rot,
                      '-ROT': self.m_rot,
                      'SWAP': self.swap,
                      'NIP': self.nip,
                      'TUCK': self.tuck,
                      'OVER': self.over}

    def clear(self):
        """
        clear stack, stdout, stderr
        """
        self.stack.clear()
        self.stdout.clear()
        self.stderr.clear()

    def __call__(self, code: str):
        tokens = code.split()
        self.run(tokens)
        return self.stdout

    def __str__(self):
        return str(self.stack)

    def run(self, tokens: list):
        while tokens:
            token = tokens[0]  # token to be processed
            tokens = tokens[1:]  # popleft token
            word = self.words.get(token)
            if token in ['IF', 'BEGIN', 'DO', ':']:  # control structures
                tokens = word(tokens)  # tokens given and tokens returned start at first token to be processed
            elif word:
                word()
            else:
                self.stack.append(int(token))

    def _if(self, tokens: list):
        count = 0
        next_then = 0
        next_else = 0
        for i, token in enumerate(tokens):
            if token == 'THEN' and count == 0:  # next THEN found
                next_then = i
                break
            if token == 'ELSE' and count == 0:  # next ELSE found
                next_else = i
            elif token == 'IF':  # irrelevant IF
                count += 1
            elif token == 'THEN':  # irrelevant THEN
                count -= 1

        if next_then == 0:
            self.stderr.append('bad if-structure')
            raise Exception
        if next_else == 0:
            next_else = next_then

        if_clause = tokens[:next_else]
        else_clause = tokens[next_else + 1:next_then]
        if self.stack.pop():
            self.run(if_clause)
        else:
            self.run(else_clause)
        return tokens[next_then + 1:]

    def begin(self, tokens: list):
        """
        it's either an UNTIL- or a REPEAT-loop
        """
        count = 0
        next_until = 0
        next_repeat = 0
        next_while = 0

        for i, token in enumerate(tokens):  # test_ for UNTIL
            if token == 'UNTIL' and count == 0:  # next UNTIL found
                next_until = i
                break
            elif token == 'BEGIN':  # irrelevant BEGIN
                count += 1
            elif token == 'UNTIL':  # irrelevant UNTIL
                count -= 1

        if next_until > 0:  # it's a UNTIL loop
            loop_clause = tokens[:next_until]  # everything between BEGIN and UNTIL
            self.run(loop_clause)  # run loop_clause until top of stack is true
            while not self.stack.pop():
                self.run(loop_clause)
            return tokens[next_until + 1:]

        else:  # must be a WHILE .. REPEAT loop
            count = 0
            for i, token in enumerate(tokens):
                if token == 'WHILE' and count == 0:  # next WHILE found
                    next_while = i
                if token == 'REPEAT' and count == 0:  # next REPEAT found
                    next_repeat = i
                    break
                elif token == 'BEGIN':  # irrelevant BEGIN
                    count += 1
                elif token == 'REPEAT':  # irrelevant REPEAT
                    count -= 1

            if next_repeat == 0 or next_while == 0:  # is neither UNTIL nor REPEAT
                self.stderr.append('bad begin-structure')
                raise Exception

            while_clause = tokens[:next_while]  # everything between BEGIN and WHILE
            repeat_clause = tokens[next_while + 1:next_repeat]  # everything between WHILE and REPEAT

            while True:  # run while until top of stack is false
                self.run(while_clause)
                if self.stack.pop():
                    self.run(repeat_clause)  # not executed at last iteration
                else:
                    break
            return tokens[next_repeat + 1:]

    def do(self, tokens: list):
        initial = self.stack.pop()
        limit = self.stack.pop()

        count = 0
        next_loop = 0
        for i, token in enumerate(tokens):
            if token == 'LOOP' and count == 0:  # next LOOP found
                next_loop = i
                break
            elif token == 'DO':  # irrelevant DO
                count += 1
            elif token == 'LOOP':  # irrelevant LOOP
                count -= 1

        if next_loop == 0:
            self.stderr.append('bad do-structure')
            raise Exception

        loop_clause = tokens[:next_loop]  # everything between DO and LOOP
        for _ in range(initial, limit):
            self.run(loop_clause)  # run loop (limit - initial) times
        return tokens[next_loop + 1:]

    def colon(self, tokens: list):
        """
        This method defines a new word given as ': LITERAL ( comment ) <code>;'
        and stores it in self.words under LITERAL
        """
        literal = tokens[0]  # get literal
        tokens = tokens[1:]

        if tokens[0] == '(':  # eliminate comment
            count = 0
            end_comment = 0
            for i, token in enumerate(tokens[1:]):
                if token == ')' and count == 0:  # end_comment found
                    end_comment = i
                    break
                elif token == '(':  # irrelevant (
                    count += 1
                elif token == ')':  # irrelevant )
                    count += -1

            if end_comment == 0:
                self.stderr.append('bad comment-structure')
                raise Exception

            tokens = tokens[end_comment + 2:]

        next_semicolon = 0
        for i, token in enumerate(tokens):
            if token == ';':
                next_semicolon = i
                break

        if next_semicolon == 0:
            self.stderr.append('bad word-structure')
            raise Exception

        sub = tokens[:next_semicolon]
        self.words[literal] = lambda: self.run(sub)
        return tokens[next_semicolon + 1:]

    def to_R(self):
        a = self.stack.pop()
        self.return_stack.append(a)

    def R_from(self):
        a = self.return_stack.pop()
        self.stack.append(a)

    def dot(self):
        self.stdout.append(self.stack.pop())

    def drop(self):
        self.stack.pop()

    def _not(self):
        a = self.stack.pop()
        self.stack.append(not bool(a))

    def dup(self):
        a = self.stack[-1]
        self.stack.append(a)

    def pick(self):
        # (an an-1 .. a0 n - an an-1 .. a0 an)
        n = self.stack.pop()
        a = self.stack[-n]
        self.stack.append(a)

    def q_dup(self):
        a = self.stack[-1]
        if a:
            self.stack.append(a)

    def dup2(self):
        """
        (b a - b a b a)
        """
        a = self.stack[-1]
        b = self.stack[-2]
        self.stack.append(b)
        self.stack.append(a)

    def swap(self):
        """
        swap top and second
        ( b a - a b )
        """
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(a)
        self.stack.append(b)

    def m_rot(self):
        """
        top to third
        ( c b a - a c b )
        """
        a = self.stack.pop()
        b = self.stack.pop()
        c = self.stack.pop()
        self.stack.append(a)
        self.stack.append(c)
        self.stack.append(b)

    def rot(self):
        """
        third to top
        ( c b a - b a c )
        """
        a = self.stack.pop()
        b = self.stack.pop()
        c = self.stack.pop()
        self.stack.append(b)
        self.stack.append(a)
        self.stack.append(c)

    def tuck(self):
        """
        copy of top to third
        ( b a - a b a )
        """
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(a)
        self.stack.append(b)
        self.stack.append(a)

    def over(self):
        """
        copy of second to top
        ( b a - b a b )
        """
        b = self.stack[-2]
        self.stack.append(b)

    def nip(self):
        """
        drop second item on stack
        ( c b a - c a )
        """
        a = self.stack.pop()
        self.stack.pop()
        self.stack.append(a)

    def plus(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b + a)

    def minus(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b - a)

    def one_minus(self):
        a = self.stack.pop()
        self.stack.append(a - 1)

    def star(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b * a)

    def slash(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b // a)

    def mod(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b % a)

    def less_than(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b < a)

