# class Integer:
#     def __init__(self) -> None:
#         self.value = 0

#     def __get__(self, instance, owner):
#         return self.value

#     def __set__(self, instance, value):
#         self.value = value


# class Model:
#     id = Integer()
#     name = 'hydromel'
#     age = Integer()

#     class Meta:
#         my = 'meta'


# if __name__ == '__main__':
#     print(Model.__name__)
#     print(Model.__dict__)
#     print(Model.__module__)
#     print(Model.__class__)
#     print(Model.__bases__)
#     print(Model.__qualname__)
#     print(Model.__annotations__)
#     print(Model.__doc__)
#     print(Model.Meta.__dict__)
#     print(Model.__repr__)
#     print(Model.__str__)
#     print(Model.__hash__)
#     print(Model.__dir__)
#     print(Model.__sizeof__)
#     print(Model.__format__)
#     print(Model.__getattribute__)
#     print(Model.__setattr__)
#     print(Model.__delattr__)
#     print(Model.__init__)
#     print(Model.__new__)
#     print(Model.__del__)
#     print(Model.__lt__)
#     print(Model.__le__)
#     print(Model.__eq__)
#     print(Model.__ne__)
#     print(Model.__gt__)
#     print(Model.__ge__)
#     print(Model.__iter__)
#     print(Model.__next__)
#     print(Model.__reversed__)
#     print(Model.__contains__)
#     print(Model.__getitem__)
#     print(Model.__setitem__)
#     print(Model.__delitem__)
#     print(Model.__len__)
#     print(Model.__length_hint__)
#     print(Model.__add__)
#     print(Model.__sub__)
#     print(Model.__mul__)
#     print(Model.__matmul__)
#     print(Model.__truediv__)
#     print(Model.__floordiv__)
#     print(Model.__mod__)
#     print(Model.__divmod__)
#     print(Model.__pow__)
#     print(Model.__lshift__)
#     print(Model.__rshift__)
#     print(Model.__and__)
#     print(Model.__xor__)
#     print(Model.__or__)
#     print(Model.__radd__)
#     print(Model.__rsub__)
#     print(Model.__rmul__)
#     print(Model.__rmatmul__)
#     print(Model.__rtruediv__)
#     print(Model.__rfloordiv__)
#     print(Model.__rmod__)
#     print(Model.__rdivmod__)
#     print(Model.__rpow__)
#     print(Model.__rlshift__)
#     print(Model.__rrshift__)
#     print(Model.__rand__)
#     print(Model.__rxor__)
#     print(Model.__ror__)
#     print(Model.__iadd__)
#     print(Model.__isub__)
#     print(Model.__imul__)
#     print(Model.__imatmul__)
#     print(Model.__itruediv__)
#     print(Model.__ifloordiv__)
#     print(Model.__imod__)
#     print(Model.__ipow__)
#     print(Model.__ilshift__)
#     print(Model.__irshift__)
#     print(Model.__iand__)
#     print(Model.__ixor__)
#     print(Model.__ior__)
#     print(Model.__neg__)
#     print(Model.__pos__)
#     print(Model.__abs__)
#     print(Model.__invert__)
#     print(Model.__complex__)
#     print(Model.__int__)
#     print(Model.__float__)
#     print(Model.__index__)
#     print(Model.__round__)
#     print(Model.__trunc__)
#     print(Model.__floor__)
#     print(Model.__ceil__)
#     print(Model.__enter__)
#     print(Model.__exit__)
#     print(Model.__await__)
#     print(Model.__aiter__)
#     print(Model.__anext__)
#     print(Model.__aenter__)
#     print(Model.__aexit__)


# {
#     '$pull': {
#         '$pk': 'value',
#         'field': {
#             '$fk': {
#                 'field': 'value',
#                 'field': 'value',
#                 'field': {'$gt': 'value'},
#                 'field': {'$lt': 'value'},
#                 'field': {
#                     '$fk': {
#                         'field': 'value',
#                         'field': 'value',
#                     }
#                 }
#             }
#         }
#     }
# }
