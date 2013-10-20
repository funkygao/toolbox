=========================
AWS
=========================

:Author: Gao Peng <funky.gao@gmail.com>
:Description: NA
:Revision: $Id$

.. contents:: Table Of Contents
.. section-numbering::

Background
==========

Active since July 2002, amazon offer computing and storage cloud solutions.

AWS accounts for 3.1% of total http/https traffic, i,e., 1/5 of google.


Customers
=========

- Dropbox

- Zynga

- Netflix

- FourSquare

EC2
===

EC2 instances can be allocated on seven datacenters (called also Availability Zones by AWS) world-widely distributed.

No automatic tool for migration of instances among different Availability Zones has been implemented yet.

AWS follow a strict naming rule for EC2: 

::

    the instance IP address a.b.c.d is registered with a Type-A DNS record as ec2-a-b-c-d.XXXXX.amazonaws.com, where XXXXX is a variable string. 
    A simple DNS reverse lookup from the IP address allows to discover that a.b.c.d hosts an EC2 instance

S3
==

Offers storage services through standard interfaces (REST, SOAP, and BitTorrent).

Data are stored by means of “objects” whose size can span from 1B to 5TB each. 

S3 is reported to store more than a trillion objects as of June 20122. 

EC2 and S3 are co-located in each Availability Zone.

CloudFront
==========

CloudFront can deliver dynamic, static as well as streaming content.

VPC
===

Virtual Private Cloud
