import logging
import requests


class AuthException(Exception):
	pass

class MinecraftError(Exception):
	pass


class Profile(object):
	def __init__(self):
		self.id = None
		self.name = None

	def to_dict(self):
		if self:
			return {"id": self.id, "name": self.name}
		else:
			raise AttributeError("Profile is not yet populated.")

	def __bool__(self):
		bool_state = self.id is not None and self.name is not None
		return bool_state


class SimpleToken(object):
	AGENT_NAME = "MineProxy"

	def __init__(self):
		self.log = logging.getLogger(f"{self.__class__.__name__}")
		self.log.info("Hellow world")
		self.profile = Profile()
		self.mc_token_type = "Bearer"
		self.mc_access_token = None

	@property
	def authenticated(self):
		return False

	def authenticate(self, username, password):
		raise NotImplementedError("Authenticate is not implemented")

	def refresh_access_token(self):
		raise NotImplementedError("Refresh is not implemented")

	def validate_access_token(self):
		raise NotImplementedError("Validate is not implemented")

	@classmethod
	def sign_out(cls, username, password):
		raise NotImplementedError("Sign-Out is not implemented")

	def invalidate(self):
		raise NotImplementedError("Invalidate is not implemented")

	def join_server(self, server_id):
		raise NotImplementedError("Join server is not implemented")

	def get_profile(self):
		self.log.info("Loading profile")

		response = requests.get("https://api.minecraftservices.com/minecraft/profile", headers={"Authorization": f"{self.mc_token_type} {self.mc_access_token}"})
		data = response.json()

		self.profile = Profile()
		self.profile.id = data["id"]
		self.profile.name = data["name"]
