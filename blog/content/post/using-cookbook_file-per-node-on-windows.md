+++
title = "Using cookbook_file per Node on Windows"
date = 2016-09-06
weight = 2006
author = ["Hippie Hacker"]
lastmod = "Tue Sep 06 11:43:03 NZST 2016"
summary = "I needed to deploy a different node specific license file to our windows hosts so I wrote a cookbook_file resource..."
+++


I needed to deploy a different node specific license file to our windows hosts so I wrote a [cookbook_file](https://docs.chef.io/resource_cookbook_file.html) resource that looked something like this:

```ruby
cookbook_file 'C:\\Program Files (x86)\\vendor\\node.license'
```

And using the [file-specificity overhaul](https://github.com/chef/chef-rfc/blob/master/rfc017-file-specificity.md) I expected to be able to create a directory for each host under ```our-cookbook/files/host-NODENAME/our.license``` and have that be the file for that specific node.

```
our-cookbook $ tree files/host-nodes*
files/host-nodename1
└── node.license
files/host-nodename2
└── node.license
files/host-nodename3
└── node.license
files/host-nodename4
└── node.license
```

It took me a while to understand my failed assumptions.

_NODENAME isn't the same as FQDN_

It usually is, but on windows ec2 instances they often differ.

Ec2Config service is configured by default on many windows AMIs to [reset computer name on next boot](http://docs.aws.amazon.com/AWSEC2/latest/WindowsGuide/UsingConfig_WinAMI.html#UsingConfigInterface_WinAMI) which results in new machines geting renamed to ```ip-IP_INHEX``` where IP_INHEX is the hex representation of the internal ip.

```
$ knife winrm -m $IP 'ohai' | grep fqdn
10.113.6.171   "fqdn": "ip-0A7106AB",
```

When we bootstrap an ec2 ami and give it an ec2 instance name and nodename for chef, the fdqn/hostname is often left as the default:

```
$ knife search node *:$NODE_NAME
1 items found

Node Name:   $NODE_NAME
Environment: OURENV
FQDN:        ip-0A7106AB
IP:          10.113.6.171
...
Platform:    windows 6.3.9600
```

The fix for getting our license files into place based on the chef nodename was to add a ```source``` parameter to our resource based on the ```node.name```

```ruby
cookbook_file 'C:\\Program Files (x86)\\vendor\\node.license'' do
  # normally this is host-#{node['fdqn']} and on aws/windows than ip-HEXNUMBR
  source "host-#{node.name}/node.license'"
end
```
