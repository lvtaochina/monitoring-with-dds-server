import xml.etree.ElementTree as ET
import urllib.parse
import urllib.request
from urllib.error import *

def getddsroot(*, url, parm, use, passwd):
        '''
           Return dds data as xml root based on the info given.
           based on 'urllib' module
           url:Standard url provided by DDS server,dds performance url is defaulted.
           pam:Dictionary containing required matrix
           use:auth info (USER) 
           passwd:auth info (password)
        '''
        full_url = url + '?' + urllib.parse.urlencode(parm)

        # create a password manager
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        # Add the username and password. If we knew the realm, we could use it instead of None.
        password_mgr.add_password(None, url, use, passwd)

        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

        # create "opener" (OpenerDirector instance)
        opener = urllib.request.build_opener(handler)

        try:
                # use the opener to fetch a URL
                with opener.open(full_url) as response:
                        return ET.fromstring(response.read().decode(encoding='utf-8'))
                
        except HTTPError:
                print("认证失败")
        except URLError:
                print("无法连接到DDS服务器:检查网络,服务器IP和端口号")
                
        
def getddsrootv2(*, url, parm, use, passwd):
        '''
           Return dds data as xml root based on the info given.
           based on 'requests' module
           url:Standard url provided by DDS server,dds performance url is defaulted.
           pam:Dictionary containing required matrix
           use:auth info (USER) 
           passwd:auth info (password)
        '''
        import requests
        try:
                r = requests.get(url,params=parm,auth=(use,passwd))
                if r.status_code != 401:
                        #print('\n',r.status_code)
                        root = ET.fromstring(r.text)
                else:
                        print('认证失败')
                        root = None
                                        
        except requests.exceptions.RequestException:
                print("无法连接到DDS服务器:检查网络,服务器IP和端口号")
                root = None
        finally:
                return root


def parse_root(r):
        for row in r.iter('row'):
                return row[1].text


def parse_root_with_iter(iter_rng,r):
        rnt_list = []
        for i in iter_rng:
                for row in r.iter('row'):
                        if row[0].text.partition('.')[0] == i:
                                rnt_list.append(row[1].text)
                                break
                else: rnt_list.append('NaN')
        return rnt_list

def average(strs):
        values = [float(i) for i in strs if i!='NaN']
        return str(round(sum(values)/len(values),1))
