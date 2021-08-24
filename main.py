import sys
import time
from common import authentication
import proxy


if __name__ == "__main__":

	auth_token = authentication.AuthenticationToken()
	try:
		auth_token.authenticate("tuglersamuel@gmail.com", "TZnkMw8vF1s0B")
	except authentication.YggdrasilError as e:
		print(e)
		sys.exit()

	print(f"Logged in as {auth_token.username} ({auth_token.profile.name})")

	proxy = proxy.MinecraftProxyManager("192.168.1.33", server_port=25565, listen_port=25565, auth_token=auth_token)
	# proxy = proxy.MinecraftProxyManager("mc.hypixel.net", server_port=25565, listen_port=25565, auth_token=auth_token)
	proxy.start()

	while True:
		time.sleep(1)