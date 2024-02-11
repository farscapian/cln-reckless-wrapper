#!/usr/bin/env python3
import json
import os
import re
import subprocess
from pyln.client import Plugin, RpcError

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
        result = subprocess.run([reckless_script_path] + params, stdout=subprocess.PIPE, text=True, check=True)
        output = result.stdout

    except RpcError as e:
        plugin.log(e)
        return e

    return_output = output.strip()

    return {
        "output": f"{return_output}"
    }

# DONE
@plugin.method("reckless-help")
def reckless_help(plugin):
    '''reckless help'''

    return execute_reckless(params=[ "-r", "help" ])

# DONE
@plugin.method("reckless-sourcelist")
def reckless_sourcelist(plugin):
    '''reckless source list'''
    
    return execute_reckless(params=[ "-r", "source", "list" ])


@plugin.method("reckless-sourceadd")
def reckless_sourceadd(plugin, repo_url):
    '''reckless source add'''

    return execute_reckless(params=[ "-r", "source", "add", f"{repo_url}" ])

@plugin.method("reckless-sourcerm")
def reckless_sourcerm(plugin, repo_url):
    '''reckless source rm'''

    return execute_reckless(params=[ "-r", "source", "rm", f"{repo_url}" ])

@plugin.method("reckless-install")
def reckless_install(plugin, plugin_name):
    '''reckless install <plugin_name>'''

    return execute_reckless(params=[ "-r", "install", f"{plugin_name}" ])

@plugin.method("reckless-uninstall")
def reckless_uninstall(plugin, plugin_name):
    '''reckless uninstall <plugin_name>'''

    return execute_reckless(params=[ "-r", "uninstall", f"{plugin_name}" ])

@plugin.method("reckless-search")
def reckless_search(plugin, plugin_name):
    '''reckless search <plugin_name>'''

    return execute_reckless(params=[ "-r", "search", f"{plugin_name}" ])

@plugin.method("reckless-disable")
def reckless_disable(plugin, plugin_name):
    '''reckless help'''

    return execute_reckless(params=[ "-r", "disable", f"{plugin_name}" ])

plugin.run()  # Run our plugin
