+++
title = "SSL Certificate Bindings on Windows with Chef"
date = 2016-09-06
weight = 2005
author = ["Hippie Hacker"]
lastmod = "Tue Sep 06 11:42:02 NZST 2016"
summary = "Enusring ssl certificates on windows are installed correctly."
+++


I recently needed to ensure some ssl certificates on windows installed correctly. I opened an issue at [chef-cookbook/windows#313](https://github.com/chef-cookbooks/windows/issues/313) but the gist of it is here:

```feature
As a windows chef user
I want to ensure a specific certificate binding to a port
In order to replace any existing binding with what I have specified

Given a certificate in pfx form
And it's successfully imported
When I write a windows_certificate_binding resource stanza
And specify the desired subject or fingerprint
And there is already another certificate bound to the desired port
Then the desired certificate binding should replace the existing one
```

What you currently have to do (using an encrypted data bag with password, subject and fingerpint, and a files/default/certificate.pfx):

```ruby
iis_site 'Default Web Site' do
  action :config
  site_id 1
  bindings 'http/*:80:,net.tcp/808:*,net.pipe/*,net.msmq/localhost,msmq.formatname/localhost,https/*:443:'
end

decrypted = data_bag_item('passwords', "certificate")

pfx = "c:\\chef\\certificate.pfx"

cookbook_file pfx

windows_certificate pfx do
  pfx_password decrypted['password']
  store_name 'MY'
  user_store false
end

subject = decrypted['subject']
fingerprint = decrypted['fingerprint']

#removing the current one IF it doesn't match
windows_certificate_binding 'Unbind any non-matching certs' do
  action :delete
  name subject
  name_kind :subject
  address '0.0.0.0'
  guard_interpreter :powershell_script
  not_if <<-EOF
  Import-Module WebAdministration
  $x = Git-Item IIS:\SslBindings\0.0.0.0!443
  $x.Thumbprint.CompareTo("#{fingerprint}")
  EOF
end

# bind the correct one... this should be all we need to specify...
# if there is already a binding on this port... it does nothing
# it should replace it in my opinion
windows_certificate_binding 'Reuse RDP and WINRM self-signed cert for IIS' do
  action :create
  name_kind :subject
  name subject
  address '0.0.0.0'
end
```
