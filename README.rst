Introduction
============
The kytos project was conceived to fill a gap left by common popular
controllers: a controller that could be easily deployed and that was centered
on the development of applications by its users. Thus, our intention is not
only to build a new OpenFlow controller, but also build a community of
developers around it, creating new applications that benefit from the SDN
paradigm. 

The project was born in 2014, when the first version of the message parsing
library was built. After some time stalled, the development took off in earlier
2016.

In less than a year a new library was built, following a strictly free open
source software philosophy. Also, a new controller and a basic set of network
applications known as NApps was developed. 

Our team is mainly composed by Computer Scientist and Engineers and some of us
have participated in several demonstrations involving tests with high-speed
networks (~ 1 terabit/s), some even involving data transfers from/to
Caltech, CERN and São Paulo State University.

Considering that background we enumerate some of our major values:

Speed focused
-------------

We keep the word performance in mind since the beginning of the development.
The controller should be able to handle large amount of requests on high-speed
networks.

Always updated
--------------
The architecture designed for our project allows for a high level of reuse.
Thus, when a new OpenFlow version is released, the amount of work needed to
implement it is minimized by reusing the parts that did not change between
version.

This means that the first version (1.0.0 = v0x01) was fully coded from the
OpenFlow 1.0.0 Protocol. The 1.1 version (v0x02) imports the 1.0 version and
then do the necessary changes to make it compatible with the OpenFlow 1.1.0
Protocol, and so on.

Easy to learn
-------------
We chose python for its simplicity and code clarity, thus, we try to code in a
"pythonic way". We also try to keep the most complete and didactic API
documentation. Once you get a hold on how the library works, understanding how
the controller works is a trivial task.

Born to be free
---------------
OpenFlow was born with a simple idea: make your network more vendor agnostic
and we like that!

We are advocates and supporters of free software and we believe that the more
eyes reviewing a certain code, the better the code will be. This project can
receive support of many vendors, but will never follow a particular vendor
direction.

We always will keep this code open.

Supported OpenFlow Versions
---------------------------
We have a fully implemented OpenFlow 1.0 and 1.3 APIs and currently we are
working to deliver versions 1.2.

Disclaimer
----------
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE, TITLE AND NON-INFRINGEMENT. IN NO EVENT SHALL
THE COPYRIGHT HOLDERS OR ANYONE DISTRIBUTING THE SOFTWARE BE LIABLE FOR ANY
DAMAGES OR OTHER LIABILITY, WHETHER IN CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

