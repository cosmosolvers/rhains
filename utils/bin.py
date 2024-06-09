import base64

alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def decimal_to_binary(decimal: int) -> str:
    return bin(decimal)[2:]


def decimal_to_hexadecimal(decimal: int) -> str:
    return hex(decimal)[2:]


def decimal_to_base64(decimal: int) -> str:
    return base64.b64encode(
        decimal.to_bytes((decimal.bit_length() + 7) // 8, 'big')).decode()


def decimal_to_base64url(decimal: int) -> str:
    return base64.urlsafe_b64encode(
        decimal.to_bytes((decimal.bit_length() + 7) // 8, 'big')).decode()


def decimal_to_base32(decimal: int) -> str:
    return base64.b32encode(
        decimal.to_bytes((decimal.bit_length() + 7) // 8, 'big')).decode()


def decimal_to_baseN(decimal: int, base: int) -> str:
    if base < 2 or base > 62:
        raise ValueError("base must be between 2 and 62")
    if decimal == 0:
        return alphabet[0]
    baseN = ""
    while decimal:
        decimal, i = divmod(decimal, base)
        baseN = alphabet[i] + baseN
    return baseN


def binary_to_decimal(binary: str) -> int:
    return int(binary, 2)


def binary_to_hexadecimal(binary: str) -> str:
    return hex(int(binary, 2))[2:]


def binary_to_base64(binary: str) -> str:
    return base64.b64encode(
        int(binary, 2).to_bytes((len(binary) + 7) // 8, 'big')).decode()


def binary_to_base64url(binary: str) -> str:
    return base64.urlsafe_b64encode(
        int(binary, 2).to_bytes((len(binary) + 7) // 8, 'big')).decode()


def binary_to_base32(binary: str) -> str:
    return base64.b32encode(
        int(binary, 2).to_bytes((len(binary) + 7) // 8, 'big')).decode()


def binary_to_baseN(binary: str, base: int) -> str:
    if base < 2 or base > 62:
        raise ValueError("base must be between 2 and 62")
    if binary == "0":
        return alphabet[0]
    baseN = ""
    decimal = binary_to_decimal(binary)
    while decimal:
        decimal, i = divmod(decimal, base)
        baseN = alphabet[i] + baseN
    return baseN


def hexadecimal_to_decimal(hexadecimal: str) -> int:
    return int(hexadecimal, 16)


def hexadecimal_to_binary(hexadecimal: str) -> str:
    return bin(int(hexadecimal, 16))[2:]


def hexadecimal_to_base64(hexadecimal: str) -> str:
    return base64.b64encode(
        int(hexadecimal, 16).to_bytes((len(hexadecimal) + 1) // 2, 'big')).decode()


def hexadecimal_to_base64url(hexadecimal: str) -> str:
    return base64.urlsafe_b64encode(
        int(hexadecimal, 16).to_bytes((len(hexadecimal) + 1) // 2, 'big')).decode()


def hexadecimal_to_base32(hexadecimal: str) -> str:
    return base64.b32encode(
        int(hexadecimal, 16).to_bytes((len(hexadecimal) + 1) // 2, 'big')).decode()


def hexadecimal_to_baseN(hexadecimal: str, base: int) -> str:
    if base < 2 or base > 62:
        raise ValueError("base must be between 2 and 62")
    if hexadecimal == "0":
        return alphabet[0]
    baseN = ""
    decimal = hexadecimal_to_decimal(hexadecimal)
    while decimal:
        decimal, i = divmod(decimal, base)
        baseN = alphabet[i] + baseN
    return baseN


def base64_to_decimal(base64_: str) -> int:
    return int.from_bytes(base64.b64decode(base64_), 'big')


def base64_to_binary(base64_: str) -> str:
    return bin(int.from_bytes(base64.b64decode(base64_), 'big'))[2:]


def base64_to_hexadecimal(base64_: str) -> str:
    return hex(int.from_bytes(base64.b64decode(base64_), 'big'))[2:]


def base64_to_base64url(base64_: str) -> str:
    return base64.urlsafe_b64encode(base64.b64decode(base64_)).decode()


def base64_to_base32(base64_: str) -> str:
    return base64.b32encode(base64.b64decode(base64_)).decode()


def base64_to_baseN(base64_: str, base: int) -> str:
    if base < 2 or base > 62:
        raise ValueError("base must be between 2 and 62")
    if base64_ == "0":
        return alphabet[0]
    baseN = ""
    decimal = base64_to_decimal(base64_)
    while decimal:
        decimal, i = divmod(decimal, base)
        baseN = alphabet[i] + baseN
    return baseN


def base64url_to_decimal(base64url: str) -> int:
    return int.from_bytes(base64.urlsafe_b64decode(base64url), 'big')


def base64url_to_binary(base64url: str) -> str:
    return bin(int.from_bytes(base64.urlsafe_b64decode(base64url), 'big'))[2:]


def base64url_to_hexadecimal(base64url: str) -> str:
    return hex(int.from_bytes(base64.urlsafe_b64decode(base64url), 'big'))[2:]


def base64url_to_base64(base64url: str) -> str:
    return base64.b64encode(base64.urlsafe_b64decode(base64url)).decode()


def base64url_to_base32(base64url: str) -> str:
    return base64.b32encode(base64.urlsafe_b64decode(base64url)).decode()


def base64url_to_baseN(base64url: str, base: int) -> str:
    if base < 2 or base > 62:
        raise ValueError("base must be between 2 and 62")
    if base64url == "0":
        return alphabet[0]
    baseN = ""
    decimal = base64url_to_decimal(base64url)
    while decimal:
        decimal, i = divmod(decimal, base)
        baseN = alphabet[i] + baseN
    return baseN


def base32_to_decimal(base32: str) -> int:
    return int.from_bytes(base64.b32decode(base32), 'big')


def base32_to_binary(base32: str) -> str:
    return bin(int.from_bytes(base64.b32decode(base32), 'big'))[2:]


def base32_to_hexadecimal(base32: str) -> str:
    return hex(int.from_bytes(base64.b32decode(base32), 'big'))[2:]


def base32_to_base64(base32: str) -> str:
    return base64.b64encode(base64.b32decode(base32)).decode()


def base32_to_base64url(base32: str) -> str:
    return base64.urlsafe_b64encode(base64.b32decode(base32)).decode()


def base32_to_baseN(base32: str, base: int) -> str:
    if base < 2 or base > 62:
        raise ValueError("base must be between 2 and 62")
    if base32 == "0":
        return alphabet[0]
    baseN = ""
    decimal = base32_to_decimal(base32)
    while decimal:
        decimal, i = divmod(decimal, base)
        baseN = alphabet[i] + baseN
    return baseN


def baseN_to_decimal(baseN: str, base: int) -> int:
    if base < 2 or base > 62:
        raise ValueError("base must be between 2 and 62")
    return sum(alphabet.index(char) * base ** i for i, char in enumerate(reversed(baseN)))


def baseN_to_binary(baseN: str, base: int) -> str:
    return bin(baseN_to_decimal(baseN, base))[2:]


def baseN_to_hexadecimal(baseN: str, base: int) -> str:
    return hex(baseN_to_decimal(baseN, base))[2:]


def baseN_to_base64(baseN: str, base: int) -> str:
    return base64.b64encode(
        baseN_to_decimal(baseN, base).to_bytes(
            (baseN_to_decimal(baseN, base).bit_length() + 7) // 8, 'big')).decode()


def baseN_to_base64url(baseN: str, base: int) -> str:
    return base64.urlsafe_b64encode(
        baseN_to_decimal(baseN, base).to_bytes(
            (baseN_to_decimal(baseN, base).bit_length() + 7) // 8, 'big')).decode()


def baseN_to_base32(baseN: str, base: int) -> str:
    return base64.b32encode(
        baseN_to_decimal(baseN, base).to_bytes(
            (baseN_to_decimal(baseN, base).bit_length() + 7) // 8, 'big')).decode()
