import random

from human_input.protocol import HIDCommand as HC
from human_input.protocol import HIDKey as HK
from human_input.protocol import AppCommand as AC


class Humanizer:
    _RU_LAYOUT = {
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

    _EN_SYMBOLS = {
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

    _QWERTY_GRID = [
        "`1234567890-=",
        "qwertyuiop[]\\",
        "asdfghjkl;'",
        "zxcvbnm,./",
    ]

    def __init__(self, typing_settings=None):
        cfg = typing_settings or {}
        self.layout = str(cfg.get("layout", "en")).lower()
        self.wpm = max(10.0, float(cfg.get("speed", 90.0)))
        self.error_rate = max(0.0, min(0.25, float(cfg.get("error_rate", 0.03))))
        self.base_keystroke = 60.0 / (self.wpm * 5.0)
        self._neighbor_map = self._build_neighbor_map()

    def _build_neighbor_map(self):
        pos = {}
        for row_idx, row in enumerate(self._QWERTY_GRID):
            for col_idx, key in enumerate(row):
                pos[key] = (row_idx, col_idx)

        neighbors = {}
        for key, (row_idx, col_idx) in pos.items():
            points = []
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr = row_idx + dr
                    nc = col_idx + dc
                    if 0 <= nr < len(self._QWERTY_GRID):
                        row = self._QWERTY_GRID[nr]
                        if 0 <= nc < len(row):
                            points.append(row[nc])
            if points:
                neighbors[key] = points
        return neighbors

    def _resolve_key(self, char):
        if self.layout.startswith("ru") and char in self._RU_LAYOUT:
            return self._RU_LAYOUT[char]

        if char in self._EN_SYMBOLS:
            return self._EN_SYMBOLS[char]

        if "a" <= char <= "z":
            return (char, False)
        if "A" <= char <= "Z":
            return (char.lower(), True)
        if "0" <= char <= "9":
            return (char, False)

        return None

    def _sample_interval(self, multiplier=1.0):
        mean = self.base_keystroke * multiplier
        dt = random.gauss(mean, mean * 0.30)
        return max(0.015, dt)

    def _sample_space_pause(self):
        return random.uniform(0.08, 0.24)

    def _emit_press_release(self, key_char, use_shift=False):
        if use_shift:
            yield (HC.KEY_DOWN, HK.LEFT_SHIFT)
            yield (AC.WAIT, self._sample_interval(0.45))

        yield (HC.KEY_DOWN, ord(key_char))
        yield (AC.WAIT, self._sample_interval(0.70))
        yield (HC.KEY_UP, ord(key_char))

        if use_shift:
            yield (AC.WAIT, self._sample_interval(0.30))
            yield (HC.KEY_UP, HK.LEFT_SHIFT)

    def _emit_typo_then_correction(self, key_char, use_shift):
        wrong_candidates = self._neighbor_map.get(key_char, [])
        if not wrong_candidates:
            return

        wrong_key = random.choice(wrong_candidates)

        for item in self._emit_press_release(wrong_key, use_shift=False):
            yield item

        yield (AC.WAIT, random.uniform(0.12, 0.38))

        yield (HC.KEY_DOWN, HK.BACKSPACE)
        yield (AC.WAIT, self._sample_interval(0.55))
        yield (HC.KEY_UP, HK.BACKSPACE)
        yield (AC.WAIT, self._sample_interval(0.85))

        for item in self._emit_press_release(key_char, use_shift=use_shift):
            yield item

    def process_text(self, text):
        for char in text:
            resolved = self._resolve_key(char)
            if resolved is None:
                continue

            key_char, use_shift = resolved

            if random.random() < self.error_rate and key_char != " " and key_char != "\n":
                for item in self._emit_typo_then_correction(key_char, use_shift):
                    yield item
            else:
                for item in self._emit_press_release(key_char, use_shift):
                    yield item

            if key_char == " ":
                yield (AC.WAIT, self._sample_space_pause())
            else:
                yield (AC.WAIT, self._sample_interval(1.00))

        yield (HC.KEY_RELEASE_ALL, 0)
