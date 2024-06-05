""""""

def less_than_instrcut(key: str, value):
    return f"{key} < ?", (value,)


def less_equal_instruct(key: str, value):
    return f"{key} <= ?", (value,)


def greater_than_instruct(key: str, value):
    return f"{key} > ?", (value,)


def greater_equal_instruct(key: str, value):
    return f"{key} >= ?", (value,)


def in_instruct(key: str, value):
    return f"{key} IN (?)", (value,)


def ne_instruct(key: str, value):
    return f"{key} != ?", (value,)


def nin_instruct(key: str, value):
    return f"{key} NOT IN (?)", (value,)


def between_instruct(key: str, value):
    return f"{key} BETWEEN ? AND ?", (value,)




CONNECTOR = {
    # less than < value
    'lt': less_equal_instruct,
    # greater than > value
    'gt': greater_than_instruct,
    # in (tuple, list)
    'in': in_instruct,
    # not in (tuple, list)
    'nin': nin_instruct,
    # not equal != value
    'ne': ne_instruct,
    # less or equal <= value
    'le': less_equal_instruct,
    # greater or equal >= value
    'ge': greater_equal_instruct,
    # interval (tuple, list)
    'bet': between_instruct,
    # max value (list, tuple)
    'max': max,
    # min value (list, tuple)
    'min': min,
    # sum value (list, tuple)
    'sum': sum,
    # average value (list, tuple)
    'avg': lambda *args: sum(args) / len(args),
    # regex pattern
    'like': lambda key, value: f"{key} REGEXP ?", (value,),
}



# 1. simple list
# {
#     '$pull': {'$': '*'}
# }
# 2. filter
# {
#     '$pull': {
#         'field': 'value',
#         'field': {'$gt': 'value'}
#     }
# }
# 3. utiliser les requirements
# {
#     '$pull': {
#         'field': 'value',
#         'field': {'$gt': 'value'}
#         'field': {'$fk': {'field': 'value}}
#     }
# }
# 4. utiliser les agents
# {
#     '$pull': {
#         'field': 'value',
#         'field': {'$gt': 'value'}
#         '$': {
#             {'$-': {'field': 'value'}},
#             {'$.': '!'}
#         }
#     }
# }
# 5. utiliser les conditions
# {
#     '$pull': {
#         'field': 'value',
#         'field': {'$gt': 'value'}
#         'field': {'$lt': 'value'},
#         'field': {'$le': 'value'},
#         'field': {'$gt': 'value'},
#         'field': {'$ge': 'value'},
#         'field': {'$in': 'value'},
#         'field': {'$nin': 'value'},
#         'field': {'$ne': 'value'},
#         'field': {'$like': 'value'},
#         'field': {'$min': 'value'},
#         'field': {'$max': 'value'},
#         'field': {'$avg': 'value'},
#         'field': {'$rm': 'value'},
#         'field': {'$add': 'value'},
#         'field': {'$set': 'value'}
#         }
#     }
# }

