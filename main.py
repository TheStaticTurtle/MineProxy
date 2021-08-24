import sys
import time
from common import authentication
import proxy
import logging
import coloredlogs

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("urllib3").propagate = False
coloredlogs.install(level='DEBUG', stream=sys.stdout, fmt="[%(asctime)s] [%(name)22s] [%(levelname)5s] %(message)s")

log = logging.getLogger("main")
log.info("Hellow world")

auth_token = authentication.AuthenticationToken()
try:
	auth_token.authenticate("tuglersamuel@gmail.com", "TZnkMw8vF1s0B")
except authentication.YggdrasilError as e:
	log.error(f"Error occured while logging in", e)
	sys.exit()

proxy = proxy.MinecraftProxyManager("192.168.1.33", server_port=25565, listen_port=25565, auth_token=auth_token)
# proxy = proxy.MinecraftProxyManager("mc.hypixel.net", server_port=25565, listen_port=25565, auth_token=auth_token)
proxy.start()

while True:
	time.sleep(1)