from typing import Callable, Dict, List, Any

MODULE_REGISTRY: Dict[str, List[Dict[str, Any]]] = {}

def Module(
    *,
    module_type: str,
    proxies_required: bool = False,
    module_data: Any = None
) -> Callable:
    def decorator(func: Callable) -> Callable:
        MODULE_REGISTRY.setdefault(module_type, []).append({
            'func': func,
            'proxies_required': proxies_required,
            'module_data': module_data,
            'name': func.__name__,
            'module': func.__module__,
        })
        return func
    return decorator
