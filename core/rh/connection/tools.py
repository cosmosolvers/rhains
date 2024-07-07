"""

"""
import re


def lt_(left, rigth):
    return True if left < rigth else False


def le_(left, rigth):
    return True if left <= rigth else False


def gt_(left, rigth):
    return True if left > rigth else False


def ge_(left, rigth):
    return True if left >= rigth else False


def in_(left, rigth):
    return True if left in rigth else False


def nin_(left, rigth):
    return True if left not in rigth else False


def ne_(left, rigth):
    return True if left != rigth else False


def like_(left, rigth):
    return True if re.search(rigth, left) else False


def bet_(left, rigth):
    return True if rigth[0] <= left <= rigth[-1] else False


def min_(left, rigth):
    return True if min(*left) == rigth else False


def max_(left, rigth):
    return True if max(*left) == rigth else False


def avg_(left, rigth):
    return True if sum(left) / len(left) == rigth else False


def rm_(left, rigth):
    _t = type(left)
    left = list(left)
    if rigth in left:
        left.remove(rigth)
    left = _t(left)


def add_(left, rigth):
    _t = type(left)
    left = list(left)
    left.append(rigth)
    left = _t(left)


agents = {
    '$lt': lt_,
    '$le': le_,
    '$gt': gt_,
    '$ge': ge_,
    '$in': in_,
    '$nin': nin_,
    '$ne': ne_,
    '$like': like_,
    '$$': bet_,
    '$min': min_,
    '$max': max_,
    '$avg': avg_,
    '$rm': rm_,
    '$add': add_
}


class DataParser:
    pass
