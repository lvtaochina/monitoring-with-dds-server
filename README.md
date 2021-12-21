# monitoring-with-dds-server.
Tools for accessing performance data using the RMF Distributed Data Server API
[Intro and benifit]
>System performance data gathering &reporting, during or after tests &cutover 
phases in mainframe projects are always scheduled on regular basis.

>Traditional pre-reporting process includes SMF data dump, RMF post processor
and finally data extraction using scripts languages.  

>And clients to whom I am working for, want to incorporate more modern and open
 source tool in data center modernization journey.

>Here, I prepared a demo tool(python only), which sends HTTP requests for selected 
performance data using RMF DDS API been provided by DDS server, traditional z/OS
resources or metrics data(CPU,APPL,STORAGE,DASD,CF) will be persistent in a 
ASCII file for future viewing or processing.

[repository]
https://github.com/lvtaochina/monitoring-with-dds-server

[How to use this tool]
All the steps you need to do can be done in a few steps, I will show you how:
1.Configure and start DDS server on your z/OS system.
- Minimally, a "START GPMSERVE" command is enough.

2.Update "DDS_SERVER_ZOS demo.py", which is the Top-level definition file you 
  need to run later.
  Please see attached imgage for illustration on how to update this file.
  
  Module file "dds.py" ,contains several under-lying functions for TCPIP request
  XML-parsing, and dose some simple math work.
  
3.Optionally, install Python package "requests" if you want to use this popular
  module, or you can choose to use the python built-in "urllib.request" module.
  
4.Run the "DDS_SERVER_ZOS demo.py" to get the data you want.
  Any problems during use, please drop me a mail or call: tao.lv@kyndryl.com
  
[Doc that helps]
- You will find more in "Setting up the Distributed Data Server for z/OS" in - 
  Chapter 2 in <Resource Measurement Facility User's Guide> SC34-2664-30
  
- Chapter 3. Accessing performance data using the RMF Distributed Data Serve
  in "Resource Measurement Facility Programmer's Guide" provides more about the
  API for possilbe z/OS and mainframe resources and metrics.SC34-2667-30
  
  
