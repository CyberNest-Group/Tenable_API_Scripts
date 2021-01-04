    ### Written by Andrew Shuman
    ### Feb 05, 2020
     
    import requests
    import json
    import datetime
    import subprocess
    import base64
    ### Only add this for self-signed certs to disable warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
     
    ### TODO Add Config file for this.
     
    param = {
     
                "username" : "sc username",
     
                "password" : "sc password",
     
                "releaseSession" : "false"
     
    }
    ### SC URL
     
    url = 'https://sc url/rest/'
     
    ### Get the API Token
     
    def getToken():
        r = requests.post(url + 'token', params=param, verify=False)
        token = str(r.json()['response']['token'])
        cookie = r.cookies
        return token, cookie
     
    ### Get the config settings from Tenable.SC
     
    def getConfig():
        token, cookie = getToken()    
        header = {"X-SecurityCenter" : str(token), "Content-Type" : "application/json"}
        r = requests.get(url + 'configSection/0', headers=header, cookies=cookie, verify=False)
        json_data = json.loads(r.content)
        response = json_data['response']
        config = response['LicenseConfig']
        expiration = config['expiration']
        return expiration
     
    ### Get the expiration date of the license
     
    def getExpiration():
        expiration = getConfig()
        posix_time = int(expiration)
        date = datetime.datetime.utcfromtimestamp(posix_time)
        return date
     
    ### Calculate number of days before license expiration
     
    def Days():
        from datetime import date
        d0 = getExpiration()
        d1 = datetime.datetime.today()
        delta = d0 - d1
        print(delta)
        return delta
        
    Days()
