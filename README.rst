simdeplower is a python tool that you can use to deploy vCenter Server Appliances and have them
magically configured in simulator mode (or how ever you see fit using a shell script).

Getting Started
===============
simdeplower has been tested extensively on OSX, but should work anywhere that subprocess32 and paramiko will run.
simdeplower requires either VMWare Workstation or Fusion to be successful. From those products simdeplower will use
vmrun and ovftool. simdeplower uses ovftool to deploy (extract) an ova onto the filesystem then uses vmrun to launch
the extracted VMX. Once the VM is up and running simdeplower uses paramiko to ssh in using the default username and
password of "root" and "vmware" and executes a shell script you provide, or a bundled script that will configure the
appliance as a simulator. This only works on VCSA 5.x products because simulator no longer works on 6.x


Installing
==========
To install it is best to create a new virtualenv and install using pip
For detailed instructions see the `wiki <https://github.com/virtdevninja/simdeplower/wiki>`_ on GitHub


Contributing
============
To contribute to simdeplower please follow the fork, branch, pull request work flow. Tests are required where applicable. 
All code should follow pep8 standards, and must support python 2.7 When opening a pull request please 
do so against the development branch.


Python Support
==============
* simdeplower 0.1 and later support Python 2.7


Reporting Issues
================
To report a problem with simdeplower or to make a feature request open an 
`issue <https://github.com/virtdevninja/simdeplower/issues>`_ on GitHub.


Usage Examples
==============
See the `wiki <https://github.com/virtdevninja/simdeplower/wiki>`_ on GitHub


Releases
========
* simdeplower 0.1


.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/virtdevninja/simdeplower
   :target: https://gitter.im/virtdevninja/simdeplower?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge