# Copyright (c) 2023 - Lee Hetherington <lee@edgenative.net>
# Script: mikrotik_bgpmon.py
#
# Usage: mikrotik_bgpmon.py router_ip email_address
#
# This script will take a config file containing the Username and Password of the router, then using
# the ROS API, connect to the router and do two things;
# 1. Compare configured vs running BGP sessions and alert if differences
# 2. Alert if there is a running session that is not in Established state
#
# You can then use this output for your own systems/email alerting etc.  If you specify an email address
# as a command line switch, it'll send alert emails to that email address
#

import configparser
import routeros_api
import argparse
import smtplib
from email.mime.text import MIMEText

# Let's take some arguments on the command line
parser = argparse.ArgumentParser()

# add arguments to the parser
parser.add_argument("router_ip", help="IP address or hostname of the router")
parser.add_argument("email", nargs='?', help="Email address to receive alerts")
# parse the arguments
args = parser.parse_args()

# access the values of the arguments
router_ip = args.router_ip
email_address = args.email

# Read from the config file
# which contains the auth information
config = configparser.ConfigParser()
config.read('config.cfg')
username = config.get('API', 'username')
password = config.get('API', 'password')
smtp_server = config.get('ALERTS', 'smtp_server')
smtp_port = config.get('ALERTS', 'smtp_port')
smtp_username = config.get('ALERTS', 'smtp_username')
smtp_password = config.get('ALERTS', 'smtp_password')

def send_email(subject, message, recipient):

    # Create email message
    email_msg = MIMEText(message)
    email_msg['Subject'] = subject
    email_msg['From'] = f"BGP Alerts <{smtp_username}>"
    email_msg['To'] = recipient

    # Establish a connection to the email server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)

    # Send the email
    server.send_message(email_msg)
    server.quit()

def check_bgp_sessions(router_ip, username, password, email_address=None):
    api = routeros_api.RouterOsApiPool(router_ip, username=username, password=password, use_ssl=True, ssl_verify=False, plaintext_login=True)
    api_conn = api.get_api()

    configured_connections = api_conn.get_resource('/routing/bgp/connection').get()
    configured_sessions = api_conn.get_resource('/routing/bgp/session').get()

    alerts = []  # Store the generated alerts

    for connection in configured_connections:
        connection_name = connection['name']
        connection_asn = connection.get('remote.as', 'Unknown')
        session_exists = False

        for session in configured_sessions:
            session_name = session['name']
            session_asn = session.get('remote.as', 'Unknown')
            # Remove the last two characters (-1) from session_name for comparison since
            # Mikrotik seems to add this!
            if session_name[:-2] == connection_name:
                session_exists = True
                session_established = session.get('established', '')
                if session_established != "true":
                    alert_msg = f"Alert: BGP session {session_name} with {session_asn} is not established."
                    alerts.append(alert_msg)
                break

        if not session_exists:
            alert_msg = f"Alert: BGP session {connection_name} with {connection_asn} is configured but not found in running sessions."
            alerts.append(alert_msg)

    if email_address and alerts:
        subject = f"Mikrotik BGP Session Alerts [{router_ip}]"
        message = "\n".join(alerts)
        send_email(subject, message, email_address)

    if alerts:
        print("Alerts generated:")
        for alert in alerts:
            print(alert)
    else:
        print("No alerts generated.")

check_bgp_sessions(router_ip, username, password, email_address)
