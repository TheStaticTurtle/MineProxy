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

		response = requests.get("https://api.minecraftservices.com/minecraft/profile",
			headers={
				"Authorization": f"{self.mc_token_type} {self.mc_access_token}"
			}
		)
		data = response.json()

		self.profile = Profile()
		self.profile.id = data["id"]
		self.profile.name = data["name"]

# def _make_request(server, endpoint, data):
# 	"""
#     Fires a POST with json-packed data to the given endpoint and returns
#     response.
#     Parameters:
#         endpoint - An `str` object with the endpoint, e.g. "authenticate"
#         data - A `dict` containing the payload data.
#     Returns:
#         A `requests.Request` object.
#     """
# 	req = requests.post(server + "/" + endpoint, data=json.dumps(data),
# 	                    headers=HEADERS)
# 	return req
#
#
# def _raise_from_request(req):
# 	"""
#     Raises an appropriate `YggdrasilError` based on the `status_code` and
#     `json` of a `requests.Request` object.
#     """
# 	if req.status_code == requests.codes['ok']:
# 		return None
#
# 	try:
# 		json_resp = req.json()
#
# 		if "error" not in json_resp and "errorMessage" not in json_resp:
# 			raise YggdrasilError("Malformed error message.")
#
# 		message = "[{status_code}] {error}: '{error_message}'"
# 		message = message.format(status_code=str(req.status_code),
# 		                         error=json_resp["error"],
# 		                         error_message=json_resp["errorMessage"])
# 	except ValueError:
# 		message = "Unknown requests error. Status code: {}"
# 		message.format(str(req.status_code))
#
# 	raise YggdrasilError(message)
