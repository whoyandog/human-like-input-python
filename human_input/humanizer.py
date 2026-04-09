import random

from human_input.layouts import build_neighbor_map
from human_input.layouts import resolve_layout_key
from human_input.protocol import HIDCommand as HC
from human_input.protocol import HIDKey as HK
from human_input.protocol import AppCommand as AC


class Humanizer:
    def __init__(self, typing_settings):
        cfg = typing_settings or {}
        self.layout = str(cfg.get("layout", "en")).lower()
        self.wpm = max(10.0, float(cfg.get("speed", 85.0)))
        self.error_rate = max(0.0, min(0.25, float(cfg.get("error_rate", 0.03))))

        timing_cfg = cfg.get("timing", {})
        self.timing_std_ratio = self._bounded_float(timing_cfg.get("interval_std_ratio", 0.30), 0.01, 1.00)
        self.min_interval = self._bounded_float(timing_cfg.get("min_interval", 0.015), 0.001, 0.500)
        self.space_pause_min = self._bounded_float(timing_cfg.get("space_pause_min", 0.08), 0.001, 3.000)
        self.space_pause_max = self._bounded_float(timing_cfg.get("space_pause_max", 0.24), self.space_pause_min, 5.000)
        self.typo_reaction_min = self._bounded_float(timing_cfg.get("typo_reaction_min", 0.12), 0.001, 5.000)
        self.typo_reaction_max = self._bounded_float(timing_cfg.get("typo_reaction_max", 0.38), self.typo_reaction_min, 8.000)

        self.shift_down_multiplier = self._bounded_float(timing_cfg.get("shift_down_multiplier", 0.45), 0.05, 3.00)
        self.key_hold_multiplier = self._bounded_float(timing_cfg.get("key_hold_multiplier", 0.70), 0.05, 3.00)
        self.shift_up_multiplier = self._bounded_float(timing_cfg.get("shift_up_multiplier", 0.30), 0.05, 3.00)
        self.post_key_multiplier = self._bounded_float(timing_cfg.get("post_key_multiplier", 1.00), 0.05, 5.00)
        self.backspace_hold_multiplier = self._bounded_float(timing_cfg.get("backspace_hold_multiplier", 0.55), 0.05, 5.00)
        self.post_backspace_multiplier = self._bounded_float(timing_cfg.get("post_backspace_multiplier", 0.85), 0.05, 5.00)

        default_shift_lead_min = max(0.05, self.shift_down_multiplier * 0.65)
        default_shift_lead_max = max(default_shift_lead_min, self.shift_down_multiplier * 3.10)
        default_shift_lag_min = max(0.05, self.shift_up_multiplier * 0.35)
        default_shift_lag_max = max(default_shift_lag_min, self.shift_up_multiplier * 3.50)

        self.shift_lead_min_multiplier = self._bounded_float(
            timing_cfg.get("shift_lead_min_multiplier", default_shift_lead_min), 0.05, 5.00
        )
        self.shift_lead_max_multiplier = self._bounded_float(
            timing_cfg.get("shift_lead_max_multiplier", default_shift_lead_max), self.shift_lead_min_multiplier, 6.00
        )
        self.shift_release_lag_min_multiplier = self._bounded_float(
            timing_cfg.get("shift_release_lag_min_multiplier", default_shift_lag_min), 0.05, 5.00
        )
        self.shift_release_lag_max_multiplier = self._bounded_float(
            timing_cfg.get("shift_release_lag_max_multiplier", default_shift_lag_max), self.shift_release_lag_min_multiplier, 6.00
        )
        self.shift_sticky_probability = self._bounded_float(
            timing_cfg.get("shift_sticky_probability", 0.035), 0.0, 1.0
        )
        self.shift_sticky_correction_probability = self._bounded_float(
            timing_cfg.get("shift_sticky_correction_probability", 0.85), 0.0, 1.0
        )

        self.base_keystroke = 60.0 / (self.wpm * 5.0)
        self._neighbor_map = build_neighbor_map()

    @staticmethod
    def _bounded_float(value, min_value, max_value):
        result = float(value)
        if result < min_value:
            return min_value
        if result > max_value:
            return max_value
        return result

    def _resolve_key(self, char):
        return resolve_layout_key(self.layout, char)

    def _sample_interval(self, multiplier=1.0):
        mean = self.base_keystroke * multiplier
        dt = random.gauss(mean, mean * self.timing_std_ratio)
        return max(self.min_interval, dt)

    def _sample_space_pause(self):
        return random.uniform(self.space_pause_min, self.space_pause_max)

    def _sample_shift_lead(self):
        # Bias to longer lead time to avoid robotic "exactly together" Shift.
        multiplier = random.triangular(
            self.shift_lead_min_multiplier,
            self.shift_lead_max_multiplier,
            self.shift_lead_max_multiplier,
        )
        return self._sample_interval(multiplier)

    def _sample_shift_release_lag(self):
        multiplier = random.triangular(
            self.shift_release_lag_min_multiplier,
            self.shift_release_lag_max_multiplier,
            self.shift_release_lag_max_multiplier,
        )
        return self._sample_interval(multiplier)

    def _emit_key_press_release(self, key_char):
        yield (HC.KEY_DOWN, ord(key_char))
        yield (AC.WAIT, self._sample_interval(self.key_hold_multiplier))
        yield (HC.KEY_UP, ord(key_char))

    def _emit_shift_down(self):
        yield (HC.KEY_DOWN, HK.LEFT_SHIFT)
        yield (AC.WAIT, self._sample_shift_lead())

    def _emit_shift_up(self):
        yield (AC.WAIT, self._sample_shift_release_lag())
        yield (HC.KEY_UP, HK.LEFT_SHIFT)

    def _emit_press_release(self, key_char, use_shift=False):
        if use_shift:
            for item in self._emit_shift_down():
                yield item

        for item in self._emit_key_press_release(key_char):
            yield item

        if use_shift:
            for item in self._emit_shift_up():
                yield item

    def _emit_typo_then_correction(self, key_char, use_shift):
        wrong_candidates = self._neighbor_map.get(key_char, [])
        if not wrong_candidates:
            return

        wrong_key = random.choice(wrong_candidates)

        for item in self._emit_press_release(wrong_key, use_shift=False):
            yield item

        yield (AC.WAIT, random.uniform(self.typo_reaction_min, self.typo_reaction_max))

        yield (HC.KEY_DOWN, HK.BACKSPACE)
        yield (AC.WAIT, self._sample_interval(self.backspace_hold_multiplier))
        yield (HC.KEY_UP, HK.BACKSPACE)
        yield (AC.WAIT, self._sample_interval(self.post_backspace_multiplier))

        for item in self._emit_press_release(key_char, use_shift=use_shift):
            yield item

    def process_text(self, text):
        shift_is_down = False
        sticky_shift_pending = False

        for char in text:
            resolved = self._resolve_key(char)
            if resolved is None:
                continue

            key_char, use_shift = resolved

            accidental_shift_capture = (
                sticky_shift_pending and not use_shift and key_char not in (" ", "\n")
            )
            effective_shift = use_shift or accidental_shift_capture

            if effective_shift and not shift_is_down:
                for item in self._emit_shift_down():
                    yield item
                shift_is_down = True

            if random.random() < self.error_rate and key_char != " " and key_char != "\n":
                for item in self._emit_typo_then_correction(key_char, use_shift):
                    yield item
            else:
                for item in self._emit_key_press_release(key_char):
                    yield item

            if accidental_shift_capture:
                sticky_shift_pending = False
                if random.random() < self.shift_sticky_correction_probability:
                    yield (AC.WAIT, random.uniform(self.typo_reaction_min, self.typo_reaction_max))
                    yield (HC.KEY_DOWN, HK.BACKSPACE)
                    yield (AC.WAIT, self._sample_interval(self.backspace_hold_multiplier))
                    yield (HC.KEY_UP, HK.BACKSPACE)

                    for item in self._emit_shift_up():
                        yield item
                    shift_is_down = False

                    yield (AC.WAIT, self._sample_interval(self.post_backspace_multiplier))
                    for item in self._emit_key_press_release(key_char):
                        yield item

            if use_shift and shift_is_down:
                if random.random() < self.shift_sticky_probability:
                    sticky_shift_pending = True
                else:
                    for item in self._emit_shift_up():
                        yield item
                    shift_is_down = False

            if (not use_shift) and shift_is_down and (not sticky_shift_pending):
                for item in self._emit_shift_up():
                    yield item
                shift_is_down = False

            if key_char == " ":
                yield (AC.WAIT, self._sample_space_pause())
            else:
                yield (AC.WAIT, self._sample_interval(self.post_key_multiplier))

        if shift_is_down:
            for item in self._emit_shift_up():
                yield item

        yield (HC.KEY_RELEASE_ALL, 0)
