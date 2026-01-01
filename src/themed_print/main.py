"""
Functions & dependencies for printing colourfull outputs to the console

Created on Mon Dec  8 12:18:41 2025

@author: Yiheng Yu
"""

from functools import wraps, partial
from typing import Any, Optional

from rich import markup, pretty
from rich.console import Console, ConsoleRenderable, List, RenderHook
from rich.highlighter import RegexHighlighter, Highlighter
from rich.text import Text

from .config import DEFAULT_THEME

### Pretty printing
class _PrettyIndentHook(RenderHook):
    """
    RenderHook hook for format pretty-printing
    """

    def __init__(
        self,
        indent_size: int = 4,
        indent_guides: bool = False,
    ):
        """
        Args:
            indent_size (int, optional): Number of spaces in indent. Defaults to 4.
            indent_guides (bool, optional) – Enable indentation guides. Defaults to False.
        """
        self.indent_size = indent_size
        self.indent_guides = indent_guides

    def process_renderables(
        self, renderables: List[ConsoleRenderable]
    ) -> List[ConsoleRenderable]:
        processed = []
        for item in renderables:
            if isinstance(item, pretty.Pretty):
                item.indent_size = self.indent_size
                item.indent_guides = self.indent_guides
            processed.append(item)

        return processed


### Highlighter
# highlighter for regex match different data types
class DTypeRegexHighlighter(RegexHighlighter):
    base_stype = "dtype."
    highlights = [
        r"(?P<CONSTANT>(\s[A-Z_]*(?=[\s,])))",  # captalised texts (i.e., environment variables)
        r"(?<![\\\w])(?P<STR>b?'''.*?(?<!\\)'''|b?'.*?(?<!\\)'|b?\"\"\".*?(?<!\\)\"\"\"|b?\".*?(?<!\\)\")",
        r"(?P<NUMBER>(?<!\w)\-?[0-9]+\.?[0-9]*(e[-+]?\d+?)?\b|0x[0-9a-fA-F]*)",
        r"(?P<TRUE>True)",  # boolean
        r"(?P<FALSE>False)",  # boolean
        r"(?P<NONE>None)",  # None
        r"(?P<ENUM>[A-z]*\.[A-Z_]*(?=:))",  # Enums, flags etc.,
        r"(?P<DATACLASS_NAME>[A-z]*(?=\())",  # dataclass
        r"(?P<DICT_KEY>'.*'): ",  # dictionary key
        r"(?P<PUNCTUATION>[^\w\s\d])",  # punctuation
        r"^\[(?P<HOUR>2[0-3]|[01][0-9])\:(?P<MINUTE>[0-5][0-9])\:(?P<SECOND>[0-5][0-9])\]",  # logging datetime regex
        r"<function (?P<FUNCTION_NAME>[^\s]+) at (?P<HEX_ADDRESS>[a-zA-Z0-9]+)>",
        r"<(?P<INSTANCE_CLS>[^\s]+) object at (?P<HEX_ADDRESS>[a-zA-Z0-9]+)>",
        r"<class '(?P<CLASS>[\w\.]+)'>",
        r"<module '(?P<MODULE>[^\s]+)'",
        r"from '(?P<MODULE_FROM>[^\s]+)'>",
    ]

### Timestamp
def format_timestamp(highlighter_:Highlighter, input_datetime):
    """Formatting function for timestamp used in rich.Console.log"""
    formatted = input_datetime.strftime("[%X]")
    formatted = Text(formatted)
    return highlighter_(formatted)

### Console instance
HIGHLIGHTER = DTypeRegexHighlighter()
format_timestamp_ = partial(format_timestamp, HIGHLIGHTER)
theme = DEFAULT_THEME  # TODO: make themes customisable
CONSOLE = Console(
    color_system="truecolor",
    highlight=True,
    highlighter=HIGHLIGHTER,
    theme=theme,
    log_time_format=format_timestamp_,
    log_path=False,
)


### Functions
def print(
    *content: Any,
    indent: int = 4,
    show_guideline: bool = True,
    sep: str = " ",
    end: str = "\n",
) -> None:
    """
    Print colourful, formatted contents to the console

    Args:
        content (Any): objects to be pretty-printed.
        indent (int, optional): Number of spaces to use for indentation in
            nested structures. Defaults to 1.
        show_guideline (bool, optional): Whether to print indent guidelines when possible. Defaults to True.
        sep (str, optional): String inserted between values when printing.
            Passed through to `CONSOLE.print`. Defaults to ` `.
        end (str, optional): String appended after the last value.
            Passed through to `CONSOLE.print`. Defaults to `\n`.

    Returns:
        None
    """
    # adding
    to_print = [markup.escape(cnt) if isinstance(cnt, str) else cnt for cnt in content]

    # format pretty printing
    hook = _PrettyIndentHook(indent_size=indent, indent_guides=show_guideline)
    CONSOLE.push_render_hook(hook) 
    CONSOLE.print(*to_print, sep=sep, end=end)
    # ..and put everything back to normal
    CONSOLE.pop_render_hook()


def show_status(
    status_message: str | Text,
    exit_message: Optional[str | Text] = None,
    exit_message_style: str = "dark_sea_green1",
    spinner: str = "dots",
    **status_kwargs,
):
    """
    Decorator that runs the decorated function with spinner (like npm)

    If the decorated function is an instance method, the decorator first checks
    for an instance attribute named `_show_status`. If this attribute exists and
    is set to `False`, the function is executed normally without displaying
    the status spinner or exit message.

    Example usage:

    import time
    @show_status("running", exit_message="finished")
    def f():
        for i in range(3):
            time.sleep(0.5)
            print('loop', i)
    f()

    status_message: str|Text,
        status message
    exit_message: str|Text, default None
        exit message
    exit_message_style: str, default 'dark_sea_green1'
        text style for the exit message
    spinner: str, default None
        rich spinner.
        Run python -m rich.spinner to preview all spinners
    status_kwargs:
        other kwargs to pass to rich.console.Console.status() init call
    """
    if exit_message is None:
        exit_message = status_message

    def wrapper(func):
        @wraps(func)
        def run_as_status(*args, **kwargs):
            # If the input func is a instance method, we first check if the instance attrbute '_show_status'
            # skip logging output if _show_status attribute set to be False.
            # ** for instance methods, the first inputs would always be 'self'
            if args:
                instance = args[0]
                should_log = getattr(instance, "_show_status", True)
            else:
                should_log = True

            if should_log is False:
                function_output = func(*args, **kwargs)
                return function_output

            with CONSOLE.status(status_message, spinner=spinner, **status_kwargs):
                function_output = func(*args, **kwargs)

            CONSOLE.print(exit_message, style=exit_message_style)
            return function_output

        return run_as_status

    return wrapper
