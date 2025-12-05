# okta-sprayer
python3 script that reads usernames from an input file and a password from the command line and then attemps that password for each user against the specified domain's okta page.

First: pip3 install requests

Use: python3 okta-sprayer.py -f [input_file] -d [domain.com] - [wait_time_in_seconds]....then enter the password to use for the spray next

# This fork infomation
This version forked from https://github.com/cedowens/okta-sprayer. it was inhanced to:
* Randomize user-agents 
* Randomize the waiting time to be just a randome to avoid detections.

It is suitable to work with IP rutation tools like AUT now.

