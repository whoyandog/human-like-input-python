from human_input.layouts.en_us import resolve_key as resolve_en_key

RU_LAYOUT = {
    "ё": ("`", False), "Ё": ("`", True),
    "1": ("1", False), "2": ("2", False), "3": ("3", False), "4": ("4", False), "5": ("5", False),
    "6": ("6", False), "7": ("7", False), "8": ("8", False), "9": ("9", False), "0": ("0", False),
    "-": ("-", False), "=": ("=", False),
    "!": ("1", True), '"': ("2", True), "№": ("3", True), ";": ("4", True), "%": ("5", True),
    ":": ("6", True), "?": ("7", True), "*": ("8", True), "(": ("9", True), ")": ("0", True),
    "_": ("-", True), "+": ("=", True),
    "й": ("q", False), "ц": ("w", False), "у": ("e", False), "к": ("r", False), "е": ("t", False),
    "н": ("y", False), "г": ("u", False), "ш": ("i", False), "щ": ("o", False), "з": ("p", False),
    "х": ("[", False), "ъ": ("]", False),
    "Й": ("q", True), "Ц": ("w", True), "У": ("e", True), "К": ("r", True), "Е": ("t", True),
    "Н": ("y", True), "Г": ("u", True), "Ш": ("i", True), "Щ": ("o", True), "З": ("p", True),
    "Х": ("[", True), "Ъ": ("]", True),
    "ф": ("a", False), "ы": ("s", False), "в": ("d", False), "а": ("f", False), "п": ("g", False),
    "р": ("h", False), "о": ("j", False), "л": ("k", False), "д": ("l", False), "ж": (";", False),
    "э": ("'", False),
    "Ф": ("a", True), "Ы": ("s", True), "В": ("d", True), "А": ("f", True), "П": ("g", True),
    "Р": ("h", True), "О": ("j", True), "Л": ("k", True), "Д": ("l", True), "Ж": (";", True),
    "Э": ("'", True),
    "я": ("z", False), "ч": ("x", False), "с": ("c", False), "м": ("v", False), "и": ("b", False),
    "т": ("n", False), "ь": ("m", False), "б": (",", False), "ю": (".", False), ".": ("/", False),
    "Я": ("z", True), "Ч": ("x", True), "С": ("c", True), "М": ("v", True), "И": ("b", True),
    "Т": ("n", True), "Ь": ("m", True), "Б": (",", True), "Ю": (".", True), ",": ("/", True),
}


def resolve_key(char):
    if char in RU_LAYOUT:
        return RU_LAYOUT[char]

    return resolve_en_key(char)
