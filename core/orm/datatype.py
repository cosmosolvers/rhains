

def string(n):
    return f'VARCHAR({n})'

def char(n):
    return f'CHAR({n})'

def clobs():
    return 'CLOB'

def integer():
    return 'INTEGER'

def timestamp():
    return 'TIMESTAMP'

def datetimg():
    return 'DATE'

def time():
    return 'TIME'

def blob():
    return 'BLOB'

def binary():
    return 'BINARY'

def varbinary(n):
    return f'VARBINARY({n})'

def text():
    return 'TEXT'

def boolean():
    return 'BOOLEAN'

def real():
    return 'FLOAT'

def double():
    return 'DECIMAL'

def decimal(p, s):
    return f'DECIMAL({p}, {s})'

def numeric(p, s):
    return f'NUMERIC({p}, {s})'

def interval():
    return 'INTERVAL'