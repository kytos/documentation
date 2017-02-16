############
Architecture
############

========
Overview
========

The Kytos project works as an umbrella for a multi-component architecture, in
which any of the component is interchangeable. That means that adopters of
this project are free to replace any of its components with a customized
version or a whole new component.

The core components inside this architecture are: (a) a library for parsing
OpenFlow messages; (b) a controller to provide a state machine which implements
the OpenFlow protocol, and also delivers a communication mechanism that allows
apps to communicate with each other; and (c) a set of core applications that
allows any systems administrator to deploy a (basic) SDN based infrastructure,
providing communication between nodes, monitoring capability and an
administrative interface that allows one to visualize the network topology and
to deploy flows. 

===============
Main Components
===============
Following we give more details on the components listed above. The rational
behind the separation of such components is to clearly define the main
responsibilities needed to take care of in order to build an OpenFlow based
network.

Kytos OpenFlow Library - python3-openflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The main responsibility of this component is to read binary OpenFlow messages
and building primary data structures from them. We've developed a set of basic
classes that is really similar to the specification, so, anyone who reads the
specification will be able to use this library. 

Another primary responsibility of this component is to transform the message
objects into binary blobs that latter will be sent to the switches.

For more information on python3-openflow, please refer to its documentation.

Kytos Controller - Kyco
~~~~~~~~~~~~~~~~~~~~~~~

As stated before, the controller is the component responsible for providing the
communication infrastructure, registering, loading and unloading apps. It works
on a completely asynchronous way, thus allowing to cope with scalability
issues.

The controller basically define three queues, one for arriving messages, one
for app events and the last one for outgoing messages. The apps must register
to specific queue change events, such as: new packet-in arrival. 

The communication between apps is also possible by means of the app event
buffer.

For more information on Kyco, please refer to its documentation.

Kytos Core Napps - kyco-core-napps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Core Napps package delivers the baisc Napps that allow a system
administrator to deploy a basic infrastructure that relies on OpenFlow to
provide communication between nodes, statistics and topology finding. The
Napps inside this set are:

- of.core: provides communication and event management for all Napps; 
- of.flow-manager: provides a service that allows to manipulate the flow table
  inside the switches;
- of.ipv6drop: a basic firewall Napp that drops all packages that use IP v6
  protocol;
- of.l2ls: a basic layer 2 learning switch;
- of.l2lsloop: the same as the l2ls but with the ability to handle topology
  loops;
- of.liveness: keeps the communication between the controller and the openflow
  switches;
- of.lldp: injects Link Layer Discovery Protocol (LLDP) packets in the
  network in order to detect the connection between switches, thus allowing to
  discover the topology;
- of.stats: continuously collect OpenFlow statistics from the switch ports and
  the flows themselves;
- of.topology: responsible for discovering the connection between a common
  host and a switch port;
- web.topology.layout: this Napp is used by the Web Interface and allows a
  user to save and restore a topology layout manually defined.

