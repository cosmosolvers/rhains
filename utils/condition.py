""""""


def less_than_instrcut(tab: str, key: str, value):
    return f"{tab}.{key} < ?", (value,)


def less_equal_instruct(tab: str, key: str, value):
    return f"{tab}.{key} <= ?", (value,)


def greater_than_instruct(tab: str, key: str, value):
    return f"{tab}.{key} > ?", (value,)


def greater_equal_instruct(tab: str, key: str, value):
    return f"{tab}.{key} >= ?", (value,)


def in_instruct(tab: str, key: str, value):
    return f"{tab}.{key} IN (?)", (value,)


def ne_instruct(tab: str, key: str, value):
    return f"{tab}.{key} != ?", (value,)


def nin_instruct(tab: str, key: str, value):
    return f"{tab}.{key} NOT IN (?)", (value,)


def between_instruct(tab: str, key: str, value):
    return f"{tab}.{key} BETWEEN ? AND ?", (value,)


CONDITION = {
    # less than < value
    '$lt': less_equal_instruct,
    # greater than > value
    '$gt': greater_than_instruct,
    # in (tuple, list)
    '$in': in_instruct,
    # not in (tuple, list)
    '$nin': nin_instruct,
    # not equal != value
    '$ne': ne_instruct,
    # less or equal <= value
    '$le': less_equal_instruct,
    # greater or equal >= value
    '$ge': greater_equal_instruct,
    # interval (tuple, list)
    '$$': between_instruct,
    # regex pattern
    '$like': lambda tab, key, value: (f"{tab}.{key} REGEXP ?", (value,))
}

HAVING = {
    # max value (list, tuple)
    '$max': max,
    # min value (list, tuple)
    '$min': min,
    # sum value (list, tuple)
    '$sum': sum,
    # average value (list, tuple)
    '$avg': lambda *args: sum(args) / len(args),
}
