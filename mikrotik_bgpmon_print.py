# Copyright (c) 2023 - Lee Hetherington <lee@edgenative.net>
# Script: mikrotik_bgpmon_print.py
#
# Usage: mikrotik_bgpmon_print.py router_ip true|false
#
# This script will take a config file containing the Username and Password of the router, then using
# the ROS API, connect to the router and dump you a list of current BGP Sessions and tell you their
# status.  The output can then be used for any number of your own systems.
#
import sys
import configparser
import routeros_api
import argparse

# Let's take some arguments on the command line
parser = argparse.ArgumentParser()

# add arguments to the parser
parser.add_argument("router_ip", help="IP address or hostname of the router")
parser.add_argument("session_state", help="Provide Session state, true = established, false = anything else")
# parse the arguments
args = parser.parse_args()

# access the values of the arguments
ROUTER_IP = args.router_ip
session_state = args.session_state

# Read from the config file
# which contains the auth information
config = configparser.ConfigParser()
config.read('config.cfg')
username = config.get('API', 'username')
password = config.get('API', 'password')

# Build the API connection to the router
connection = routeros_api.RouterOsApiPool(ROUTER_IP, username=username, password=password, use_ssl=True, ssl_verify=False, plaintext_login=True)
api = connection.get_api()

# Get the current configuration from the router
current_config_connection = api.get_resource('/routing/bgp/session')
current_config_response = current_config_connection.get(established=session_state)
current_config_str = str(current_config_response)
config_list = eval(current_config_str)

for item in config_list:
    session_name = item.get('name')
    remote_as = item.get('remote.as')
    remote_address = item.get('remote.address')
    uptime = item.get('uptime')
    session_state = item.get('established')
    if session_state == "true":
      session_state_name = "Established"
    else:
      session_state_name = "Connect"
    print(f"Session: {session_name}, AS: {remote_as}, Peer IP: {remote_address}, Status: {session_state_name}, Uptime: {uptime}")
