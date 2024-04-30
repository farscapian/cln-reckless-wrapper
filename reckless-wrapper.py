#!/usr/bin/env python3
import json
import os
import re
import subprocess
from pyln.client import Plugin, RpcError

plugin = Plugin()

@plugin.init()  # this runs when the plugin starts.
def init(options, configuration, plugin, **kwargs):

    plugin.log("initializing reckless-wrapper.py.")

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

        reckless_script_path = f"reckless"
        result = None
        result = subprocess.run([reckless_script_path] + env_params + params, stdout=subprocess.PIPE, text=True, check=True)
        output = result.stdout
        
        if result.stderr:
            plugin.log(error_output)
        
    except RpcError as e:
        plugin.log(e)
        return e

    return_output = output.strip()
    plugin.log(f"return_output: {return_output}", "info")

    return return_output

def reckless_sourcelist():
    reckless_output = execute_reckless(params=[ "source", "list" ])
    sources = reckless_output.split('\n') 

    plugin.log(f"source: {sources}", "info")

    if sources[0] == "":
        sources = []

    json_object = { "sources": sources }

    return json_object
    
@plugin.method("reckless-source")
def reckless_source(plugin, subcommand: None, repo_url=""):
    '''reckless source subcommand=[add|remove] repo_url='''

    plugin.log(f"reckless-source {subcommand} {repo_url}", "info")
    allowed_subcommands = ["add", "remove", "list"]

    if subcommand not in allowed_subcommands:
        raise Exception("Allowed subcommands are add/remove/list.")

    if subcommand != "list":
        if repo_url == "":
            raise Exception(f"You must provide a repo_url when running reckless source {subcommand}")

        execute_reckless(params=[ "source", f"{subcommand}", f"{repo_url}"])
        
    return reckless_sourcelist()

@plugin.method("reckless")
def reckless_install(plugin, subcommand: None, plugin_name=None, git_commit=None):
    '''reckless search|install|uninstall|enable|disable plugin_name'''

    if subcommand == "search":
        search_results = execute_reckless(params=[ "search", f"{plugin_name}" ])
        search_results_lines = search_results.split('\n')

        if search_results_lines[0] == "":
            search_results_lines = []

        json_object = { "search_results": search_results_lines } 

        return json_object

    elif subcommand == "install":
        # TODO git_commit
        params=[ "install", f"{plugin_name}" ]

        if git_commit != None:
            params.append(f"{git_commit}")

        install_output = execute_reckless(params)

        install_output_lines = install_output.split('\n') 

        if install_output_lines[0] == "":
            install_output_lines = []

        json_object = { "install_output": install_output_lines }

        return json_object
    elif subcommand == "uninstall":
        uninstall_output = execute_reckless(params=[ "uninstall", f"{plugin_name}"] )

        uninstall_output_lines = uninstall_output.split('\n') 

        if uninstall_output_lines[0] == "":
            uninstall_output_lines = []

        json_object = { "uninstall_output": uninstall_output_lines }

        return json_object

    elif subcommand == "enable":
        return execute_reckless(params=[ "enable", f"{plugin_name}" ])
    elif subcommand == "disable":
        return execute_reckless(params=[ "disable", f"{plugin_name}" ])
    else:
        return execute_reckless(params=[ "help" ])

plugin.run()
