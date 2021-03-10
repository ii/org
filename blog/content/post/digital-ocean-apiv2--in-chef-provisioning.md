+++
title = "Digital Ocean APIv2  in chef-provisioning"
date = 2015-10-30
weight = 2011
author = ["Hippie Hacker"]
lastmod = "Fri Oct 30 03:54:18 NZDT 2015"
summary = "Digital ocean is sunsetting api v1 on November 9th.  It's taken a while, but @geemus released support in fog v1.35.0"
+++


Digital Ocean is [sunsetting api v1](https://developers.digitalocean.com/documentation/changelog/api-v1/sunsetting-api-v1/) on November 9th. It's taken a while, but @geemus [released support in fog v1.35.0](https://github.com/fog/fog/issues/3419#issuecomment-149700617)

I was able to take that work and [update chef-provisioning-fog](https://github.com/chef/chef-provisioning-fog/issues/119#issuecomment-152188977) which we can now use to chef-provision on digital ocean after next week.

The branch is at [ii/chef-provisioning-fog apiv2](https://github.com/ii/chef-provisioning-fog/tree/do_api_v2)

Run ```chef-client -z my_do_server.rb``` on the following ruby:

```ruby
with_driver 'fog:DigitalOcean', compute_options: {
                 digitalocean_token: ENV['DOTOKEN']
#                 digitalocean_api_key: 'V1_DEPRECATED',
#                 digitalocean_client_id: 'V1_DEPRECATED',
               }
# Adding compute_options here seems broken ^^^^
# so make sure and add driver_options to knife.rb

# put this in knife.rb
#knife[:digital_ocean_access_token] = ENV['DOTOKEN']
#driver_options compute_options: {digitalocean_token: ENV['DOTOKEN']}

with_machine_options bootstrap_options: {
                       image_distribution: 'Ubuntu',
                       image_name: '14.04 x64',
                       region_name: 'New York 3',
                       flavor_name: '2GB'
                       tags: {
                         'ii' => 'lovesyou'
                       },
                     }

with_chef_server 'https://api.chef.io/organizations/ii',
                 :client_name => Chef::Config[:node_name],
                 :signing_key_filename => Chef::Config[:client_key]

machine 'do.ii.delivery'
```
