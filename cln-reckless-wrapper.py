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

    return return_output

# DONE
@plugin.method("reckless-help")
def reckless_help(plugin):
    '''reckless help'''

    return execute_reckless(params=[ "-r", "help" ])

# DONE
@plugin.method("reckless-sourcelist")
def reckless_sourcelist(plugin):
    '''reckless source list'''
    
    reckless_output = execute_reckless(params=[ "-r", "source", "list" ])

    sources = reckless_output.split('\n') 

    json_object = { "sources": sources }

    return json_object


@plugin.method("reckless-sourceadd")
def reckless_sourceadd(plugin, repo_url):
    '''reckless source add'''

    # execute_reckless(params=[ "-r", "source", "add", f"{repo_url}" ])

    # url_found = "false"

    # # Lets check if the URL exists in the file. If so, we can assume the source is added.
    # with open('/root/.lightning/reckless/.sources', 'r') as file:
    #     for line in file:
    #         if repo_url in line:
    #             url_found = "true"
    #             break  # Stop searching once the URL is found

    return execute_reckless(params=[ "-r", "source", "add", f"{repo_url}" ])

@plugin.method("reckless-sourcerm")
def reckless_sourcerm(plugin, repo_url):
    '''reckless source rm'''

    # remove the entry
    output = execute_reckless(params=[ "-r", "source", "remove", f"{repo_url}" ])

    return output
    #reckless_sourcelist(plugin)

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
