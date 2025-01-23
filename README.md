# Python Tools Pack

## Requirements
1. Install Python 3.12+
2. Install pipenv
`pip install pipenv`
3. Run shell
`pipenv shell`
4. Install all requirements libraries (in shell)
`pip install`

## Tools
`1_logfiles_parser.py`

Script for parsing text log files  
Usage: `1_logfiles_parser.py [-h] file [file ...]`  
Log format: `start_time | end_time | req_path | resp_code | resp_body`

Example log data in /demo dir

`2_rmpath_tool.py`

Script for recursive delete specified path   
Usage: `2_rmpath_tool.py [-h] path`

`3_make_wgconf.py`

Script for download and set 'AllowedIPs' option in Wireguard config  
List IPs download from https://stat.ripe.net/ by specified country code  
Usage: `3_make_wgconf.py <country code (ie. RU)> <WG config file (*.conf)>`