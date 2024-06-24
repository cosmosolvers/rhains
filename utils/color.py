""""""


def hex_to_rgb(hex: str) -> tuple:
    hex = hex.lstrip('#')
    length = len(hex)
    return tuple(int(hex[i:i + length // 3], 16) for i in range(0, length, length // 3))

# Exemple
# print(hex_to_rgb("#FF0000"))  # (255, 0, 0)
# print(hex_to_rgb("#F00"))     # (255, 0, 0)


def rgb_to_hex(red: int, green: int, blue: int) -> str:
    return f'#{red:02X}{green:02X}{blue:02X}'

# Exemple
# print(rgb_to_hex(255, 0, 0))  # #FF0000


def rgb_to_hsl(red: int, green: int, blue: int) -> tuple:
    red, green, blue = red / 255.0, green / 255.0, blue / 255.0
    maxc = max(red, green, blue)
    minc = min(red, green, blue)
    lightness = (maxc + minc) / 2
    if maxc == minc:
        h = s = 0.0
    else:
        diff = maxc - minc
        s = diff / (2.0 - maxc - minc) if lightness > 0.5 else diff / (maxc + minc)
        d = {
            red: (green - blue) / diff + (6 if green < blue else 0),
            green: (blue - red) / diff + 2,
            blue: (red - green) / diff + 4
        }
        h = d[maxc] / 6
    return round(h * 360), round(s * 100), round(lightness * 100)

# Exemple
# print(rgb_to_hsl(255, 0, 0))  # (0, 100, 50)


def hsl_to_rgb(hue: int, saturation: int, lightness: int) -> tuple:
    hue, saturation, lightness = hue / 360.0, saturation / 100.0, lightness / 100.0

    def hue_to_rgb(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    if saturation == 0:
        r = g = b = lightness
    else:
        q = lightness * (1 + saturation)\
            if lightness < 0.5 else lightness + saturation - lightness * saturation
        p = 2 * lightness - q
        r = hue_to_rgb(p, q, hue + 1 / 3)
        g = hue_to_rgb(p, q, hue)
        b = hue_to_rgb(p, q, hue - 1 / 3)
    return round(r * 255), round(g * 255), round(b * 255)

# Exemple
# print(hsl_to_rgb(0, 100, 50))  # (255, 0, 0)


def rgba_to_hsla(read: int, green: int, blue: int, alpha: float) -> tuple:
    hue, saturation, lightness = rgb_to_hsl(read, green, blue)
    return hue, saturation, lightness, alpha

# Exemple
# print(rgba_to_hsla(255, 0, 0, 0.5))  # (0, 100, 50, 0.5)


def hsla_to_rgba(hue: int, saturation: int, lightness: int, aalpha: float) -> tuple:
    read, green, blue = hsl_to_rgb(hue, saturation, lightness)
    return read, green, blue, aalpha

# Exemple
# print(hsla_to_rgba(0, 100, 50, 0.5))  # (255, 0, 0, 0.5)
