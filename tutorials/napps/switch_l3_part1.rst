:tocdepth: 2
:orphan:

.. _tutorial-create-l3-sw-1:

######################################
Creating an L3 learning switch: Part 1
######################################

********
Overview
********
This tutorial will show the first steps to create an L3 learning switch NApp
using *Kytos* (|kytos|_).
The average time to go through this is: ``20 min``

What you will learn
====================
* How to unpack the Packet-In data looking for L3 information;
* How to install proactive flows in switches using Kytos.

What you will need
===================
* Your |dev_env|_ already up and running.
* The *kytos/of_core* NApp installed and enabled.
* To have finished the |l2_tutorial|_.

************
Introduction
************

Layer 3
=======
*Layer 3* refers to the *Network layer*, the third one in the |osi_model|_. This layer
is responsible for defining logical addresses and identification for network
devices.

The |ip_proto|_, used in the Internet for example, is the most relevant implementation
for this layer. IP addresses, like '192.168.10.1', are essentialy Layer 3 addresses.

The L3 learning switch
======================

The Layer 3 learning switch will operate similarly to the |l2ls|_,
but working with IP addresses instead of MAC addresses.

The *l3ls* NApp will learn at which port each IP address is, and install reactive
flows in switches to handle traffic based on source IP and destination IP. ARP
packets will be just flooded to the network, because they have different headers.

Is this a router?
=================

No. A router should be capable of switching packets between different networks, and
to actively communicate with hosts using protocols such as ARP and ICMP. We will cover
the steps to implement routing in future tutorials.

For this implementation of *l3ls*, we will consider that hosts are in the same logical
network.

.. NOTE:: We are also considering the addresses to be IPv4 addresses.

.. ATTENTION:: This NApp was designed for instructional purposes. Running it in
    production environments may lead to unwanted behavior.

Before proceeding to the next section of this tutorial, go to the
|napps_server_sign_up| in order to create a user for you on our
|napps_server|_. After you submit the form you will receive an email to confirm
your registration. Click on the link present on the email body and, after
seeing the confirmation message on the screnn, go to the next section.

******************
Creating your NApp
******************

First, create your NApp using the ``kytos`` command. Use your **<username>**
(the one you have just registered) as the username and 'of_l3ls' as the NApp name,
as follows (don't forget to create the ``~/tutorials`` folder if it does not exist):

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

  Please, insert your NApps Server username: <username>
  Please, insert your NApp name: of_l3ls
  Please, insert a brief description for your NApp [optional]: This NApp does packet switching using L3 information

  Congratulations! Your NApp have been bootstrapped!
  Now you can go to the directory <username>/of_l3ls and begin to code your NApp.
  Have fun!

Start copying the ``main.py`` file from the |l2_tutorial|_: you'll change it to
use L3 information instead of L2. Then, open it in your preferred editor to start
coding your NApp.

.. code-block:: console

  $ cp <username>/of_l2ls/main.py <username>/of_l3ls/main.py

Create an L3 switching table
============================

First of all, you will create an L3 table for each switch that connects to the
controller. When a new switch is connected, *Kytos* generates a ``core.switch.new``
KytosEvent. Your NApp will have a method to deal with those.

The L3 table will be a Python dictionary, mapping IP addresses to switch ports.

.. code-block:: python3

  @listen_to('kytos/core.switch.new')
  def initialize_switch(self, event):
      switch = event.content['switch']
      switch.l3_table = {}

      # (Continues...)


Deal with the ARP packets
=========================

When you perform packet switchin with L3 information, you have to deal separately with
ARP. ARP packets will be sent in the network with a source MAC and a destination MAC,
enabling the L2 learning switch to exchange them properly, but they have different
L3 headers and do not carry a source IP or destination IP.

The naive solution is to just flood ARP packets, in a 'hub-like' behavior, without even
sending them to the controller. While the L2 learning switch is only *reactive*, the
L3 switch will have *proactive* flows matching ARP.

.. code-block:: python3

  @listen_to('kytos/core.switch.new')
  def initialize_switch(self, event):
      # (...)

      arp_flow_mod = FlowMod()
      arp_flow_mod.command = FlowModCommand.OFPFC_ADD
      arp_flow_mod.match = Match()
      arp_flow_mod.match.dl_type = EtherType.ARP
      arp_flow_mod.actions.append(ActionOutput(port=Port.OFPP_FLOOD))
      event_out = KytosEvent(name=('<username>/of_l3ls.messages.out.'
                                   'ofpt_flow_mod'),
                             content={'destination': switch.connection,
                                      'message': arp_flow_mod})
      self.controller.buffers.msg_out.put(event_out)


Change ``handle_packet_in`` to use L3 information
=================================================

Updating the L3 table
---------------------
To update the switch's L3 table, you need to get the IPV4 information of the
PacketIn sent to the controller. You'll do it with one more ``unpack`` on the
data field of the Ethernet frame. It's important to check if it is an IPV4 packet
before the unpack, to avoid errors. Once unpacked, you can add the source IP to the
L3 table. The needed changes are shown below:

.. code-block:: python3

  @listen_to('kytos/of_core.v0x01.messages.in.ofpt_packet_in')
  def handle_packet_in(self, event):
      #(...)
      ethernet.unpack(packet_in.data.value)
  
      # Add the unpack here
      if ethernet.ether_type = EtherType.IPV4
          ipv4 = IPv4()
          ipv4.unpack(ethernet.data.value)
          
          in_port = packet_in.in_port.value
          switch = event.source.switch
          switch.l3_table[ipv4.source] = in_port
          log.info('Packet received from %s to %s.', ipv4.source,
                   ipv4.destination)

          # To look for the port, we will use the dictionary's get() method.
          dest_port = switch.l3_table.get(ipv4.destination, None)

.. note:: All further code will be inside the above `if` statement. Check the
    final main.py file in case of doubt.

.. warning:: As dest_port is now a single port and not a list, remove the
    subscript (from dest_ports[0] to dest_port) in all the code.

Installing FlowMods with L3 information
---------------------------------------
To use L3 information on flows, you will change two lines used while constructing
the FlowMod message.

.. code-block:: python3

  # flow_mod.match.dl_src = ethernet.source.value
  # flow_mod.match.dl_dst = ethernet.destination.value
  # Remove the lines above, using instead:
  flow_mod.match.nw_src = ipv4.source
  flow_mod.match.nw_dst = ipv4.destination

You don't need to change the PacketOut code: it shall work the same.

Final main.py file
==================

Now your ``main.py`` file shall look like the one below. Here we have all the
needed imports, and comments were removed to improve readability.

.. code-block:: python3

    from kytos.core import KytosEvent, KytosNApp, log
    from kytos.core.helpers import listen_to
    from pyof.foundation.network_types import Ethernet, EtherType, IPv4
    from pyof.v0x01.common.action import ActionOutput
    from pyof.v0x01.common.flow_match import Match
    from pyof.v0x01.common.phy_port import Port
    from pyof.v0x01.controller2switch.flow_mod import FlowMod, FlowModCommand
    from pyof.v0x01.controller2switch.packet_out import PacketOut

    from napps.<username>.of_l3ls import settings


    class Main(KytosNApp):
        def setup(self):
            pass

        def execute(self):
            pass

        @listen_to('kytos/core.switch.new')
        def create_switching_table(self, event):
            switch = event.content['switch']
            switch.l3_table = {}
            
            arp_flow_mod = FlowMod()
            arp_flow_mod.command = FlowModCommand.OFPFC_ADD
            arp_flow_mod.match = Match()
            arp_flow_mod.match.dl_type = EtherType.ARP
            arp_flow_mod.actions.append(ActionOutput(port=Port.OFPP_FLOOD))
            event_out = KytosEvent(name=('<username>/of_l3ls.messages.out.'
                                   'ofpt_flow_mod'),
                             content={'destination': switch.connection,
                                      'message': arp_flow_mod})
            self.controller.buffers.msg_out.put(event_out)

        @listen_to('kytos/of_core.v0x01.messages.in.ofpt_packet_in')
        def handle_packet_in(self, event):
            packet_in = event.content['message']

            ethernet = Ethernet()
            ethernet.unpack(packet_in.data.value)

            if ethernet.ether_type.value == EtherType.IPV4:
                ipv4 = IPv4()
                ipv4.unpack(ethernet.data.value)

                in_port = packet_in.in_port.value
                switch = event.source.switch
                switch.l3_table[ipv4.source] = in_port
                log.info('Packet received from %s to %s.', ipv4.source,
                         ipv4.destination)

                dest_port = switch.l3_table.get(ipv4.destination, None)

                if dest_port is not None:
                    log.info('%s is at port %d.', ipv4.destination, dest_port)
                    flow_mod = FlowMod()
                    flow_mod.command = FlowModCommand.OFPFC_ADD
                    flow_mod.match = Match()
                    flow_mod.match.nw_src = ipv4.source
                    flow_mod.match.nw_dst = ipv4.destination
                    flow_mod.match.dl_type = ethernet.ether_type
                    flow_mod.actions.append(ActionOutput(port=dest_port))
                    event_out = KytosEvent(name=('<username>/of_l3ls.messages.out.'
                                                 'ofpt_flow_mod'),
                                           content={'destination': event.source,
                                                    'message': flow_mod})
                    self.controller.buffers.msg_out.put(event_out)
                    log.info('Flow installed! Subsequent packets will be sent directly.')

                packet_out = PacketOut()
                packet_out.buffer_id = packet_in.buffer_id
                packet_out.in_port = packet_in.in_port
                packet_out.data = packet_in.data

                port = dest_port if dest_port is not None else Port.OFPP_FLOOD
                packet_out.actions.append(ActionOutput(port=port))
                event_out = KytosEvent(name=('<username>/of_l3ls.messages.out.'
                                             'ofpt_packet_out'),
                                       content={'destination': event.source,
                                                'message': packet_out})

                self.controller.buffers.msg_out.put(event_out)

        def shutdown(self):
            pass



*****************************
Running and testing your NApp
*****************************

To run your NApp, you need to run *Kytos* first to enable NApp management. In
another terminal window, make sure to activate your |dev_env|_ and run:

.. code-block:: console

  $ kytosd -f
  2017-07-25 14:45:35,135 - INFO [kytos.core.logs] (MainThread) Logging config file "/home/user/test42/etc/kytos/logging.ini" loaded successfully.
  2017-07-25 14:45:35,137 - INFO [kytos.core.controller] (MainThread) /home/user/test42/var/run/kytos
  2017-07-25 14:45:35,137 - INFO [kytos.core.controller] (MainThread) Starting Kytos - Kytos Controller
  2017-07-25 14:45:35,139 - INFO [kytos.core.tcp_server] (TCP server) Kytos listening at 0.0.0.0:6653
  2017-07-25 14:45:35,142 - INFO [kytos.core.controller] (RawEvent Handler) Raw Event Handler started
  2017-07-25 14:45:35,144 - INFO [kytos.core.controller] (MsgInEvent Handler) Message In Event Handler started
  2017-07-25 14:45:35,148 - INFO [kytos.core.controller] (MsgOutEvent Handler) Message Out Event Handler started
  2017-07-25 14:45:35,148 - INFO [kytos.core.controller] (AppEvent Handler) App Event Handler started
  2017-07-25 14:45:35,148 - INFO [kytos.core.controller] (MainThread) Loading Kytos NApps...
  2017-07-25 14:45:35,153 - INFO [kytos.core.napps.napp_dir_listener] (MainThread) NAppDirListener Started...
  2017-07-25 14:45:35,155 - INFO [kytos.core.controller] (MainThread) Loading NApp kytos/of_core
  2017-07-25 14:45:35,612 - INFO [root] (kytos/of_core) Running NApp: <Main(kytos/of_core, started 140029615662848)>

  (...)

  kytos $>

As you can see, there is a log line indicating that *kytos/of_core* is running.
You need the OpenFlow core NApp installed and enabled. It is possible to check
it by running, in the previous terminal window:

.. code-block:: console

  $ kytos napps list

  Status |          NApp ID          |                     Description
  =======+===========================+======================================================
   [ie]  | kytos/of_core             | OpenFlow Core of Kytos Controller, responsible for...
   [i-]  | kytos/flow_manager        | Manage switches' flows through a REST API.
   [i-]  | kytos/of_l2ls             | An L2 learning switch application for OpenFlow swi...
   [i-]  | kytos/of_lldp             | Discovers switches and hosts in the network using ...
   [i-]  | kytos/of_stats            | Provide statistics of openflow switches.
   [i-]  | kytos/topology            | Keeps track of links between hosts and switches. R...

If the NApp is installed but not enabled, you can enable it by running:

.. code-block:: console

  $ kytos napps enable kytos/of_core

In order to run your NApp, you can install it locally or remotely:

To install locally, you have to run the following commands:

.. code-block:: console

  $ cd ~/tutorials/<username>/of_l3ls
  $ python3 setup.py develop

To install remotely, you have to publish it first:

.. code-block:: console

  $ cd ~/tutorials/<username>/of_l3ls
  $ kytos napps upload
  Enter the username: <username>
  Enter the password for <username>: <password>
  SUCCESS: NApp <username>/of_l3ls uploaded.

Now that you have published your NApp, you can access |napps_server|_ and see
that it was sent. After that, install and run the *<username>/of_l3ls* NApp:

.. code-block:: console

  $ cd ~/tutorials
  $ kytos napps install <username>/of_l3ls
  INFO  NApp <username>/of_l3ls:
  INFO    Searching local NApp...
  INFO    Found and installed.
  INFO    Enabling...
  INFO    Enabled.

With the NApp installed and enabled, you can run Mininet to see it in action:

.. code-block:: console

  $ sudo mn -c ; sudo mn --controller remote --switch ovsk,protocols=OpenFlow10

.. IMPORTANT:: As no specific topology configuration was passed to Mininet, it
    will generate a virtual network with a switch connecting two hosts, 10.0.0.1
    and 10.0.0.2.

.. ATTENTION:: Just like the l2ls implementation, this NApp will NOT work in
    topologies containing loops. However, it works with linear and tree topologies.

Now, in the Mininet console, run:

.. code-block:: console

  mininet> h1 ping h2
  PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
  64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=83.3 ms
  64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=66.6 ms
  64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.495 ms
  64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.117 ms
  64 bytes from 10.0.0.2: icmp_seq=5 ttl=64 time=0.114 ms

The pings are sucessful! Communication between the hosts is possible because the
*of_l3ls* NApp has dealt with the Flows. You can check it by looking at the controller
logs:

.. code-block:: console

  2017-07-25 16:04:07,150 - INFO [<username>/of_l3ls] (Thread-88) Packet received from 10.0.0.1 to 10.0.0.2.
  2017-07-25 16:04:07,165 - INFO [<username>/of_l3ls] (Thread-90) Packet received from 10.0.0.2 to 10.0.0.1.
  2017-07-25 16:04:07,166 - INFO [<username>/of_l3ls] (Thread-90) 10.0.0.1 is at port 1.
  2017-07-25 16:04:07,177 - INFO [<username>/of_l3ls] (Thread-90) Flow installed! Subsequent packets will be sent directly.
  2017-07-25 16:04:08,148 - INFO [<username>/of_l3ls] (Thread-94) Packet received from 10.0.0.1 to 10.0.0.2.
  2017-07-25 16:04:08,150 - INFO [<username>/of_l3ls] (Thread-94) 10.0.0.2 is at port 2.
  2017-07-25 16:04:08,163 - INFO [<username>/of_l3ls] (Thread-94) Flow installed! Subsequent packets will be sent directly.

Once the flows are set in both directions, the switch sends the packets direclty.
Good job!

.. include:: ../back_to_list.rst

.. |osi_model| replace:: *OSI Model*
.. _osi_model: https://en.wikipedia.org/wiki/OSI_model

.. |ip_proto| replace:: *IP protocol*
.. _ip_proto: https://en.wikipedia.org/wiki/Internet_Protocol

.. |l2ls| replace:: *Layer 2 learning switch*
.. _l2ls: https://github.com/kytos/kytos-napps/tree/master/napps/kytos/of_l2ls

.. |kytos| replace:: *Kytos*
.. _kytos: http://docs.kytos.io/kytos

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/

.. |l2_tutorial| replace:: *L2 Learning Switch tutorial*
.. _l2_tutorial: http://tutorials.kytos.io/napps/switch_l2/

.. |napps_server| replace:: *NApps Server*
.. _napps_server: http://napps.kytos.io

.. |napps_server_sign_up| replace:: **sign_up**
.. _napps_server_sign_up: https://napps.kytos.io/signup/
