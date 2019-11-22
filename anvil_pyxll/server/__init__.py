"""
Server side part of the Anvil-PyXLL integration.

Example usage::

    from anvil_pyxll.server import xl_func

    @xl_func
    def function_to_expose_to_excel(args):
        pass
"""
import anvil.server
import inspect

_xl_funcs = {}


def xl_func(signature=None,
            category="PyXLL",
            help_topic="",
            thread_safe=False,
            macro=False,
            allow_abort=None,
            volatile=None,
            disable_function_wizard_calc=False,
            disable_replace_calc=False,
            name=None,
            auto_resize=False,
            hidden=False,
            anvil_name=None):
    """
    xl_func is decorator used to expose python functions to Excel.
    Functions exposed in this way can be called from formulas in an Excel worksheet and
    appear in the Excel function wizard.
    See pyxll.xl_func for full details.
    """
    # xl_func may be called with no arguments as a plain decorator, in which
    # case the first argument will be the function it's applied to.
    func = None
    if signature is not None and callable(signature):
        func = signature
        signature = None

    def xl_func_decorator(func):
        # Register the function with Anvil
        anvil_name = "pyxll.xl_func." + func.__module__ + "." + func.__name__
        func = anvil.server.callable(anvil_name)(func)

        # Build the dict to be passed back to Excel
        xl_name = name or func.__name__
        getargspec = inspect.getfullargspec if hasattr(inspect, "getfullargspec") else inspect.getargspec
        spec = getargspec(func)
        func_info = {
            "anvil_name": anvil_name,
            "func_name": func.__name__,
            "args": spec.args,
            "varargs": spec.varargs,
            "defaults": spec.defaults if spec.defaults else None,
            "doc": func.__doc__,
            "signature": signature,
            "category": category,
            "help_topic": help_topic,
            "thread_safe": thread_safe,
            "macro": macro,
            "allow_abort": allow_abort,
            "volatile": volatile,
            "disable_function_wizard_calc": disable_function_wizard_calc,
            "disable_replace_calc": disable_replace_calc,
            "name": xl_name,
            "auto_resize": auto_resize,
            "hidden": hidden
        }

        _xl_funcs[xl_name] = func_info
        return func

    if func is not None:
        return xl_func_decorator(func)

    return xl_func_decorator


@anvil.server.callable("pyxll.get_xl_funcs")
def _get_xl_funcs():
  """Return all functions registered as PyXLL functions in Anvil
  """
  return list(_xl_funcs.values())
