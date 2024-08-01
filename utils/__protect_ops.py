import requests, xml.etree.ElementTree as ET
from functools import lru_cache

'''
API Reference: https://www.ibm.com/support/pages/ibm-spectrum-protect-operations-center-v810-rest-api-commands
'''

class Protect_OPC():
  def __init__(self, url:str = "", api_base:str = "", user:str = '', pw:str = '', verify_tls:bool = True) :
    self.__url = url 
    self.__user = user
    self.__pw = pw
    self.__verify_tls = verify_tls
    self.__api_base = f"{self.__url}{api_base}"

    self.__custom_headers = {
      "OC-API-Version" : "1.0",
      "Content-Type" : "application/json"
    }
    if self.__verify_tls is False :
      import urllib3
      urllib3.disable_warnings()

    self.__requests_parms = { 'headers' : self.__custom_headers, 'auth' : (self.__user,self.__pw) , 'verify' : self.__verify_tls }

    self.__keys = { 'servers'        : [ "/servers", 'server' ],
                    'alerts'         : [ "/alerts",  'alert' ],
                    'clients'        : [ "/clients", 'client' ],
                    'storagepools'   : [ "/storagepools", 'storagepool' ],
                    'storagedevices' : [ "/storagedevices", 'storagedevice' ]
                  }

    return(None)

  #####################################################################################################################
  @lru_cache(maxsize=128)
  def __get_key(self,dst_url,key_to_find) :
    tree = None 
    ret = []
    resp = requests.get(dst_url, **self.__requests_parms)
    if resp.ok is True :
      tree = ET.fromstring(resp.text)
      for key in tree.iter(tag=key_to_find) :
        ret.append({ elm : key.get(elm) for elm in key.keys() })
    return(ret)

  #####################################################################################################################
  def get_list(self, key:str) :
    '''
    For available keys, check var __keys
    '''
    try :
      return(self.__get_key(f"{self.__api_base}{self.__keys[key][0]}",self.__keys[key][1]))
    except Exception as e :
      raise Exception('Protect_OPC.get_list', e)

  #####################################################################################################################
  def get_detailed_clients(self, details:bool = True, atrisk:bool = True, filespaces:bool = True) :
    '''
    Changing any element from True to false, just prevents aditional API calls, by setting that specific key to None
    '''
    try :
      ret = {}
      for lst in [ ( a['SERVER'], a['NAME'] ) for a in self.get_list('clients') ] :
        url_base = f"{self.__api_base}/servers/{lst[0]}/clients/{lst[1]}"
        dt = {}
        dt['details']    = self.__get_key(f"{url_base}/details",'clientdetail')[0] if details is True else None
        dt['atrisk']     = self.__get_key(f"{url_base}/atrisk",'clientatrisk')[1]  if atrisk is True else None
        dt['filespaces'] = self.__get_key(f"{url_base}/filespaces",'filespace')    if filespaces is True else None

        try :
          ret[lst[0]][lst[1]] = dt
        except :
          ret[lst[0]] = { lst[1] : dt }
      return(ret)
    except Exception as e :
      raise Exception('Protect_OPC.get_detailed_clients', e)
          
  def __exit__(self ,type, value, traceback):
    return(None)

  def __enter__(self) :
    return(self)
