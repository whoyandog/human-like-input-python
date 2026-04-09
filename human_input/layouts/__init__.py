from human_input.layouts.en_us import resolve_key as resolve_en_key
from human_input.layouts.ru_jcuken import resolve_key as resolve_ru_key
from human_input.layouts.topology import QWERTY_GRID, build_neighbor_map


def resolve_layout_key(layout, char):
    layout_name = str(layout or "en").lower()

    if layout_name.startswith("ru"):
        return resolve_ru_key(char)

    return resolve_en_key(char)


__all__ = ["resolve_layout_key", "QWERTY_GRID", "build_neighbor_map"]
