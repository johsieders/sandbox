# j.siedersleben
# fasttrack to professional programming
# lesson 8: interpreters
# 20.11.2020

# update 29.04.2925


# the dict operator contains all operators with
# 1) arity (= 1 or 2) and
# 2) priority (= 1, 2 or 3; 1 = low, 3 = high)

operators = {'+': (2, 1), '-': (2, 1), '*': (2, 2), '/': (2, 2), '~': (1, 3)}


def infix2postfix(formula: String, operators: dict[str, tuple[int, int]])-> String:
    """
    transforms an infix into a postfix formula
    """
    formula = formula.strip()
    if not formula:
        return formula
    formula = stripBrackets(formula)
    left, op, right = split(formula, operators)
    if op is None:
        return formula
    left = infix2postfix(left, operators)
    right = infix2postfix(right, operators)
    if left:
        return left + ' ' + right + op
    else:
        return right + op


i2p = infix2postfix


def bracketsOk(formula):
    bc = 0  ## bracket count
    for c in formula:
        if c == '(':
            bc += 1
        elif c == ')':
            bc -= 1
            if bc < 0:  # bc must never be negative
                return False
    return bc == 0  # bc must be 0


def stripBrackets(formula):
    """ removes brackets and blanks"""
    while formula[0] == '(' and formula[-1] == ')' and bracketsOk(formula[1:-1]):
        formula = formula[1:-1]
    return formula.strip()


def split(formula, operators):
    """ returns
        a) the formula's first part
        b) the innermost operator (lowest priority)
        c) the formula's second part
    """
    bracketCount = 0  # counts brackets
    minWeight = 100000  # weight of lowest priority op
    minIdx = -1  # index of this op

    for i, c in enumerate(formula):
        if c == '(':
            bracketCount += 10
        elif c == ')':
            bracketCount -= 10
        elif operators.has_key(c):
            arity, prio = operators[c]
            w = prio + bracketCount
            if minWeight > w:
                minWeight, minIdx = w, i
    if minIdx < 0:  ## no operator
        return formula, None, None
    else:
        return formula[:minIdx], formula[minIdx], formula[minIdx + 1:]
