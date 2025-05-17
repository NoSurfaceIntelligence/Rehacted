# NoSINT.org — Development Guide

Welcome, Agent.
This repository provides a modular, Python-based framework derived from the proprietary NoSINT.org platform. It allows analysts and automated agents to execute targeted modules against specific platforms or objectives. This guide outlines how to build, structure, and integrate new modules into the system effectively.
---

## Get Started
- Install Requirements
    ```sh
    pip install -r requirements.txt
    ```

- Run Our Example
    ```sh
    cd ./src
    python main.py info_exposure megadose@protonmail.com
    ```

## Module Structure

All modules should be Python scripts that define a function or class that can be called with a common interface.

### Minimal Example

```python
def run(session, query, *args, **kwargs):
    return {
        'module': 'freelancer.recovery',
        'query': query,
        'is_valid': True,
        'result': {
            'display_name': 'John Doe',
            'username': 'johndoe123',
            'last_seen': '2025-05-17',
        },
    }
```

### File Structure Example

```text
modules/
└── freelancer.py -- # contains run()
```

---

## Best Practices

- **Modularize** by platform (e.g., 'freelancer', 'reddit', 'linkedin').
- Use the function signature 'run(session, query, *args, **kwargs)' as the standard callable.
- Return a dictionary with keys:
  - `module`: `str` – module identifier
  - `query`: `str` – original input
  - `is_valid`: `bool` – validity of the result
  - `results`: `dict` – structured output
- Keep functions **pure** where possible (avoid side-effects).
- Avoid unnecessary dependencies.
- Use the provided 'Print' class to log or output data.

---

## Output Format

All modules should return a dict with the following shape:

```python
{
    'module': 'namespace.identifier',
    'query':  'original input query',
    'is_valid': True,
    'result': {
        'key1': 'value',
        'key2': 42,
        'nested': {
            'item': 'subvalue'
        }
    }
}
```

This allows the output to be parsed and visualized in a clean tree-style with the built-in 'Print.prettify()' function.

---

### Session Usage Example

```python
from _util import Session, Print

requests = Session()

def run(query):
    url = f'https://example.com/api/user/{query}'
    response = requests.get(url)

    if response.status_code != 200:
        return {
            'module': 'example.module',
            'query': query,
            'is_valid': False,
            'result': {
                'error': response.status_code
            }
        }

    data = response.json()

    return {
        'module': 'example.module',
        'query': query,
        'is_valid': True,
        'result': {
            'username': data.get('username'),
            'email_verified': data.get('email_verified')
        }
    }
```

---

## Testing Your Module

You can test modules locally using:

```bash
python main.py <module_type> <target>
```

---

## Submitting Plugins

So, you think your module is worth adding to NoSINT?
- Test thoroughly.
- Ensure output conforms to schema.
- Follow naming conventions: 'platform.action.py' (e.g., 'freelancer.recovery').
- Submit a pull request with your modules.

---

🧠 Happy hunting, Rehacted Agent.
