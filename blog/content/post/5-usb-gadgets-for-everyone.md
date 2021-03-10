+++
title = "5 Dollar USB Gadgets for Everyone"
date = 2015-12-06
weight = 2010
author = ["Hippie Hacker"]
lastmod = "Sun Dec 06 00:10:35 NZDT 2015"
summary =  "In my work trying to create devices that can install OSes from scratch on computers and flash phones and embedded IoT devices, I'm always looking for things that can support being both a usb host and a usb gadget."
+++


In my work trying to create devices that can install OSes from scratch on computers and flash phones and embedded IoT devices, I'm always looking for things that can support being both a usb host and a usb gadget.

Think about your phone, how it works to connect a micro-B to charge and  connect to it as a gadget to your computer, then when you connect a micro-A cable you plug mice, keyboard, and thumb drives into your phone.

As a usb host, you can plug a mouse, keyboard, and pretty much anything you'd plug into your computer to it. Allowing you to do things like:

* Format a thumb drive or microSD card
* bootstrap embedded devices like intel edison
* flash a phone

As a usb gadget, you can plug the device into a computer and have it show up as a usb keyboard, disk, network, and other interesting things.

* show up as a network adapter
* provide a web / programming interface to the gadget without needing internet
* send some keystrokes a computer
* present a dynamic USB cdrom / dvd drive
* re-install a computer from scratch combining keyboard and drive support
* install OSes to a drive hosted on the device and snapshot them

I'm looking to see if we can't get the new $5 RPi zero to [function as both](http://blog.ii.delivery/rpi-zero-gadget-support/).
