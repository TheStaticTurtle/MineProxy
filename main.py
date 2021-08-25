from dotenv import load_dotenv
import sys
import os
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

load_dotenv()

auth_token = authentication.AuthenticationToken()
try:
	auth_token.authenticate(os.getenv("MINEPROXY_AUTH_MINECRAFT_EMAIL"), os.getenv("MINEPROXY_AUTH_MINECRAFT_PASSWORD"))
except authentication.YggdrasilError as e:
	log.error(f"Error occured while logging in", e)
	sys.exit()

proxy = proxy.MinecraftProxyManager(
	os.getenv("MINEPROXY_PROXY_REMOTE_IP"),
	server_port=int(os.getenv("MINEPROXY_PROXY_REMOTE_PORT")),
	listen_port=int(os.getenv("MINEPROXY_PROXY_LISTEN_PORT")),
	auth_token=auth_token
)
proxy.start()

while True:
	time.sleep(1)