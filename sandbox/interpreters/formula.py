# update 28.04.2025


def interpret(formula, dictionary):
    """ Interpretation einer Formel in Postfix-Form
    Erlaubte Operatoren: AND, OR, NOT
    Das dictionary enthaelt die auszufuehrenden Funktionen """

    stack = []
    for token in formula.split():
        if token == "AND":
            p = stack.pop()
            q = stack.pop()
            stack.append(lambda x: q(x) & p(x))
        elif token == "OR":
            p = stack.pop()
            q = stack.pop()
            stack.append(lambda x: q(x) | p(x))
        elif token == "NOT":
            p = stack.pop()
            stack.append(lambda x: not p(x))
        else:
            stack.append(dictionary[token])
    return stack.pop()
