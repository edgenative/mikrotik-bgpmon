# mikrotik-bgpmon
Mikrotik BGP Monitoring Scripts

#### Prerequisits

[Mikrotik RouterOS API Python Packages](https://pypi.org/project/RouterOS-api/) and a Mikrotik Router(s) running BGP

#### What is this for?

There are two scripts in this collection, which will help you monitor BGP sessions on your Mikrotik Routers, given Mikrotik is _STILL_ lacking BGP support in their SNMP implementation.

### mikrotik_bgpmon.py

This script will look at configured (but _not_ disabled) peers under /routing/bgp/connection and compare them with the items under /routing/bgp/session to see if they match.  If they don't, an alert is created.  Seconly, it'll also look at the status of sessions under /routing/bgp/session and alert you of any status that isn't established.  If you specify an email address (and details in the config.cfg), it'll also send you an email with the output each time you run the script.

Example output;

```
Skipping disabled connection: ipv6.sfmix.lg
Alerts generated:
Alert: BGP connection ipv4.sfmix.as8674 with 8674 is configured but not found in running sessions.
Alert: BGP connection ipv6.sfmix.as8674 with 8674 is configured but not found in running sessions.
Alert: BGP connection ipv4.sfmix.as21928 with 21928 is configured but not found in running sessions.
Alert: BGP connection ipv6.sfmix.as21928 with 21928 is configured but not found in running sessions.
````

### mikrotik_bgpmon_print.py

This script will display the sessions currently running on the router, and give you some details.  It doesn't look at things which are in /routing/bgp/connection that are not also in /routing/bgp/session - so it shouldn't be used to monitor the health.  However, if you supply the routerIP, then up or down to the script at the command line, it'll show you the status.

Example output;

```
Session: ipv6.sfmix.rs1-1, AS: 63055, Peer IP: 2001:504:30::ba06:3055:1, Status: true, Uptime: 3h19m56s310ms, Prefixes: 55721
Session: ipv4.sfmix.rs1-1, AS: 63055, Peer IP: 206.197.187.253, Status: true, Uptime: 3h19m56s310ms, Prefixes: 111222
```

#### How do I run it?

The script needs a few things.  In the ```config.cfg``` you can specify the auth details for your RouterOS API, as well as SMTP server details.  We're assuming here you have a common username/password across all of your routers for this purpose - simiarly, assuming you are using SSL on your API (Self Signed is fine) - you can tweak this in the API connection string in the python if needed.  Further you need to supply a couple of command line arguments;
````
python3 mikrotik_bgpmon.py router_ip email_address
````
If you don't supply an email address as a command line argument, it'll just print the alerts to the terminal, and not send an email.

For the second script, you simply need to supply the router_ip and what status sessions you want to see, up or down

```
python3 mikrotik_bgpmon_print.py router_ip up
```

