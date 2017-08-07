:tocdepth: 2
:orphan:

.. _tutorial-create-l3-sw-2:

#######################################
Creating an L3 learning switch - Part 2
#######################################

********
Overview
********
This tutorial will show how to handle ARP packets to create an improved
L3 learning switch NApp using *Kytos* (|kytos|_).
The average time to go through this is: ``30 min``

What you will learn
====================
* How to answer directly to a request using OpenFlow;
* How to install flows for a switch to change packet information when forwarding.

What you will need
===================
* Your |dev_env|_ already up and running.
* The *kytos/of_core* NApp installed and enabled.
* Creating a L3 learning switch, part 1- Refer to |L3_part1|_.

************
Introduction
************

Address Resolution Protocol
===========================
|ARP|_ is a protocol designed to enable hosts in a multiple access network to
discover addresses needed for communication. In Ethernet networks running IPv4,
ARP requests are sent to target IP addresses in order to discover which MAC
address is associated with it.

When hosts in different logical networks must exchange data, they use the ARP
protocol to discover the *router*'s MAC address.

But why must we deal with ARP?
==============================
Because we want to make hosts in different logical networks communicate with
each other!

A host sending data to some other network will create its packets targeting the
IP address of the destination host, but the MAC address will be the *router*'s
address.

In our scenario, the OpenFlow switch will have the routing role, and must change
the MAC addresses of frames before they are forwarded. ARP is used to advertise
the *l3_switch*'s virtual MAC to the hosts, replying when they look for their
default gateway.


So is this a router now?
========================
Not yet. A router should be able to work with ICMP, to manage |routing|_
(static or dynamic), decrement the TTL in IP packets and recalculate checksums,
among other features. It must also recognize networks for each interface and use
proper MAC addresses at each interface.


.. ATTENTION:: This NApp was designed for instructional purposes. Running it in
    production environments may lead to unwanted behavior.


******************
Creating your NApp
******************

First, create your NApp using the ``kytos`` command. Use 'tutorial' as the
username and 'of_l3ls_v2' as the NApp name, as follows (don't forget to create
the ``~/tutorials`` folder if it does not exist):

.. code-block:: console

  $ cd ~/tutorials
  $ kytos napps create
  --------------------------------------------------------------
  Welcome to the bootstrap process of your NApp.
  --------------------------------------------------------------
  In order to answer both the username and the napp name,
  You must follow this naming rules:
   - name starts with a letter
   - name contains only letters, numbers or underscores
   - at least three characters
  --------------------------------------------------------------

  Please, insert your NApps Server username: tutorial
  Please, insert your NApp name: of_l3ls_v2
  Please, insert a brief description for your NApp [optional]: This NApp handles forwarding between different networks.

  Congratulations! Your NApp have been bootstrapped!
  Now you can go to the directory tutorial/of_l3ls_v2 and begin to code your NApp.
  Have fun!

You will edit the ``settings.py`` and the ``main.py`` files. You can open them
in your preferred editor to start coding your NApp:

.. code-block:: console

  $ emacs tutorial/of_l3ls_v2/settings.py tutorial/of_l3ls_v2/main.py


NApp settings
=============
In the ``settings`` module you will define the IP addresses for our OpenFlow
switch, as well as a virtual MAC address that will be used for routing purposes.
The same IP addresses will be later configured as the *gateway* addresses for
each host.

.. code-block::

  GW_MAC = '10:20:30:40:50:60'
  GW_IP = ['10.0.0.100', '20.0.0.100']


Create the ARP and switching tables
===================================
First you will create an ARP table, to store known associations of IP addresses
to MAC addresses in the network. You will also create a forwarding table to
learn at which physical port each IP address can be reached.

The tables are implemented as Python dictionaries. The metod needs a decorator
in order to listen to the Kytos's *new switch* event.

.. code-block::

    @listen_to('kytos/core.switches.new')
    def create_switch_tables(self, event):
        switch = event.content['switch']
        switch.fw_table = {}
	switch.arp_table = {}

.. ATTENTION:: Some classes and methods used in the code snippets need to be imported
    in your main.py file. Please check the full content of the file and import these
    elements as needed.


Verifying the type of received packet_ins
=========================================
Next step is to write a method to handle PacketIn events. As the decision to
be taken depends on the ``ether_type`` of the packet, your method will unpack
the data in an Ethernet instance and call another handler, for ARP or IPv4, as
needed.

.. code-block::

  @listen_to('kytos/of_core.v0x01.messages.in.ofpt_packet_in')
  def handle_packet_in(self, event):
      packet_in = event.content['message']

      ethernet = Ethernet()
      ethernet.unpack(packet_in.data.value)

      in_port = packet_in.in_port.value

      if ethernet.ether_type.value == 0x806:
          self.handle_arp(ethernet, in_port, event.source)
      elif ethernet.ether_type.value == 0x800:
          self.handle_ip(ethernet, in_port, event.source)


Learning host address information from ARP packets
==================================================
The method to handle ARP packets will unpack the data in an ARP instance, and
populate the switch's tables with its information. ARP carries information
about the host who sent it: the **Source Protocol Address** is the IP address
of the sender and the **Source Hardware Address** is the MAC address of the
sender.

There's no need to decorate the ``handle_arp`` method as it does not need to be
executed on PacketIn arrival, being actually called by ``handle_packet_in``.


.. code-block::

  def handle_arp(self, ethernet, in_port, source):
      arp = ARP()
      arp.unpack(ethernet.data.value)

      source.switch.arp_table[arp.spa.value] = arp.sha.value
      source.switch.fw_table[arp.spa.value] = in_port

      log.info('Learning %s at port %d with mac %s.', arp.spa.value, in_port,
               arp.sha.value)

      # (Continues...)

Replying to ARP requests
========================
ARP packets can be requests targeting the *L3 switch*. If this is the case, you
need to create an ARP reply to answer it.

If the ARP operation equals 1 (Request) and any of the *L3 switch*'s addresses
is the target, create an ARP packet with the operation set to 2 (Reply). The
**Source Hardware Address** is the information the sender is looking for - you
will answer with the virtual MAC defined in settings. The other three fields
have their values swapped between Source and Target for the reply.

To send the reply, you need an Ethernet frame to encapsulate it. The Ethernet
source is the virtual MAC of the *L3 Switch*, the destination is the source of
the original frame, ``ether_type`` is ARP (``0x806``) and the data, or *payload*,
is the packed reply you just created.

For the switch to send back the Ethernet frame, you will put it in a PacketOut
OpenFlow message as the data, adding an Action to output it through the same
port it came from. As in |L3_part1|_, create the ``KytosEvent`` and put it in
the controller's ``msg_out`` buffer.


.. code-block::

  def handle_arp(self, ethernet, in_port, source):

      # (...)

      if arp.oper.value == 1 and arp.tpa.value in settings.GW_IP:
          reply = ARP(oper=2)
          reply.sha = settings.GW_MAC
          reply.spa = arp.tpa
          reply.tha = arp.sha
          reply.tpa = arp.spa

          frame = Ethernet()
          frame.source = settings.GW_MAC
          frame.destination = ethernet.source
          frame.ether_type = 0x806
          frame.data = reply.pack()

          packet_out = PacketOut()
          packet_out.data = frame.pack()
          packet_out.actions.append(ActionOutput(port=in_port))

          event_out = KytosEvent(name=('tutorial/of_l3ls_v2.messages.out.'
                                       'ofpt_packet_out'),
                                 content={'destination': source,
                                          'message': packet_out})

          self.controller.buffers.msg_out.put(event_out)
          log.info('Replygin arp request from %s', arp.spa.value)


Installing flows for known hosts
================================
When an IP packet comes, you want to install a rule on the *L3 switch* for it
to forward further incoming packets automatically.

You will look for the destination IPv4 address in the arp_table looking for
a destination MAC address. If any is found, you will create a FlowMod to install
the forwarding rule in the switch. However, it is important to note the new
actions which must be set *before* the ``OutputAction``: tell the switch to
change the source MAC address for its own virtual MAC, and the destination MAC
address of the frame must be the one determined by the controller.

Create the ``KytosEvent`` and put it out right away.


.. code-block::

  def handle_ip(self, ethernet, in_port, source):
      ipv4 = IPv4()
      ipv4.unpack(ethernet.data.value)

      switch = source.switch

      dest_mac = switch.arp_table.get(ipv4.destination, None)

      log.info('Packet received from %s to %s', ipv4.source,
               ipv4.destination)

      if dest_mac is not None:
          dest_port = switch.fw_table.get(ipv4.destination)

          flow_mod = FlowMod()
          flow_mod.command = FlowModCommand.OFPFC_ADD
          flow_mod.match = Match()
          flow_mod.match.nw_src = ipv4.source
          flow_mod.match.nw_dst = ipv4.destination
          flow_mod.match.dl_type = 0x800
          flow_mod.actions.append(ActionDLAddr(action_type=ActionType.OFPAT_SET_DL_SRC,
                                               dl_addr=settings.GW_MAC))
          flow_mod.actions.append(ActionDLAddr(action_type=ActionType.OFPAT_SET_DL_DST,
                                               dl_addr=dest_mac))
          flow_mod.actions.append(ActionOutput(port=dest_port))

          event_out = KytosEvent(name=('tutorial.of_l3ls_v2.messages.out.'
                                       'ofpt_flow_mod'),
                                 content={'destination': source,
                                          'message': flow_mod})

          self.controller.buffers.msg_out.put(event_out)
          log.info('Flow installed! Subsequent packets will be sent directly.')

          # (Continues...)

Looking for unknown hosts in the network
========================================
If any packet comes but the ARP table still does not have the proper address
registered, you need to search for the destination MAC address using an ARP
request.

Create an ARP packet with operation set to 1 (Request), with the *L3 switch*'s
virtual MAC as the SHA and the IPv4 address we're requesting as the TPA.

As with the reply written above, it needs to be encapsulated into an Ethernet
frame and the put in a PacketOut. The Ethernet frame will have the broadcast
MAC address as the destination, and the action in the PacketOut will make the
switch flood it in the network.

Once this request gets a reply, the ``arp_handler`` method will learn the
addresses enabling the *L3 switch* to create the FlowMod next time.

.. code-block::

  def handle_ip(self, ethernet, in_port, source):
      (...)
      if dest_mac is not None:
      (...)

      else:
          arp_request = ARP(oper=1)
          arp_request.sha = settings.GW_MAC
          arp_request.tpa = ipv4.destination

          frame = Ethernet()
          frame.source = settings.GW_MAC
          frame.destination = 'ff:ff:ff:ff:ff:ff'
          frame.ether_type = 0x806
          frame.data = arp_request.pack()

          packet_out = PacketOut()
          packet_out.data = frame.pack()
          packet_out.actions.append(ActionOutput(port=Port.OFPP_FLOOD))

          event_out = KytosEvent(name=('tutorial/of_l3ls_v2.messages.out.'
                                       'ofpt_packet_out'),
                                 content={'destination': source,
                                          'message': packet_out})

          self.controller.buffers.msg_out.put(event_out)
          log.info('ARP request sent to %s', ipv4.destination)


Final main.py file
==================

Now your ``main.py`` file shall look like the one below. Here we have all the
needed imports, and comments were removed to improve readability.

.. code-block::

  from kytos.core import KytosEvent, KytosNApp, log
  from kytos.core.helpers import listen_to
  from pyof.foundation.network_types import ARP, Ethernet, IPv4
  from pyof.v0x01.common.action import ActionOutput, ActionDLAddr, ActionType
  from pyof.v0x01.common.flow_match import Match
  from pyof.v0x01.common.phy_port import Port
  from pyof.v0x01.controller2switch.flow_mod import FlowMod, FlowModCommand
  from pyof.v0x01.controller2switch.packet_out import PacketOut

  from napps.tutorial.of_l3ls_v2 import settings


  class Main(KytosNApp):

      def setup(self):
          pass

      def execute(self):
          pass

      @listen_to('kytos/core.switches.new')
      def create_switch_tables(self, event):
          switch = event.content['switch']
          switch.fw_table = {}
          switch.arp_table = {}

      @listen_to('kytos/of_core.v0x01.messages.in.ofpt_packet_in')
      def handle_packet_in(self, event):
          packet_in = event.content['message']

          ethernet = Ethernet()
          ethernet.unpack(packet_in.data.value)

          in_port = packet_in.in_port.value

          if ethernet.ether_type.value == 0x806:
              self.handle_arp(ethernet, in_port, event.source)
          elif ethernet.ether_type.value == 0x800:
              self.handle_ip(ethernet, in_port, event.source)

      def handle_arp(self, ethernet, in_port, source):
          arp = ARP()
          arp.unpack(ethernet.data.value)

          source.switch.arp_table[arp.spa.value] = arp.sha.value
          source.switch.fw_table[arp.spa.value] = in_port

          log.info('Learning %s at port %d with mac %s.', arp.spa.value, in_port,
                   arp.sha.value)

          if arp.oper.value == 1 and arp.tpa.value in settings.GW_IP:
              reply = ARP(oper=2)
              reply.sha = settings.GW_MAC
              reply.spa = arp.tpa
              reply.tha = arp.sha
              reply.tpa = arp.spa

              frame = Ethernet()
              frame.source = settings.GW_MAC
              frame.destination = ethernet.source
              frame.ether_type = 0x806
              frame.data = reply.pack()

              packet_out = PacketOut()
              packet_out.data = frame.pack()
              packet_out.actions.append(ActionOutput(port=in_port))

              event_out = KytosEvent(name=('tutorial/of_l3ls_v2.messages.out.'
                                           'ofpt_packet_out'),
                                     content={'destination': source,
                                              'message': packet_out})

              self.controller.buffers.msg_out.put(event_out)
              log.info('Replygin arp request from %s', arp.spa.value)

      def handle_ip(self, ethernet, in_port, source):
          ipv4 = IPv4()
          ipv4.unpack(ethernet.data.value)

          switch = source.switch

          dest_mac = switch.arp_table.get(ipv4.destination, None)

          log.info('Packet received from %s to %s', ipv4.source,
                   ipv4.destination)

          if dest_mac is not None:
              dest_port = switch.fw_table.get(ipv4.destination)

              flow_mod = FlowMod()
              flow_mod.command = FlowModCommand.OFPFC_ADD
              flow_mod.match = Match()
              flow_mod.match.nw_src = ipv4.source
              flow_mod.match.nw_dst = ipv4.destination
              flow_mod.match.dl_type = 0x800
              flow_mod.actions.append(ActionDLAddr(action_type=ActionType.OFPAT_SET_DL_SRC,
                                                   dl_addr=settings.GW_MAC))
              flow_mod.actions.append(ActionDLAddr(action_type=ActionType.OFPAT_SET_DL_DST,
                                                   dl_addr=dest_mac))
              flow_mod.actions.append(ActionOutput(port=dest_port))

              event_out = KytosEvent(name=('tutorial.of_l3ls_v2.messages.out.'
                                           'ofpt_flow_mod'),
                                     content={'destination': source,
                                              'message': flow_mod})

              self.controller.buffers.msg_out.put(event_out)
              log.info('Flow installed! Subsequent packets will be sent directly.')

          else:
              arp_request = ARP(oper=1)
              arp_request.sha = settings.GW_MAC
              arp_request.tpa = ipv4.destination

              frame = Ethernet()
              frame.source = settings.GW_MAC
              frame.destination = 'ff:ff:ff:ff:ff:ff'
              frame.ether_type = 0x806
              frame.data = arp_request.pack()

              packet_out = PacketOut()
              packet_out.data = frame.pack()
              packet_out.actions.append(ActionOutput(port=Port.OFPP_FLOOD))

              event_out = KytosEvent(name=('tutorial/of_l3ls_v2.messages.out.'
                                           'ofpt_packet_out'),
                                     content={'destination': source,
                                              'message': packet_out})

              self.controller.buffers.msg_out.put(event_out)
              log.info('ARP request sent to %s', ipv4.destination)

      def shutdown(self):
          pass


*****************************
Running and testing your NApp
*****************************

To run your NApp, you need to run *Kytos* first to enable NApp management. In
another terminal window, make sure to activate your |dev_env|_ and run:

.. code-block:: console

  kytosd -f
  2017-08-04 13:00:48,988 - INFO [kytos.core.logs] (MainThread) Logging config file "/home/user/test42/etc/kytos/logging.ini" loaded successfully.
  2017-08-04 13:00:48,991 - INFO [kytos.core.controller] (MainThread) /home/user/test42/var/run/kytos
  2017-08-04 13:00:48,992 - INFO [kytos.core.controller] (MainThread) Starting Kytos - Kytos Controller
  2017-08-04 13:00:48,994 - INFO [kytos.core.tcp_server] (TCP server) Kytos listening at 0.0.0.0:6633
  2017-08-04 13:00:48,996 - INFO [kytos.core.controller] (RawEvent Handler) Raw Event Handler started
  2017-08-04 13:00:48,998 - INFO [kytos.core.controller] (MsgInEvent Handler) Message In Event Handler started
  2017-08-04 13:00:49,000 - INFO [kytos.core.controller] (MsgOutEvent Handler) Message Out Event Handler started
  2017-08-04 13:00:49,001 - INFO [kytos.core.controller] (AppEvent Handler) App Event Handler started
  2017-08-04 13:00:49,001 - INFO [kytos.core.controller] (MainThread) Loading Kytos NApps...
  2017-08-04 13:00:49,067 - INFO [kytos.core.napps.napp_dir_listener] (MainThread) NAppDirListener Started...
  2017-08-04 13:00:49,090 - INFO [kytos.core.controller] (MainThread) Loading NApp kytos/of_core
  2017-08-04 13:00:50,143 - INFO [root] (kytos/of_core) Running NApp: <Main(kytos/of_core, started 139685196187392)>

  (...)

  kytos $>

As you can see, there is a log line indicating that *kytos/of_core* is running.
You need the OpenFlow core NApp installed and enabled. It is possible to check
it by running, in the previous terminal window:

.. code-block:: bash

  $ kytos napps list

  Status |          NApp ID          |                     Description
  =======+===========================+======================================================
   [ie]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsible for...
   [i-]  | kytos/of_flow_manager     | Manage switches' flows through a REST API.
   [i-]  | kytos/of_ipv6drop         | Install flows to DROP IPv6 packets on all switches.
   [i-]  | kytos/of_l2ls             | An L2 learning switch application for OpenFlow swi...
   [i-]  | kytos/of_lldp             | Discovers switches and hosts in the network using ...
   [i-]  | kytos/of_stats            | Provide statistics of openflow switches.
   [i-]  | kytos/of_topology         | Keeps track of links between hosts and switches. R...
   [i-]  | kytos/web_topology_layout | Manage endpoints related to the web interface sett...

If the NApp is installed but not enabled, you can enable it by running:

.. code-block:: console

  $ kytos napps enable kytos/of_core

.. NOTE:: Enable only the kytos/of_core NApp. All other NApps shall be disabled.

Now, install and run the *of_l3ls_v2* NApp:

.. code-block:: console

  $ cd ~/tutorials
  $ kytos napps install tutorial/of_l3ls_v2
  INFO  NApp tutorial/of_l3ls_v2:
  INFO    Searching local NApp...
  INFO    Found and installed.
  INFO    Enabling...
  INFO    Enabled.

With the NApp installed and enabled, you can run Mininet to see it in action.
This time, the network topology will have two hosts from different logical
networks, 10.0.0.1 and 20.0.0.1, connected to the switch. Run Mininet using the
command below:

.. ATTENTION:: This NApp was designed for this specific topology. It will NOT
    work in topologies containing more than a single switch.

.. code-block:: console

  $ sudo mn -c ; sudo mn --controller remote --switch ovsk,protocols=OpenFlow10

.. IMPORTANT:: As no specific topology configuration was passed to Mininet, it
    will generate a virtual network with a switch connecting two hosts, 10.0.0.1
    and 10.0.0.2.

Now, in the Mininet console, you must configure the IP addresses for the hosts,
pointing their default gateways at the IP addresses defined in the settings.
To do it, run the commands:

.. code-block:: console

  mininet> h1 ip route add default via 10.0.0.100
  mininet> h2 ip addr del 10.0.0.2/8 dev h2-eth0
  mininet> h2 ip addr add 20.0.0.1/8 dev h2-eth0
  mininet> h2 ip route add default via 20.0.0.100
  mininet>

Finally, use the *ping* command to verify your NApp working:

.. code-block:: console

  mininet> h1 ping h2
  PING 20.0.0.1 (20.0.0.1) 56(84) bytes of data.
  64 bytes from 20.0.0.1: icmp_seq=4 ttl=64 time=0.435 ms
  64 bytes from 20.0.0.1: icmp_seq=5 ttl=64 time=0.113 ms
  64 bytes from 20.0.0.1: icmp_seq=6 ttl=64 time=0.113 ms
  64 bytes from 20.0.0.1: icmp_seq=7 ttl=64 time=0.113 ms
  64 bytes from 20.0.0.1: icmp_seq=8 ttl=64 time=0.104 ms
  64 bytes from 20.0.0.1: icmp_seq=9 ttl=64 time=0.127 ms

The pings are sucessful! Communication between the hosts is possible because the
*of_l3ls_v2* NApp has dealt with the Flows correctly. You can check it by
looking at the controller logs:

.. code-block:: console

  2017-08-04 13:06:27,094 - INFO [tutorial/of_l3ls_v2] (Thread-216) Learning 10.0.0.1 at port 1 with mac da:56:82:67:77:3b.
  2017-08-04 13:06:27,110 - INFO [tutorial/of_l3ls_v2] (Thread-216) Replygin arp request from 10.0.0.1
  2017-08-04 13:06:27,137 - INFO [tutorial/of_l3ls_v2] (Thread-218) Packet received from 10.0.0.1 to 20.0.0.1
  2017-08-04 13:06:27,148 - INFO [tutorial/of_l3ls_v2] (Thread-218) ARP request sent to 20.0.0.1
  2017-08-04 13:06:27,158 - INFO [tutorial/of_l3ls_v2] (Thread-220) Learning 20.0.0.1 at port 2 with mac 1a:9c:0e:4e:28:50.
  2017-08-04 13:06:28,113 - INFO [tutorial/of_l3ls_v2] (Thread-222) Packet received from 10.0.0.1 to 20.0.0.1
  2017-08-04 13:06:28,128 - INFO [tutorial/of_l3ls_v2] (Thread-222) Flow installed! Subsequent packets will be sent directly.
  2017-08-04 13:06:29,132 - INFO [tutorial/of_l3ls_v2] (Thread-224) Learning 20.0.0.1 at port 2 with mac 1a:9c:0e:4e:28:50.
  2017-08-04 13:06:29,136 - INFO [tutorial/of_l3ls_v2] (Thread-224) Replygin arp request from 20.0.0.1
  2017-08-04 13:06:29,151 - INFO [tutorial/of_l3ls_v2] (Thread-226) Packet received from 20.0.0.1 to 10.0.0.1
  2017-08-04 13:06:29,160 - INFO [tutorial/of_l3ls_v2] (Thread-226) Flow installed! Subsequent packets will be sent directly.

Note that when the first ICMP packet arrives, the controller does not know the
destination MAC and generates an ARP request, learning it just after the reply.
As the next packet is sent, a flow is installed in the switch. Once the flows
are set in both directions, the switch sends the packets direclty.

We can check the ARP tables in the controller and in each host to see every address
was learnt properly. In the mininet console, run:

.. code-block:: console

  mininet> h1 arp
  Endereço TipoHW EndereçoHW Flags Máscara Iface
  10.0.0.100               ether   10:20:30:40:50:60   C                     h1-eth0

  mininet> h2 arp
  Endereço TipoHW EndereçoHW Flags Máscara Iface
  20.0.0.100               ether   10:20:30:40:50:60   C                     h2-eth0

Each host knows its own gateway, as expected. The controller knows each host's IP
address and MAC address as well. In the Kytos console, run:

.. code-block:: console

  kytos $> controller.switches["00:00:00:00:00:00:00:01"].arp_table
  Out[1]: {'10.0.0.1': 'da:56:82:67:77:3b', '20.0.0.1': '1a:9c:0e:4e:28:50'}

Good job!

.. include:: ../back_to_list.rst

.. |ARP| replace:: *ARP*
.. _ARP: https://en.wikipedia.org/wiki/Address_Resolution_Protocol

.. |routing| replace:: *routing tables*
.. _routing: https://en.wikipedia.org/wiki/Routing_table

.. |L3_part1| replace:: *the previous tutorial*
.. _L3_part1: http://tutorials.kytos.io/napps/switch_l3_part1

.. |kytos| replace:: *Kytos*
.. _kytos: http://docs.kytos.io/kytos

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/
