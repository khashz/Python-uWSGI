# Python-uWSGI

This python uWSGI template provides a logger which prints to a file called server_logs.log in the current directory.

It utilizes a singleton handler class to respond to API calls.

The server creates request ids and keeps track of latency for each API call.

Features an ini file configured to allow for graceful shutdowns. I was not able to get graceful shutdowns to work with the uWSGI master enabled (even though this is recommended).

You do not need to launch this with root.

To start,
 # uwsgi uwsgi.ini
