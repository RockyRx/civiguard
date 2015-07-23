## Civiguard
Simple web application for [Civiguard Inc](https://code.google.com/p/modwsgi) to collect user data

### Prerequisites
- Django 2.6 
- Python 2.6-2.7
- Apache [Cassandra 0.6](http://archive.apache.org/dist/cassandra/0.6.0/)
- Apache server with [modwsgi](https://code.google.com/p/modwsgi/)
- Nginx for serving static media

### Notes
This is bit an old project and will need some considerable amout of time if you are going to set this up. I have 
used Nginx to serve static media using its ```proxy_pass``` feature. Please look into this [question](http://stackoverflow.com/questions/869001/how-to-serve-all-existing-static-files-directly-with-nginx-but-proxy-to-apache) on Stackoverflow if you
do not have prior experience with this approch.
