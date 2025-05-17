import os
from datetime import datetime

class Print:
    timestamp: bool = False
    LEVEL_COLORS = {
        'DEBUG': '94',    # blue
        'INFO': '92',     # green
        'WARNING': '93',  # yellow
        'ERROR': '91',    # red
    }

    @staticmethod
    def _timestamp_str() -> str:
        now = datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def _format_level(level: str, width: int) -> str:
        return level.ljust(width)

    @classmethod
    def _log(cls, text: str, level: str):
        lvl = level.upper()
        color = cls.LEVEL_COLORS.get(lvl, '0')
        lvl_fmt = cls._format_level(lvl, 7)
        ts = f"[{cls._timestamp_str()}] " if cls.timestamp else ''
        print(f"{ts}\x1b[{color}m[{lvl_fmt}]\x1b[0m • {text}")

    @classmethod
    def log(cls, text: str, level: str = 'INFO') -> None:
        cls._log(text, level)

    @staticmethod
    def _print_tree(key, value, indent=0, is_last=True):
        space       = '    '
        branch      = '└─' if is_last else '├─'
        dot_prefix  = '• '
        indent_str  = ''

        for i in range(indent):
            indent_str += ('│   ' if i < indent else space)

        prefix = indent_str + branch + dot_prefix

        if isinstance(value, dict):
            print(f"{prefix}\x1b[92m{key}\x1b[0m")
            last_key = list(value.keys())[-1] if value else None
            for idx, (k, v) in enumerate(value.items()):
                is_last_child = (k == last_key)
                Print._print_tree(k, v, indent + 1, is_last_child)
        elif isinstance(value, list):
            print(f"{prefix}\x1b[92m{key}\x1b[0m")
            for i, item in enumerate(value):
                is_last_child = (i == len(value) - 1)
                Print._print_tree(f"[{i}]", item, indent + 1, is_last_child)
        else:
            color_code = '90'
            if isinstance(value, bool):
                color_code = '92' if value else '91'
                value = 'Yes' if value else 'No'
            elif isinstance(value, (int, float)):
                color_code = '93'
            elif isinstance(value, str) and value.strip() == '':
                return # skip empty strings or things break

            print(f"{prefix}\x1b[92m{key}:\x1b[0m \x1b[{color_code}m{value}\x1b[0m")

    @classmethod
    def prettify(cls, results):
        if not isinstance(results, (list, tuple)):
            if not isinstance(results, dict):
                raise Exception('Print.prettify() requires a dict or list of dicts')
            results = [results]

        for idx, result in enumerate(results):
            if not isinstance(result, dict):
                continue
            print(f"\x1b[94mResult {idx + 1}:\x1b[0m")
            last_key = list(result.keys())[-1] if result else None
            for i, (k, v) in enumerate(result.items()):
                is_last = (k == last_key)
                cls._print_tree(k, v, indent=0, is_last=is_last)
            print()
