from exception.rhains import RhainsBaseException


class FieldCheckError(RhainsBaseException):
    ...


class FieldDefaultError(RhainsBaseException):
    ...


class FieldNullableError(RhainsBaseException):
    ...


class FieldEditableError(RhainsBaseException):
    ...


class FieldOverUseError(RhainsBaseException):
    ...


class IntegerFieldDefaultError(RhainsBaseException):
    ...


class FieldIntervalError(RhainsBaseException):
    ...


class IntegerFieldError(RhainsBaseException):
    ...


class FieldMinError(RhainsBaseException):
    ...


class FieldMaxError(RhainsBaseException):
    ...


class IntegerFieldLoadError(RhainsBaseException):
    ...


class IntegerFieldDumpError(RhainsBaseException):
    ...


class FieldChoicesError(RhainsBaseException):
    ...


class FieldMaxDigitsError(RhainsBaseException):
    ...


class FieldMinDigitsError(RhainsBaseException):
    ...


class FieldPrimarykeyError(RhainsBaseException):
    ...


class FieldUniqueError(RhainsBaseException):
    ...


class AggregationFieldValueError(RhainsBaseException):
    ...


class FieldMediaFormatError(RhainsBaseException):
    ...


class FieldFileSizeError(RhainsBaseException):
    ...


class FieldMediaPathError(RhainsBaseException):
    ...


class FieldFileNotFoundError(RhainsBaseException):
    ...
