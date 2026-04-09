EN_SYMBOLS = {
    " ": (" ", False),
    "-": ("-", False), "_": ("-", True),
    "=": ("=", False), "+": ("=", True),
    "[": ("[", False), "{": ("[", True),
    "]": ("]", False), "}": ("]", True),
    "\\": ("\\", False), "|": ("\\", True),
    ";": (";", False), ":": (";", True),
    "'": ("'", False), '"': ("'", True),
    ",": (",", False), "<": (",", True),
    ".": (".", False), ">": (".", True),
    "/": ("/", False), "?": ("/", True),
    "`": ("`", False), "~": ("`", True),
    "!": ("1", True), "@": ("2", True), "#": ("3", True), "$": ("4", True), "%": ("5", True),
    "^": ("6", True), "&": ("7", True), "*": ("8", True), "(": ("9", True), ")": ("0", True),
    "\n": ("\n", False),
}


def resolve_key(char):
    if char in EN_SYMBOLS:
        return EN_SYMBOLS[char]

    if "a" <= char <= "z":
        return (char, False)
    if "A" <= char <= "Z":
        return (char.lower(), True)
    if "0" <= char <= "9":
        return (char, False)

    return None
