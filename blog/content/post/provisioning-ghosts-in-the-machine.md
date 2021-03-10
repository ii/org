+++
title = "Provisioning Ghosts in the Machine"
date = 2015-10-30
weight = 2011
lastmod = "Fri Oct 30 14:35:14 NZDT 2015"
draft = true
author = ["Hippie Hacker"]
summary = "I set this blog up in a few minutes using a chef-provisoining recipe, ghost-cookbook, and the new do-api-v2 support."
+++

I set this blog up in just a few minutes using https://github.com/cnunciato/ghost-cookbook
and a simple chef-provisioning recipe and the new [do-api-v2](http://blog.ii.delivery/do-api-v2/) support.

I'd like to add support for syntax highlighting and comments at some point.

You can run this with ```DOTOKEN=XXX chef-client -z THISRECIPE.rb```

```language-ruby
with_driver 'fog:DigitalOcean', compute_options: {
                 digitalocean_token: ENV['DOTOKEN']
               }

with_machine_options convergence_options: {
                       chef_version: '12.4.3',
                       package_cache_path: '.chef/package_cache'
                     },
                     bootstrap_options: {
                       image_distribution: 'Ubuntu',
                       image_name: '14.04 x64',
                       region_name: 'New York 3',
                       flavor_name: '2GB',
                       key_name: 'iido',
                       tags: {
                         'ii' => 'lovesyou'
                       },
                     }

with_chef_server 'https://api.chef.io/organizations/ii',
                 :client_name => Chef::Config[:node_name],
                 :signing_key_filename => Chef::Config[:client_key]

machine 'do.ii.delivery' do
  action :destroy if ENV['DESTROY']
  recipe 'ghost::default'
  recipe 'ghost::nginx'
  # attribute %w[ ghost app mail transport ], 'SMTP'
  # attribute %w[ ghost app mail options service ], 'Gmail'
  # attribute %w[ ghost app mail options auth user ], 'smtp@hippiehacker.org'
  # attribute %w[ ghost app mail options auth pass ], 'SOMETHING'
  # attribute %w[ ghost remote name ], 'darepo'
  # attribute %w[ ghost remote repo ], 'git@github.com:ii/ghostcontent.git'
  # attribute %w[ ghost remote revision ], 'master'
end

```
