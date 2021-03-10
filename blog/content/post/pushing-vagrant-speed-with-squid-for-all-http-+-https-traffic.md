+++
title = "Pushing vagrant speed with squid for all http + https traffic"
date = 2015-12-19
weight = 2008
author = ["Hippie Hacker"]
lastmod = "Sat Dec 19 05:50:25 NZDT 2015"
summary = "docker run proxy exports an https certificate AND three ports for http / https proxying"
+++


docker run proxy exports an https certificate AND three ports for http / https proxying

3128 is as standard http/https proxy.
3129 is intended for use as an http transparent proxy
3130 is intended for use as an https transparent proxy

However it requires that we get ip tables to transparently change the destination traffic (the host in unaware) to connect to the transparent proxies.

Configure iptables to Pid [Owner Match](https://www.frozentux.net/iptables-tutorial/iptables-tutorial.html#OWNERMATCH) vagrant so that all traffic within the VM get's transparently proxies to iisquid.

Squid uses this certificate to create on the fly ssl certificates for any host signed by it's own CA. However, the ssl structure requires the connecting clients trusting the self-signed CA created for use with squid. (A couple countries are suggesting / requiring all their folks use this approach so the government can intercept and block)

We need to find a way to install this ca into the OSes running on devices / virtual or otherwise, we want to test.

Current target is windows, which looks straight forward.

Need to merge and get current to use compose etc:

https://github.com/hh/squid-in-a-can/network

And our approach to creating static binaries using tcl-container... I'm not sure of 

iptables modules no longer support owner
http://manpages.ubuntu.com/manpages/trusty/man8/iptables-extensions.8.html
