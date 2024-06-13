import asyncio
from configset import configset
from pathlib import Path
import psutil
import os
import sys
import time
from xnotify import notify
from pydebugger.debug import debug
from datetime import datetime
from make_colors import make_colors
import subprocess


CONFIGNAME = str(Path(__file__).parent / 'servicemon.ini')
CONFIG = configset(CONFIGNAME)

async def monitor():
	for i in CONFIG.get_config_as_list('service', 'names'):
		service, status = i.split("#")
		try:
			a = psutil.win_service_get(service)
			debug(a_status = a.status())
			debug(status_lower = status.lower())
			debug(service_name = service)
			if not status.lower() in a.status().lower():
				notify.send("Servicemon", "stop", "ServiceMon", f"Stopping servive {service}", 
				['stop'], icon = r"c:\SDK\anaconda3\Lib\site-packages\sendgrowl\sendgrowl.py")
				
				print(
					make_colors(datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S,%f'), 'lc') + " - " +\
					make_colors("stop service", 'ly') + " '" + make_colors(service, 'lw', 'r') + "'"
				)
				
				#cmd = f'sc stop "{service}"'
				
				error_file = str(Path(__file__).parent / 'servicemon_error.log')
				gener_file = str(Path(__file__).parent / 'servicemon_general.log')
				
				if not os.path.isfile(error_file): open(error_file, 'w').close()
				if not os.path.isfile(gener_file): open(gener_file, 'w').close()
				
				#os.system(cmd)
				cmd = ['sc', 'stop', service]
				with open(gener_file, 'a') as outfile, open(error_file, 'a') as errfile:
					process = subprocess.Popen(cmd, stdout=outfile, stderr=errfile)
					process.wait()
				
		except Exception as e:
			print("ERROR [1]:", e)

if __name__ == '__main__':
	e = asyncio.get_event_loop()
	try:
		while 1:
			e.run_until_complete(monitor())
			time.sleep(CONFIG.get_config('time', 'sleep', '5'))
	except KeyboardInterrupt:
		sys.exit()
	except Exception as e:
		print("ERROR [2]:", e)


