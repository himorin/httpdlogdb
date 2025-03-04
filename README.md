# httpdlogdb - DB system for httpd log analysis and display

This is a simple script to 
1) analyse httpd log files as daily batch and push into database, 
2) display via web interface as summary.

## System overview

This system is consisted of two modules and database.

- log file analysis tool, and push results into DB (used as daily batch)
- web based display tool, just read from database

Database stores raw lines and daily summary count data, on 
1) page view, 
2) count on page and referrer pair, 
3) count on page and browser ID pair.

## DB design

See [dbdef.sql](dbdef.sql) for SQL.

To save size, all string based values are stored by reference ID, 
for all of accessed page, referrer, and browser ID.

