import os
from pyln.testing.fixtures import *  # noqa: F401,F403
from pyln.client import Millisatoshi

plugin_path = os.path.join(os.path.dirname(__file__), 'reckless-wrapper.py')
plugin_opt = {'plugin': plugin_path}

# spin up a network
def test_start_plugin(node_factory):
    # Start two lightning nodes
    l1 = node_factory.get_node()

    #try:
    assert l1.rpc.plugin_start(plugin_path)
    assert l1.rpc.reckless_source(subcommand="list")
    assert l1.rpc.plugin_stop(plugin_path)
