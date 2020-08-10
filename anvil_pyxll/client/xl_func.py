import pyxll
import anvil.server
from itertools import chain
from functools import wraps


def register_xl_funcs(xl_funcs):
    """Register remote Anvil functions to be called as Excel functions"""
    for kwargs in xl_funcs:
        anvil_name = kwargs.pop("anvil_name")
        func_name = kwargs.pop("func_name")
        args = kwargs.pop("args", None) or []
        varargs = kwargs.pop("varargs", None)
        defaults = kwargs.pop("defaults", None) or []

        # Build a function that looks like the one on the remote server
        args_without_defaults = [a for a in args[:len(args) - len(defaults)]]
        args_with_defaults = [f"{a}={a}" for a in args[len(args) - len(defaults):]]
        varargs = [f"*{varargs}"] if varargs else []

        doc = kwargs.pop("doc", None) or ""
        if doc:
            doc = '\n    """' + doc + '"""\n    '

        args_str = ", ".join(chain(args_without_defaults, args_with_defaults, varargs))
        func_str = f"def {func_name}({args_str}):{doc}pass"

        ns = {}
        if defaults:
            ns = {a: d for a, d in zip(reversed(args), reversed(defaults))}

        exec(func_str, {}, ns)
        dummy_func = ns[func_name]

        def make_wrapper(template_func, func_name):
            @wraps(template_func)
            def wrapper_function(*args):
                return anvil.server.call(func_name, *args)
            return wrapper_function

        wrapper_function = make_wrapper(dummy_func, anvil_name)
        wrapper_function.__name__ = func_name
        pyxll.xl_func(**kwargs)(wrapper_function)
