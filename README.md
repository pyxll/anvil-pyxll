# Anvil-PyXLL

This project bridges PyXLL and Anvil applications.

It enables Excel add-ins to be written in Python using PyXLL, but for the  Python code
to be executed remotely via Anvil.

For details about PyXLL, see https://www.pyxll.com, and for details about Anvil
see https://anvil.works.

## Usage

Create an Anvil application at https://anvil.works, and add the PyXLL application
as a dependency.

The PyXLL Anvil application can be found here:
https://O2G7KS4BHEV7QW4V.anvil.app/AJCIRYRRBCQ6WBCTLNP3QGTY

In your Anvil application use the `anvil_pyxll.server.xl_func` decorator instead of
the usual `pyxll.xl_func` decorator.

Enable Uplink on your Anvil application and edit anvil-pyxll.cfg with the Anvil Uplink
token.

```ini
[ANVIL]
token = <your anvil uplink token here>
```

Add anvil-pyxll.cfg as an extenal config to your main pyxll.cfg, and when you start Excel
it will connect to Anvil using the token specified in the config file.

```ini
[PYXLL]
external_config =
    <path to anvil-pyxll.cfg>
```
