# j.siedersleben
# fasttrack to professional programming
# lesson 2: collections
# 17.11.2020
# update 29.04.2025


#######################
##      index 1      ##
#######################

def index_1(book):
    """
    book[i]      = list of indexable words on page i
    result[word] = list of pages containing word
    """
    result = {}
    for i, page in enumerate(book):
        for word in set(page):
            if word not in result.keys():
                result[word] = []
            result[word].append(i)
    return result


#######################
##      index 2      ##
#######################

def index_2(book, keywords):
    """
    book[i]  = set of all words on page i
    keywords = set of all indexable words
    result[word] = list of pages containing word
    standard solution
    """
    result = {}
    for i, page in enumerate(book):
        for word in set(page) & set(keywords):
            if word not in result.keys():
                result[word] = []
            result[word].append(i)
    return result


def index_2a(book, keywords):
    """
    book[i]  = set of all words on page i
    keywords = set of all indexable words
    result[word] = list of pages containing word
    elegant but slower
    idea: replace each page with the intersection of page and keywords
    """
    book = [set(page) & set(keywords) for page in book]
    return index_2(book, keywords)


#############################
##      search index       ##
#############################

def make_index(rows, v):
    """
    :param rows: list of rows; each row being a tuple of test_fields or whatever
    :param v: row -> value (value to be indexed)
    :return: a dictionary; key = field, value = IDs of rows with v(row) = value
    """
    index = {}

    for i, row in enumerate(rows):
        value = v(row)
        if value not in index.keys():
            index[value] = []
        index[value].append(i)

    return index


def make_indices(rows, vs):
    """
    :param rows: list of rows; each row being a tuple of test_fields or whatever
    :param vs: functions v: row -> value (value to be indexed)
    :return: a list of dictionaries; key = field, value = IDs of rows with v(row) = value
    """
    indices = []
    for _ in range(len(vs)):
        indices.append({})

    for i, row in enumerate(rows):
        for j, v in enumerate(vs):
            value = v(row)
            if value not in indices[j].keys():
                indices[j][value] = []
            indices[j][value].append(i)

    return indices


def is_descending(xs):
    return True if len(xs) <= 1 \
        else xs[0] > xs[1] and is_descending(xs[1:])
