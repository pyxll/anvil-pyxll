"""
This project bridges PyXLL and Anvil applications.

It enables Excel add-ins to be written in Python using PyXLL, but for the  Python code
to be executed remotely via Anvil.

For details about PyXLL, see https://www.pyxll.com, and for details about Anvil
see https://anvil.works.
"""
from .xl_func import register_xl_funcs
from pyxll import xl_on_open, xl_on_reload, get_config, rebind
import anvil.server
import logging

_log = logging.getLogger(__name__)


@xl_on_open
@xl_on_reload
def on_open(import_info):
    """Fetches and registers any remote Anvil functions"""
    cfg = get_config()
    token = cfg.get("ANVIL", "token", fallback="")
    if not token:
        _log.warning("No Anvil token found. No remove functions will be available.")
        return

    # Connect to the anvil server and register any functions
    anvil.server.connect(token)

    xl_funcs = anvil.server.call("pyxll.get_xl_funcs")
    if xl_funcs:
        register_xl_funcs(xl_funcs)
        rebind()
