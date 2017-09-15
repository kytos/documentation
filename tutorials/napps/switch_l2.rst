:tocdepth: 2
:orphan:

.. _tutorial-create-l2-sw:

#######################################
Creating an L2 learning switch - Part 1
#######################################

********
Overview
********
This tutorial will show you how to create an L2 learning switch NApp
using *Kytos* (|kytos|_).
The average time to go through this is: ``25 min``

What you will learn
====================
* How to capture OpenFlow Packet-In events;
* How to unpack the Packet-In data looking for L2 information;
* How to install flows in a switch.

What you will need
===================
* Your |dev_env|_ already up and running.
* The *kytos/of_core* NApp installed and enabled.

************
Introduction
************

Layer 2
=======
*Layer 2* refers to the *Data Link layer*, the third one in the |osi_model|_. This layer
is responsible for defining interfaces's fixed addresses for transmitting frames
in a network as well as control the Physical layer.

The |ethernet|_ standard is widely adopted for |lans|_, and will be used in this
tutorial.

The L2 learning switch
======================

The Layer 2 learning switch must be able to exchange frames between devices in
the network automatically, identifying interfaces by their |macs|_, learning where
each one is located and installing reactive flows in switches, handling the traffic
based on the source/destination MACs.

******************
Creating your NApp
******************

First, create your NApp using the ``kytos`` command. Use 'tutorial' as the
username and 'of_l2ls' as the NApp name, as follows (don't forget to create
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
  Please, insert your NApp name: of_l2ls
  Please, insert a brief description for your NApp [optional]: This NApp does packet switching using L2 information

  Congratulations! Your NApp have been bootstrapped!
  Now you can go to the directory tutorial/of_l2ls and begin to code your NApp.
  Have fun!

Open the ``main.py`` file in your preferred editor to start coding your NApp.

.. ATTENTION:: Some classes and methods used in the code snippets need to be imported
    in your main.py file. Please check the full content of the file and import these
    elements as needed.


Update switching table with incoming packets
============================================

In this first step, you will create a method to handle PacketIn events. A PacketIn is
generated everytime the switchs sends a packet to the controller for analysis.

The method has a decorator to listen to *packet in* events. It unpacks the
``packet_in.data`` into an Ethernet instance.

Once you have the Ethernet header information, you can use it to update the
switching table, associating it with the *in_port* - the physical switch
interface where the packet came from.

You can also add a log message to know when the controller receives a packet.

.. code-block:: python3

    @listen_to('kytos/of_core.v0x01.messages.in.ofpt_packet_in')
    def handle_packet_in(self, event):
        packet_in = event.content['message']

        ethernet = Ethernet()
        ethernet.unpack(packet_in.data.value)

        in_port = packet_in.in_port.value
        switch = event.source.switch
        switch.update_mac_table(ethernet.source, in_port)
        log.info('Packet received from %s to %s.', ethernet.source.value',
                 ethernet.destination.value)

            # (Continues...)

Create Flow Mods for MAC addresses
==================================

The next step is to check if the switch already knows from which port the destination
address is reachable. You will look for it using the ``where_is_mac`` method.

If the switch does know where the packet shall go to, then you will install a Flow in it so
new packets with the same source and destination addresses will be directly and
correctly forwarded, without needing the controller.
The Flow will instruct the switch to handle those new packets himself.

Your Flow Mod message shall have:
 - A Flow Mod Command: as this is a new Flow, the command is OFPFC_ADD;
 - A Flow Match: A match has all information you want the switch to check before
   deciding if the packet belongs to this particular flow. You want the switch to match the
   source MAC address, the destination MAC address and the Ethernet type;
 - A list of Actions: All the actions to be performed on the incoming packet are
   executed by the switch. Given this is a switching NApp, you want the switch
   to send the packet through the correct port, defined by the controller.

.. note:: You can add more restrictions to your OpenFlow Match, like the VLAN ID
    or PCP if your environment needs that.

Once you have prepared the Flow Mod, create a KytosEvent containing it directed to the switch
that sent you the PacketIn, and put this event in the ``msg_out`` buffer.

.. code-block:: python3

    @listen_to('kytos/of_core.v0x01.messages.in.ofpt_packet_in')
    def handle_packet_in(self, event):
        # (...)

        dest_ports = switch.where_is_mac(ethernet.destination)

        if dest_ports:
            log.info('%s is at port %d.', ethernet.destination.value, dest_ports[0])
            flow_mod = FlowMod()
            flow_mod.command = FlowModCommand.OFPFC_ADD
            flow_mod.match = Match()
            flow_mod.match.nw_src = ethernet.source.value
            flow_mod.match.nw_dst = ethernet.destination.value
            flow_mod.match.dl_type = ethernet.ether_type
            # Example: matching the VLAN ID 200:
            # flow_mod.match.dl_vlan = 200
            flow_mod.actions.append(ActionOutput(port=dest_ports[0]))
            event_out = KytosEvent(name=('tutorial/of_l2ls.messages.out.'
                                         'ofpt_flow_mod'),
                                   content={'destination': event.source,
                                            'message': flow_mod})
            self.controller.buffers.msg_out.put(event_out)
            log.info('Flow installed! Subsequent packets will be sent directly.')

        # (Continues...)

Send the packet back to the network
===================================

Whether your switch found a destination or not, the flow installed on the previous
step will work only for new incoming packets. There is still need to handle this
particular packet that generated the PacketIn event.

Create a PacketOut with the content of the PacketIn (same buffer_id, in_port
and data). If the controller knows the packet destination, then you can send it
right away through the proper port. If the controller does not know it, then tell
the switch to *flood* the packet: send it to all ports except the in_port.

Once again, create a KytosEvent and put it in the ``msg_out`` buffer.

.. code-block:: python3

    @listen_to('kytos/of_core.v0x01.messages.in.ofpt_packet_in')
    def handle_packet_in(self, event):
        # (...)

        if dest_ports:
            # (...)

        packet_out = PacketOut()
        packet_out.buffer_id = packet_in.buffer_id
        packet_out.in_port = packet_in.in_port
        packet_out.data = packet_in.data

        port = dest_ports[0] if dest_ports else Port.OFPP_FLOOD
        packet_out.actions.append(ActionOutput(port=port))
        event_out = KytosEvent(name=('tutorial/of_l2ls.messages.out.'
                                     'ofpt_packet_out'),
                               content={'destination': event.source,
                                        'message': packet_out})

        self.controller.buffers.msg_out.put(event_out)


Final main.py file
==================

Now your ``main.py`` file shall look like the one below. Here we have all the
needed imports, and comments were removed to improve readability.

.. code-block:: python3

  from kytos.core import KytosEvent, KytosNApp, log
  from kytos.core.helpers import listen_to
  from pyof.foundation.network_types import Ethernet
  from pyof.v0x01.asynchronous.packet_in import PacketInReason
  from pyof.v0x01.common.action import ActionOutput
  from pyof.v0x01.common.flow_match import Match
  from pyof.v0x01.common.phy_port import Port
  from pyof.v0x01.controller2switch.flow_mod import FlowMod, FlowModCommand
  from pyof.v0x01.controller2switch.packet_out import PacketOut
  
  from napps.tutorial.of_l2ls import settings
  
  
  class Main(KytosNApp):
  
      def setup(self):
          pass
  
      def execute(self):
          pass
  
      @listen_to('kytos/of_core.v0x01.messages.in.ofpt_packet_in')
      def handle_packet_in(self, event):
          packet_in = event.content['message']
  
          ethernet = Ethernet()
          ethernet.unpack(packet_in.data.value)
  
          in_port = packet_in.in_port.value
          switch = event.source.switch
          switch.update_mac_table(ethernet.source, in_port)
          log.info('Packet received from %s to %s.', ethernet.source.value',
                 ethernet.destination.value)
  
          dest_ports = switch.where_is_mac(ethernet.destination)
  
          if dest_ports:
              log.info('%s is at port %d.', ethernet.destination.value, dest_ports[0])
              flow_mod = FlowMod()
              flow_mod.command = FlowModCommand.OFPFC_ADD
              flow_mod.match = Match()
              flow_mod.match.dl_src = ethernet.source.value
              flow_mod.match.dl_dst = ethernet.destination.value
              flow_mod.match.dl_type = ethernet.ether_type
              flow_mod.actions.append(ActionOutput(port=dest_ports[0]))
              event_out = KytosEvent(name=('tutorial/of_l2ls.messages.out.'
                                           'ofpt_flow_mod'),
                                     content={'destination': event.source,
                                              'message': flow_mod})
              self.controller.buffers.msg_out.put(event_out)
              log.info('Flow installed! Subsequent packets will be sent directly.')
  
          packet_out = PacketOut()
          packet_out.buffer_id = packet_in.buffer_id
          packet_out.in_port = packet_in.in_port
          packet_out.data = packet_in.data
  
          port = dest_ports[0] if dest_ports else Port.OFPP_FLOOD
          packet_out.actions.append(ActionOutput(port=port))
          event_out = KytosEvent(name=('tutorial/of_l2ls.messages.out.'
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
  2017-07-25 14:45:35,139 - INFO [kytos.core.tcp_server] (TCP server) Kytos listening at 0.0.0.0:6633
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

Now, install and run the *tutorial/of_l2ls* NApp:

.. code-block:: console

  $ cd ~/tutorials
  $ kytos napps install tutorial/of_l2ls
  INFO  NApp tutorial/of_l2ls:
  INFO    Searching local NApp...
  INFO    Found and installed.
  INFO    Enabling...
  INFO    Enabled.

With the NApp installed and enabled, you can run Mininet to see it in action:

.. code-block:: console

  $ sudo mn -c ; sudo mn --controller remote --switch ovsk,protocols=OpenFlow10

.. IMPORTANT:: As no specific topology configuration was passed to Mininet, it
    will generate a virtual network with a switch connecting two hosts, 10.0.0.1
    and 10.0.0.2. If you want friendly MAC addresses, add the --mac flag.

.. ATTENTION:: This NApp will NOT work in topologies containing loops. However,
    it works with linear and tree topologies.

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
*tutorial/of_l2ls* NApp has dealt with the Flows. You can check it by looking at the controller
logs:

.. code-block:: console

  2017-07-25 16:04:07,150 - INFO [tutorial/of_l2ls] (Thread-88) Packet received from 00:00:af:d5:38:98 to 00:00:1a:1e:9a:cf.
  2017-07-25 16:04:07,165 - INFO [tutorial/of_l2ls] (Thread-90) Packet received from 00:00:1a:1e:9a:cf to 00:00:af:d5:38:98.
  2017-07-25 16:04:07,166 - INFO [tutorial/of_l2ls] (Thread-90) 00:00:af:d5:38:98 is at port 1.
  2017-07-25 16:04:07,177 - INFO [tutorial/of_l2ls] (Thread-90) Flow installed! Subsequent packets will be sent directly.
  2017-07-25 16:04:08,148 - INFO [tutorial/of_l2ls] (Thread-94) Packet received from 00:00:af:d5:38:98 to 00:00:1a:1e:9a:cf.
  2017-07-25 16:04:08,150 - INFO [tutorial/of_l2ls] (Thread-94) 00:00:1a:1e:9a:cf is at port 2.
  2017-07-25 16:04:08,163 - INFO [tutorial/of_l2ls] (Thread-94) Flow installed! Subsequent packets will be sent directly.

Once the flows are set in both directions, the switch sends the packets direclty.
Good job!

.. include:: ../back_to_list.rst

.. |osi_model| replace:: *OSI Model*
.. _osi_model: https://en.wikipedia.org/wiki/OSI_model

.. |ethernet| replace:: *Ethernet*
.. _ethernet: https://en.wikipedia.org/wiki/Ethernet

.. |lans| replace:: *Local Area Networks*
.. _lans: https://en.wikipedia.org/wiki/Local_area_network

.. |macs| replace:: *MAC Addresses*
.. _macs: https://en.wikipedia.org/wiki/MAC_address

.. |kytos| replace:: *Kytos*
.. _kytos: http://docs.kytos.io/kytos

.. |dev_env| replace:: *Development Environment*
.. _dev_env: http://tutorials.kytos.io/napps/development_environment_setup/
