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
        
        if result.stderr:
            plugin.log(error_output)
        
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
    
    reckless_output = execute_reckless(params=[ "-r",  "source", "list" ])

    sources = reckless_output.split('\n') 

    if sources[0] == "":
        sources = []

    json_object = { "sources": sources }

    return json_object


@plugin.method("reckless-sourceadd")
def reckless_sourceadd(plugin, repo_url):
    '''reckless source add'''

    execute_reckless(params=[ "-r",  "source", "add", f"{repo_url}" ])

    return reckless_sourcelist(plugin)

@plugin.method("reckless-sourcerm")
def reckless_sourcerm(plugin, repo_url):
    '''reckless source rm'''

    # remove the entry
    output = execute_reckless(params=[ "-r",  "source", "remove", f"{repo_url}" ])

    return reckless_sourcelist(plugin)

@plugin.method("reckless-install")
def reckless_install(plugin, plugin_name):
    '''reckless install <plugin_name>'''

    install_output = execute_reckless(params=[ "-r",  "install", f"{plugin_name}" ])

    install_output_lines = install_output.split('\n') 

    if install_output_lines[0] == "":
        install_output_lines = []

    json_object = { "install_messages": install_output_lines }

    return json_object

@plugin.method("reckless-uninstall")
def reckless_uninstall(plugin, plugin_name):
    '''reckless uninstall <plugin_name>'''

    uninstall_output = execute_reckless(params=[ "-r",  "uninstall", f"{plugin_name}" ])

    uninstall_output_lines = uninstall_output.split('\n') 

    if uninstall_output_lines[0] == "":
        uninstall_output_lines = []

    json_object = { "uninstall_messages": uninstall_output_lines }

    return json_object

@plugin.method("reckless-search")
def reckless_search(plugin, plugin_name):
    '''reckless search <plugin_name>'''

    search_results = execute_reckless(params=[ "-r",  "search", f"{plugin_name}" ])

    search_results_lines = search_results.split('\n')

    if search_results_lines[0] == "":
        search_results_lines = []

    json_object = { "search_results": search_results_lines } 

    return json_object

@plugin.method("reckless-disable")
def reckless_disable(plugin, plugin_name):
    '''reckless help'''

    return execute_reckless(params=[ "-r",  "disable", f"{plugin_name}" ])

plugin.run()  # Run our plugin
