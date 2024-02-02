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

    plugin.log("initializing cln-reckless-wrapper.py.")


# this is called by all the other rpc methods.
# each invoker passes params.
def execute_reckless(params="-r"):

    output = None
    
    try:

        reckless_script_path = f"/usr/local/bin/reckless"
        result = None
        if params == "-r":
            result = subprocess.run([reckless_script_path], stdout=subprocess.PIPE, text=True, check=True)
        else:
            result = subprocess.run([reckless_script_path] + params, stdout=subprocess.PIPE, text=True, check=True)

        output = result.stdout

    except RpcError as e:
        plugin.log(e)
        return e

    return output.strip()



@plugin.method("reckless-help")
def reckless_help(plugin):
    '''reckless help'''

    return execute_reckless(params=[ "-r", "help" ])


@plugin.method("reckless-sourcelist")
def reckless_sourcelist(plugin):
    '''reckless source list'''
    
    return execute_reckless(params=[ "-r", "source", "list" ])

@plugin.method("reckless-sourceadd")
def reckless_sourceadd(plugin):
    '''reckless source add'''

    return ""

@plugin.method("reckless-sourcerm")
def reckless_sourcerm(plugin):
    '''reckless source rm'''

    return "" 

@plugin.method("reckless-install")
def reckless_install(plugin):
    '''reckless install <repo_url>'''

    return "" 

@plugin.method("reckless-uninstall")
def reckless_uninstall(plugin):
    '''reckless uninstall <repo_url>'''

    return "" 

@plugin.method("reckless-search")
def reckless_search(plugin):
    '''reckless search search_string="example_plugin"'''

    return "" 


@plugin.method("reckless-disable")
def reckless_disable(plugin):
    '''reckless help'''

    return "" 

plugin.run()  # Run our plugin
