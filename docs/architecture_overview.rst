Architecture Overview
=====================

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

Main Components
---------------
Following we give more details on the components listed above. The rational
behind the separation of such components is to clearly define the main
responsibilities needed to take care of in order to build an OpenFlow based
network. 

Kytos OpenFlow Library - python3-openflow
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
[Examples of linking to another project: section :doc:`toc/introduction`,
class :class:`~pyof.foundation.base.GenericType` (if the last fails, check
pyof's doc build).]

The main responsibility of this component is to read binary OpenFlow messages
and building primary data structures from them. All structures are subclasses
of the special class :class:`~pyof.foundation.base.GenericType`. From this
class we derived the primitive data types and also complex data types, which
includes the OpenFlow messages themselves.

Another primary responsibility of this component is to transform the message
objects into binary blobs that latter will be sent to the switches. 


Kytos Controller - Kyco
~~~~~~~~~~~~~~~~~~~~~~~

[For more information about the kyco component, please visit the kyco
documentation]



Kytos Core Napps - kyco-core-napps
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

