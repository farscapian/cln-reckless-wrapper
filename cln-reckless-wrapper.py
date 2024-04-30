#!/usr/bin/env python3
import json
import os
import re
import subprocess
from pyln.client import Plugin, RpcError

#plugin_path = os.path.join(os.path.dirname(__file__), '../bolt12-prism.py')

plugin = Plugin()

@plugin.init()  # this runs when the plugin starts.
def init(options, configuration, plugin, **kwargs):

    plugin.log("initializing cln-reckless-wrapper.py.")

# this is called by all the other rpc methods.
# each invoker passes params.
def execute_reckless(params=""):

    output = None
    cln_network = plugin.rpc.getinfo()["network"]
    allowable_networks = ["regtest", "bitcoin", "liquid", "liquid-regtest", "litecoin", "signet"]

    if cln_network not in allowable_networks:
        raise Exception("Can't connect to the correct network. Please check your config.")

    # regtest bitcoin liquid, liquid-regtest, litecoin, signet
    try:
        env_params = []
        env_params.append(f"--network={cln_network}")
        env_params.append("-d")
        env_params.append("/reckless-plugins")

        reckless_script_path = f"/usr/local/bin/reckless"
        result = None
        result = subprocess.run([reckless_script_path] + env_params + params, stdout=subprocess.PIPE, text=True, check=True)
        output = result.stdout
        
        if result.stderr:
            plugin.log(error_output)
        
    except RpcError as e:
        plugin.log(e)
        return e

    return_output = output.strip()

    return return_output



def reckless_sourcelist(plugin):
    '''reckless source list'''
    
    reckless_output = execute_reckless(params=[ "source", "list" ])

    sources = reckless_output.split('\n') 

    if sources[0] == "":
        sources = []

    json_object = { "sources": sources }

    return json_object
    
@plugin.method("reckless-source")
def reckless_sourceadd(plugin, subcommand: None, repo_url: None):
    '''reckless source subcommand=[add|remove] repo_url='''

    if subcommand == "list":
        reckless_output = execute_reckless(params=[ "source", "list" ])
        sources = reckless_output.split('\n') 

        if sources[0] == "":
            sources = []

        json_object = { "sources": sources }

        return json_object

    elif subcommand == "add":
        execute_reckless(params=[ "source", "add", f"{repo_url}" ])

        return reckless_sourcelist(plugin)
    elif subcommand == "remove":
        # remove the entry
        output = execute_reckless(params=[ "source", "remove", f"{repo_url}" ])

        return reckless_sourcelist(plugin)
    else:
        raise Exception("Subcommand must be either add, remove, or list.")

@plugin.method("reckless")
def reckless_install(plugin, subcommand: None, plugin_name: None, git_commit=None):
    '''reckless install|uninstall|search|enable|disable plugin_name'''

    if subcommand == "install":
        # TODO git_commit
        install_output = execute_reckless(params=[ "install", f"{plugin_name}" ])

        install_output_lines = install_output.split('\n') 

        if install_output_lines[0] == "":
            install_output_lines = []

        json_object = { "install_messages": install_output_lines }

        return json_object
    elif subcommand == "uninstall":
        uninstall_output = execute_reckless(params=[ "uninstall", f"{plugin_name}"] )

        uninstall_output_lines = uninstall_output.split('\n') 

        if uninstall_output_lines[0] == "":
            uninstall_output_lines = []

        json_object = { "uninstall_messages": uninstall_output_lines }

        return json_object

    elif subcommend == "search":

        search_results = execute_reckless(params=[ "search", f"{plugin_name}" ])

        search_results_lines = search_results.split('\n')

        if search_results_lines[0] == "":
            search_results_lines = []

        json_object = { "search_results": search_results_lines } 

        return json_object
    elif subcommend == "enable":
        return execute_reckless(params=[ "enable", f"{plugin_name}" ])
    elif subcommend == "disable":
        return execute_reckless(params=[ "disable", f"{plugin_name}" ])
    else:
        return execute_reckless(params=[ "help" ])

plugin.run()
