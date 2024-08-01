from pysnc import ServiceNowClient
from pysnc.auth import ServiceNowPasswordGrantFlow
from functools import lru_cache

import importlib.util,sys
if importlib.util.find_spec('pandas') is not None :
  import pandas as pd


class ServiceNow() :
  def __init__(self,instance:str, auth_parameters:dict = { 'username' : '', 'password' : '', 'client_id' : '', 'secret' : '' }, \
                    extra_instance_parms:dict = { 'proxy' : None, 'verify' : None, 'cert' : None, 'auto_retry' : True} ) : 
    self.__extra_instance_parms = extra_instance_parms
    self.__instance = instance
    self.__auth_parameters = auth_parameters
    self.client = None 
    try :
      self.auth = ServiceNowPasswordGrantFlow(self.__auth_parameters['username'], self.__auth_parameters['password'], self.__auth_parameters['client_id'], self.__auth_parameters['secret'])
      try :
        self.client = ServiceNowClient(self.__instance, self.auth, **self.__extra_instance_parms)
        return(None)
      except Exception as e :
        raise Exception("__servicenow.__init__ client", e)
    except Exception as e :
      raise Exception("__servicenow.__init__ auth", e)

  #####################################################################################################################
  @lru_cache(maxsize=32)
  def get_records(self, table='incident', criteria=[("active", "true")], output_fmt = 'dict') :
    '''
    # output_fmt =  dict, pandas, list, gr
    # to use pandas, pandas have to be installed in the system
    # dict, is actually an ordered dict, which is the same used to create a pandas df

    '''
    ret = None
    try :
      gr = self.client.GlideRecord(table)
      if len(criteria) > 0 :
        for flt in criteria :
          gr.add_query(*flt)
      gr.query()
      if output_fmt == 'pandas' :
        if 'pandas' in sys.modules :
          ret = pd.DataFrame.from_dict(gr.to_pandas())
        else :
          raise(Exception('__servicenow.get_records: Unable to output to pandas without pandas'))
      elif output_fmt == 'list' :
        ret = [ i for i in gr ]
      elif output_fmt == 'dict' :
        ret = gr.to_pandas()
      else: 
        ret = gr
    except Exception as e :
      raise(Exception('__servicenow.get_records: %s'%e))
    return(ret)

  #####################################################################################################################
  def add_record(self, \
                 elements = { 'short_description' : 'test', 'description' : 'test',
                              'priority' : 3, 'impact' : 3,  'urgency' : 2 }, \
                 table='incident' ) :
    ret = None
    try :
      gr = self.client.GlideRecord(table)
      gr.initialize()
      for k,v in elements.items() :
        gr.set_value(k,v)
      gr.insert()
    except Exception as e :
      raise(Exception('__servicenow.add_record: %s'%e))
    return(ret)

  def __exit__(self ,type, value, traceback):
    return(None)

  def __enter__(self) :
    return(self)
