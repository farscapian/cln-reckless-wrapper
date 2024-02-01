#!/usr/bin/env python3
import json
import os
import re
import time
import subprocess
import uuid
from pyln.client import Plugin, RpcError
from datetime import datetime, timedelta

lnlive_plugin_api_version = "v0.0.1"

plugin_out = "/tmp/plugin_out"
if os.path.isfile(plugin_out):
    os.remove(plugin_out)

# use this for debugging-
def printout(s):
    with open(plugin_out, "a") as output:
        output.write(s)

plugin = Plugin()

@plugin.init()  # this runs when the plugin starts.
def init(options, configuration, plugin, **kwargs):


    plugin.log("cln-reckless-wrapper")


@plugin.method("reckless-sourcelist")
def reckless_install(plugin, repo_url, hours):
    '''Returns a BOLT11 invoice for the given node count and time.'''
    try:
        params = [f"--invoice-id={invoice_id}" ]

        result = None

        # get the plugin path from the os env
        plugin_path = os.environ.get('PLUGIN_PATH')

        provision_script_path = f"{plugin_path}/cln-reckless-wrapper.py"

        try:
            plugin.log(f"reckless-sourcelist")
            # + params
            result = subprocess.run(['python3', provision_script_path] + params)

        except subprocess.CalledProcessError as e:
            plugin.log(f"The bash script exited with error code: {e.returncode}")

    #reckless source add https://github.com/farscapian/cln-reckless-wrapper.git
    except RpcError as e:
        plugin.log(e)
        return e

    return result


@plugin.method("reckless-install")
def reckless_install(plugin, repo_url, hours):
    '''Returns a BOLT11 invoice for the given node count and time.'''
    try:
        params = [f"--invoice-id={invoice_id}" ]

        result = None

        provision_script_path = f"{plugin_path}/cln-reckless-wrapper.py"

        try:
            plugin.log(f"About to call reckless.py")
            # + params
            result = subprocess.run(['python', provision_script_path] + params)

        except subprocess.CalledProcessError as e:
            plugin.log(f"The bash script exited with error code: {e.returncode}")

    #reckless source add https://github.com/farscapian/cln-reckless-wrapper.git
    except RpcError as e:
        plugin.log(e)
        return e

    return result


plugin.run()  # Run our plugin
