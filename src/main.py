#!/usr/bin/env python3

import sys
import os
import importlib.util
from typing import Callable, Dict, List, Any
from _util import Print
from _types import Module
from _types.module import MODULE_REGISTRY

def load_modules(path: str = 'modules') -> None:
    """
    Load all .py files in the given modules directory and register them.
    """
    for filename in os.listdir(path):
        if not filename.endswith('.py') or filename.startswith('_'):
            continue
        module_path = os.path.join(path, filename)
        module_name = filename[:-3]
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module) # type: ignore

def run(
    module_type: str,
    *args,
    use_proxies: bool = False,
    **kwargs
) -> None:
    load_modules()

    try:
        raw_results = _run_modules_by_type(module_type, *args, use_proxies=use_proxies, **kwargs)
    except Exception as e:
        Print.log("Error", str(e), level='ERROR')
        sys.exit(1)

    for entry in raw_results:
        result = entry['result']

        if not isinstance(result, dict) or 'is_valid' not in result:
            Print.log("Module", entry['name'] + ": missing is_valid", level='DEBUG')
            continue

        level = 'INFO' if result.get('is_valid') else 'ERROR'

        Print.prettify({
            'module': entry['name'],
            'is_valid': result['is_valid'],
            'result': result.get('results')
        })


def _run_modules_by_type(
    module_type: str,
    *args,
    use_proxies: bool = False,
    **kwargs
) -> List[Any]:
    results = []
    for entry in MODULE_REGISTRY.get(module_type, []):
        if entry['proxies_required'] and not use_proxies:
            raise RuntimeError(
                f"Module {entry['name']} requires proxies but use_proxies=False"
            )

        func = entry['func']
        data = entry['module_data']

        if data is not None: result = func(data, *args, **kwargs)
        else: result = func(*args, **kwargs)

        results.append({
            'module': entry['module'],
            'name': entry['name'],
            'result': result,
        })

    return results

if __name__ == '__main__':
    use_proxies = False

    if len(sys.argv) < 3:
        Print.log("Usage: main.py <module_type> <arg1> [--use-proxies]", level='ERROR')
        sys.exit(1)

    mtype = sys.argv[1]
    cli_args = []
    
    for arg in sys.argv[2:]:
        if arg == '--use-proxies': use_proxies = True
        else: cli_args.append(arg)

    run(mtype, *cli_args, use_proxies=use_proxies)