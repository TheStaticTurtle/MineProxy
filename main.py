import sys
import time
import config

from networking.McAuth.MicrosoftAuth import MicrosoftAuthenticationToken
from networking.McAuth.MojangAuth import MojangAuthenticationToken
from networking.McAuth.SimpleToken import AuthException

import proxy
import logging
import coloredlogs

logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("urllib3").propagate = False
coloredlogs.install(level='DEBUG', stream=sys.stdout, fmt="[%(asctime)s] [%(name)28s] [%(levelname)5s] %(message)s")

log = logging.getLogger("main")
log.info("Hellow world")


auth_token = MicrosoftAuthenticationToken() if config.MINEPROXY_AUTH_USE_MICROSOFT else MojangAuthenticationToken()
try:
	auth_token.authenticate(config.MINEPROXY_AUTH_MINECRAFT_EMAIL, config.MINEPROXY_AUTH_MINECRAFT_PASSWORD)
except AuthException as e:
	log.error(f"Error occurred while logging in: {e}")
	sys.exit()

proxy = proxy.MinecraftProxyManager(
	config.MINEPROXY_PROXY_REMOTE_IP,
	server_port=config.MINEPROXY_PROXY_REMOTE_PORT,
	listen_port=config.MINEPROXY_PROXY_LISTEN_PORT,
	auth_token=auth_token
)
proxy.start()

while True:
	time.sleep(1)
