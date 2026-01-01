# Rich Console Utilities

A small utility module built on top of [Rich](https://github.com/Textualize/rich) for producing **colourful, readable, and structured console output**.

The main contens are:
* A drop-in replacement for `print`
* A decorator for running functions with a spinner/status indicator like ```npm```

***
## Usage

### ✨ Pretty Printing
```print```: A drop-in replacement for built-in `print`, prints colourful repr with indentation & guidelines 


### 🔄 Status Decorator
```show_status```
Runs decorated function with status spinner like ```npm```
Example usage:
```
@show_status("running", exit_message="finished")
def f():
    for i in range(3):
        time.sleep(0.5)
        print('loop', i)
f()
```

* Automatically disabled for instances with attribute `_show_status = False`

---

## Installation

This module depends on **Rich**:

```bash
pip install themed-print
```

---


## Usage

```python
from themed_print import print, show_status
```

---

### Pretty Print (Drop-in Replacement)

```python
print({
    "name": "Alice",
    "values": [1, 2, 3],
    "active": True,
})
```

With custom indentation:

```python
print(data, indent=2, show_guideline=True)
```

Arguments:

| Parameter        | Type | Description              |
| ---------------- | ---- | ------------------------ |
| `content`        | Any  | Objects to print         |
| `indent`         | int  | Spaces per indent level  |
| `show_guideline` | bool | Show indentation guides  |
| `sep`            | str  | Separator between values |
| `end`            | str  | Line ending              |

---

### Status Spinner Decorator

Run a function with a live spinner:

```python
import time

@show_status("Running task…", exit_message="Done ✔")
def task():
    for i in range(3):
        time.sleep(0.5)
        print("step", i)

task()
```

Supported parameters:

| Parameter            | Description                                 |
| -------------------- | ------------------------------------------- |
| `status_message`     | Message shown while running                 |
| `exit_message`       | Message printed after completion            |
| `exit_message_style` | Rich style for exit message                 |
| `spinner`            | Spinner name (see `python -m rich.spinner`) |
| `**status_kwargs`    | Passed to `Console.status()`                |

#### Instance Method Behaviour

If the decorated function is an **instance method**, logging is skipped when:

```python
self._show_status = False
```

This allows silent execution in batch or test modes.

### Customisation 

The colour schemed is implemented through ```rich.theme.Theme``` object with customised regex highlighter ```themed_print.DTypeRegexHighlighter```.

Currently, colour schemes are defined in ```themed_print.config.DEFAULT_THEME``` Support for custom theming is planned for future releases.


## Author

**Yiheng Yu**
Created: Jan 1, 2025

