#!/usr/bin/env python3


import utils,sys,os, copy, asyncio

def main() :
  try :
    sn_instance = os.getenv('SN_INSTANCE')
    sn_auth_parameters = { 'username'  : os.getenv('SN_USERNAME'), 
                           'password'  : os.getenv('SN_PASSWORD'),
                           'client_id' : os.getenv('SN_CLIENT_ID'),
                           'secret'    : os.getenv('SN_SECRET') }
    sn_target_table = os.getenv('SN_TABLE')

    protect_parameters = {  'url': os.getenv('SP_URL'),
                            'api_base': os.getenv('SP_API_BASE'),
                            'user': os.getenv('SP_USER'),
                            'pw': os.getenv('SP_PW'),
                            'verify_tls': False if 'false' in os.getenv('SP_VERIFY_TLS', 'True').lower() else True }
    default_elements = { 'short_description' : 'test', 'description' : 'test', 'priority' : 3, 'impact' : 3,  'urgency' : 2 }
    events_to_check = []
  except Exception as e :
    raise(Exception('main: Probably missing environment variables: %s'%e))

  # Fetch all events 
  with utils.Protect_OPC(**protect_parameters) as opc :
    for alert in opc.get_list('alerts') :
      print(alert)
      la = copy.deepcopy(default_elements)
      la['short_description'] = f"ALERT {alert['ALERTID']} FROM {alert['SERVER']}"
      la['description'] = str(alert)
      events_to_check.append(la)

    for client in opc.get_list('clients') :
      client_detail = opc.get_detailed_clients(client['NAME'])
      for server, cd in opc.get_detailed_clients(client['NAME']).items() :
        for client, client_data in cd.items() :
          if client_data['atrisk']['AT_RISK'] == 'yes' :
            la = copy.deepcopy(default_elements)
            la['short_description'] = f"Storage Protect client {client_data['atrisk']['NAME']} at risk"
            la['desccription'] = str(client_data)
            events_to_check.append(la)

  with utils.ServiceNow(sn_instance, auth_parameters = sn_auth_parameters ) as SN :
    records = SN.get_records(table=sn_target_table)
    for event in events_to_check :
      if event['short_description'] not in records['short_description'] :
        SN.add_record(elements=event,table=sn_target_table)


  return(os.EX_OK)

async def async_main(interval:int) :
  while True :
    main()
    await asyncio.sleep(interval)

if __name__ == "__main__" :
  loop_interval = int(os.getenv('INTERVAL', '0'))
  if loop_interval == 0 :
    sys.exit(main())
  else :
    loop = asyncio.get_event_loop()
    try:
      asyncio.ensure_future(async_main(loop_interval))
      loop.run_forever()
    except KeyboardInterrupt:
      pass
    finally:
      loop.close()
      sys.exit(os.EX_OK)
