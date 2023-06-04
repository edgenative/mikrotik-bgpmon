# mikrotik-bgpmon
Mikrotik BGP Monitoring Scripts

#### Prerequisits

[Mikrotik RouterOS API Python Packages](https://pypi.org/project/RouterOS-api/) and a Mikrotik Router(s) running BGP

#### What is this for?

These scripts will help you monitor BGP sessions on your Mikrotik Routers, given Mikrotik is _STILL_ lacking BGP support in their SNMP implementation.  There are two scripts here that'll do slightly different things.

mikrotik_bgpmon.py - This script will look at configured peers under /routing/bgp/connection and compare them with the items under /routing/bgp/session to see if they match.  If they don't, an alert is created.  Seconly, it'll also look at the status of sessions under /routing/bgp/session and alert you of any status that isn't established.  If you specify an email address (and details in the config.cfg), it'll also send you an email with the output each time you run the script.

Example output;

```
Alerts generated:
Alert: BGP session ipv6.sfmix.lg with 12276 is configured but not found in running sessions.
Alert: BGP session ipv4.sfmix.as8674 with 8674 is configured but not found in running sessions.
Alert: BGP session ipv6.sfmix.as8674 with 8674 is configured but not found in running sessions.
Alert: BGP session ipv4.sfmix.as21928 with 21928 is configured but not found in running sessions.
Alert: BGP session ipv6.sfmix.as21928 with 21928 is configured but not found in running sessions.
````

mikrotik_bgpmon_print.py - This script basically just prints running sessions to the terminal window.  You can specify with true|false on the command line, along side the router IP to display sessions which are either in Established state or not.  Useful if you want to see sessions running, and their uptime, or just want to see sessions which are currently down.

#### How do I run it?

The script needs a few things.  In the ```config.cfg``` you can specify the auth details for your RouterOS API, as well as SMTP server details.  We're assuming here you have a common username/password across all of your routers for this purpose - simiarly, assuming you are using SSL on your API (Self Signed is fine) - you can tweak this in the API connection string in the python if needed.  Further you need to supply a couple of command line arguments;
````
python3 mikrotik_bgpmon.py router_ip email_address
````

To run the print version, you'll need to supply the router address as well as true|false.  True being show me sessions which are established and false being show me all other status.
````
python3 mikrotik_bgpmon_print.py router_ip true
````
