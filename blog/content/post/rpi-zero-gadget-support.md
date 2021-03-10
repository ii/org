+++
title = "RPi Zero Gadget Support"
date = 2015-12-06
weight = 2009
author = ["Hippie Hacker"]
lastmod = "Sun Dec 06 00:09:45 NZDT 2015"
summary = "For most OTG supported ports, it depends on what you plug into it that decides if the port is in host mode or gadget mode. We just need to get confirmation that the RPi zero port is wired the same way for the port that has it's usb data pins connected (not the one dedicated to power)."
+++


For most OTG supported ports, it depends on what you plug into it that decides if the port is in host mode or gadget mode. We just need to get confirmation that the RPi zero port is wired the same way for the port that has it's usb data pins connected (not the one dedicated to power).

["A device with a micro-A plug inserted becomes an OTG A-device, and a device with a micro-B plug inserted becomes a B-device. The type of plug inserted is detected by the state of the pin ID ."](https://en.wikipedia.org/wiki/USB_On-The-Go#OTG_micro_plugs) 

The RPi zero USB_OTGID pin should be grounded by the cable when using a micro-A / OTG cable and is hopefully left floating otherwise. That way we can the more common micro-B cable for providing power and connecting the usb data pins to a computer.

Here is a RPi zero [mechanical diagram](https://www.raspberrypi.org/documentation/hardware/raspberrypi/mechanical/rpi-zero-v1_2_dimensions.pdf), that shows the two usb micro ports for the RPi zero in bottom right:

![image](https://cloud.githubusercontent.com/assets/31331/11607199/43a2a708-9b0b-11e5-8d98-518769d4df19.png)

I couldn't find wiring schematics for RPi zero, so I pulled these from the [RPi A](https://www.raspberrypi.org/wp-content/uploads/2012/10/Raspberry-Pi-R2.0-Schematics-Issue2.2_027.pdf)

This is the usb micro port used for power: (no data pins)

![image](https://cloud.githubusercontent.com/assets/31331/11607210/b6d0f310-9b0b-11e5-97fb-1de5d360647c.png)

This is the RPi-A USB-A port (note that the USB_OTGID pin on the usb controller is grounded). On the RPi zero, this connector is a micro-b port, and shouldn't have the USB_OTGID pin grounded, as that is usually done by the cable to distinguish between OTG/Host mode and usb gadget mode.

![image](https://cloud.githubusercontent.com/assets/31331/11607223/fecac092-9b0b-11e5-8bcf-1d3f2b8e107b.png)

I suspect that if we connect a normal [usb A to Micro-B cable](https://en.wikipedia.org/wiki/USB#Cable_plugs_.28USB_1.x.2F2.0.29) that doesn't ground out the USB_OTGID pin on the RPi zero, that we can accomplish the correct physical connections without any modifications, but we may need the kernel changes mentioned in this [comment on #881]( https://github.com/raspberrypi/linux/issues/881#issuecomment-161411866)

Having a $5 usb gadget that could function as a combination of anything in https://github.com/torvalds/linux/tree/master/drivers/usb/gadget/function would be pretty grand.

I've opened a ticket for PRi linux kernel to [discuss this](https://github.com/raspberrypi/linux/issues/1212).
