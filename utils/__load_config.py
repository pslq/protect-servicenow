import configparser, os.path, shutil, logging, importlib.util

def get_config(config_file:str) :
  search_path = [ '/etc', '/opt/freeware/etc', os.getenv('HOME') ]
  config_path = ''

  if importlib.util.find_spec('xdg.BaseDirectory') :
    import xdg.BaseDirectory
    search_path.insert(0,xdg.BaseDirectory.xdg_config_home)
  elif importlib.util.find_spec('xdg') :
    import xdg
    try :
      search_path.insert(0,str(xdg.XDG_CONFIG_HOME))
    except :
      pass

  for ph in search_path :
    full_path = os.path.join(ph,config_file)
    if os.path.exists(full_path) :
      config_path = full_path
      break

  if not config_path :
    new_config_path = os.path.join(search_path[0],default_config_file)
    template_file = os.path.join(os.path.dirname(importlib.util.find_spec('pq_checklist').origin),'pq_checklist.conf.template')
    try :
      shutil.copy(template_file,new_config_path)
      config_path = new_config_path
      debug_post_msg(None, 'Configuration not found at %s, writting new one at %s'%(' '.join(search_path), new_config_path), screen_only=True, flush=True)
    except Exception as e :
      raise SystemError(e)

  config = configparser.ConfigParser()
  if not config_path :
      raise SystemError('No config file could be either located or created, need at least be able to write a new one at %s'%search_path[0])
  else :
    config.read(config_path)

    # Logging configuration
    log_level = logging.INFO
    if config['LOG']['log_level'] == "DEBUG" :
      log_level = logging.DEBUG
    log_file = None
    to_dev_log = True
    if len(config['LOG']['log_file']) > 0 :
      log_file = config['LOG']['log_file']
      to_dev_log = False
    logger = pq_logger(log_level = log_level, stdout = False, name = 'pq_checklist', to_dev_log = to_dev_log, dst_file = log_file)

    if log_start :
      debug_post_msg(logger, 'Using config file: %s'%config_path, screen_only=True, flush=True)

  return(config,logger)
