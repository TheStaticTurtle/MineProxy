import re
import urllib.parse
from abc import ABC

import requests

from . import MojangAuth
from .SimpleToken import SimpleToken, AuthException, MinecraftError

class MicrosoftAuthException(AuthException):
	pass

class XboxException(MicrosoftAuthException):
	pass

class AuthenticationException(MicrosoftAuthException):
	pass

class DoesntOwnGameError(MicrosoftAuthException):
	pass



def merge_dict(*kwarg):
	c = {}
	for d in kwarg:
		for key in d.keys():
			c[key] = d[key]
	return c


class MicrosoftAuthenticationToken(SimpleToken, ABC):
	USER_AGENT = "XboxReplay; XboxLiveAuth/4.0"
	LANGUAGE = "en-US"
	BASE_HEADERS = {
		"Pragma": 'no-cache',
		"Accept": '*/*',
		"User-Agent": USER_AGENT,
		"Cache-Control": 'no-store, must-revalidate, no-cache',
		"Accept-Encoding": 'gzip, deflate, compress',
		"Accept-Language": f"{LANGUAGE}, {LANGUAGE.split('-')[0]};q=0.9",
	}
	LIVE_OAUTH_AUTHORIZE_URL = "https://login.live.com/oauth20_authorize.srf"
	LIVE_CLIENT_ID = "000000004C12AE6F"
	LIVE_SCOPE = "service::user.auth.xboxlive.com::MBI_SSL"
	LIVE_RESPONSE_TYPE = "token"
	LIVE_REDIRECT_URI = "https://login.live.com/oauth20_desktop.srf"

	PRE_AUTH_URL_RE = b'urlPost:\\\'([A-Za-z0-9:\?_\-\.&/=]+)'
	PRE_AUTH_PPFT_RE = b'sFTTag:\\\'.*value="(.*)"/>'

	XBL_AUTHENTICATE_URL = "https://user.auth.xboxlive.com/user/authenticate"
	XBL_RELAYING_PARTY = 'http://auth.xboxlive.com'

	MINECRAFT_RELAYING_PARTY = "rp://api.minecraftservices.com/"
	DEFAULT_XSTS_RLEAYING_PARTY = "http://xboxlive.com"
	DEFAULT_XSTS_SANDBOX_ID = "RETAIL"

	XSTS_AUTHORIZE_URL = "https://xsts.auth.xboxlive.com/xsts/authorize"

	XBL_CONTRACT_VERSION = 2
	XBL_HEADERS = {
		"Accept": 'application/json',
		'X-Xbl-Contract-Version': str(XBL_CONTRACT_VERSION)
	}

	MINECRAFT_XBOX_STORE_CHECK_URL = "https://api.minecraftservices.com/entitlements/mcstore"
	MINECRAFT_XBOX_AUTH_URL = "https://api.minecraftservices.com/authentication/login_with_xbox"

	SESSION_SERVER = "https://sessionserver.mojang.com/session/minecraft"
	SESSION_HEADERS = {
		"content-type": "application/json"
	}

	def __init__(self):
		super().__init__()
		self.session = requests.session()
		self.xbox_token_type = "bearer"
		self.xbox_access_token = None
		self.xbox_refresh_token = None
		self.xbox_token_expires_in = None
		self.xbox_token_scope = None
		self.xbox_user_id = None

		self.mc_username = None
		self.mc_expires_in = None

	@property
	def authenticated(self):
		if not self.mc_access_token:
			return False
		return True

	def _get_base_header(self, additional_headers=None):
		if additional_headers is None:
			additional_headers = {}
		return merge_dict(self.BASE_HEADERS, additional_headers)

	@classmethod
	def _get_authorize_url(cls, client_id=LIVE_CLIENT_ID, scope=LIVE_SCOPE, response_type=LIVE_RESPONSE_TYPE, redirect_uri=LIVE_REDIRECT_URI):
		qs = urllib.parse.unquote(urllib.parse.urlencode({
			'client_id': client_id,
			'redirect_uri': redirect_uri,
			'response_type': response_type,
			'scope': scope,
		}))
		return f"{cls.LIVE_OAUTH_AUTHORIZE_URL}?{qs}"

	def pre_auth(self):
		self.log.info("Doing Pre-Live-Auth")
		response = self.session.get(
			self._get_authorize_url(),
			headers=self._get_base_header(additional_headers={'Accept-Encoding': 'identity'})
		)
		return {
			"urlPost": re.search(self.PRE_AUTH_URL_RE, response.content).group(1),
			"PPFT": re.search(self.PRE_AUTH_PPFT_RE, response.content).group(1),
		}

	def live_auth(self, username, password):
		self.log.info(f"Authenticating with user {username}")

		pre_auth_response = self.pre_auth()

		response = self.session.post(
			pre_auth_response["urlPost"],
			headers=self._get_base_header(additional_headers={'Accept-Encoding': 'identity', 'Content-Type': 'application/x-www-form-urlencoded'}),
			data={
				"login": username,
				"loginfmt": username,
				"passwd": password,
				"PPFT": pre_auth_response["PPFT"]
			},
			allow_redirects=False,
		)

		if response.status_code != 302:
			self.log.error(f"Invalid credentials or 2FA enabled")
			raise AuthenticationException("Invalid credentials or 2FA enabled")

		if 'Location' not in response.headers:
			self.log.error(f"Missing Location header")
			raise AuthenticationException("Could not log in with supplied credentials (Missing Location header)")

		parsed = urllib.parse.urlparse(response.headers['Location'])
		fragment = urllib.parse.parse_qs(parsed.fragment)

		out = {}
		for key in fragment.keys():
			out[key] = fragment[key][0]

		return out

	def _exchange_rps_ticket_for_user_token(self, rpsTicket: str, preamble: str = "t", additional_headers=None):
		if additional_headers is None:
			additional_headers = {}
		self.log.info("Exchanging rps ticket")
		if not rpsTicket.startswith("d=") or not rpsTicket.startswith("t="):
			rpsTicket = f"{preamble}=" + rpsTicket

		response = requests.post(
			self.XBL_AUTHENTICATE_URL,
			headers=self._get_base_header(additional_headers=merge_dict(additional_headers, self.XBL_HEADERS)),
			json={
				"RelyingParty": self.XBL_RELAYING_PARTY,
				"TokenType": 'JWT',
				"Properties": {
					"AuthMethod": 'RPS',
					"SiteName": 'user.auth.xboxlive.com',
					"RpsTicket": rpsTicket
				}
			}
		)

		return response.json()

	def _exchange_tokens_for_XSTS_token(self, tokens, XSTS_relying_party=DEFAULT_XSTS_RLEAYING_PARTY, sandbox_id=DEFAULT_XSTS_SANDBOX_ID, additional_headers=None):
		if additional_headers is None:
			additional_headers = {}
		self.log.info("Exchanging tokens for XSTS token")
		response = requests.post(
			self.XSTS_AUTHORIZE_URL,
			headers=self._get_base_header(additional_headers=merge_dict(additional_headers, self.XBL_HEADERS)),
			json={
				"RelyingParty": XSTS_relying_party,
				"TokenType": 'JWT',
				"Properties": {
					"UserTokens": tokens["userTokens"],
					"SandboxId": sandbox_id
				}
			}
		)
		if response.status_code == 401:
			data = response.json()
			if data["XErr"] == 2148916233:
				raise AuthenticationException("The account doesn't have an Xbox account.")
			if data["XErr"] == 2148916235:
				raise AuthenticationException("The account is from a country where Xbox Live is not available/banned")
			if data["XErr"] == 2148916238:
				raise AuthenticationException("The account is a child (under 18) and cannot proceed unless the account is added to a Family by an adult.")
		return response.json()

	def post_live_auth(self, preamble: str = "t"):
		self.log.info("Doing Post-Live-Auth")
		user_token_response = self._exchange_rps_ticket_for_user_token(self.xbox_access_token, preamble=preamble)

		response = self._exchange_tokens_for_XSTS_token({
				"userTokens": [user_token_response["Token"]],
			},
			XSTS_relying_party=self.MINECRAFT_RELAYING_PARTY
		)

		return {
			"XSTS": response["Token"],
			"userhash": response["DisplayClaims"]["xui"][0]["uhs"]
		}

	def authenticate_mc(self, user_hash, xsts_token):
		self.log.info("Doing minecraft authentication")
		response = requests.post(
			self.MINECRAFT_XBOX_AUTH_URL,
			json={
				"identityToken": f"XBL3.0 x={user_hash};{xsts_token}>",
			}
		)
		return response.json()

	def _raise_if_doesnt_own_game(self):
		response = requests.get(self.MINECRAFT_XBOX_STORE_CHECK_URL, headers={"Authorization": f"{self.mc_token_type} {self.mc_access_token}"})
		if len(response.json()["items"]) == 0:
			raise DoesntOwnGameError("User doesn't own Minecraft")

	def authenticate(self, username, password):
		self.session = requests.Session()
		tokens = self.live_auth(username, password)

		self.xbox_access_token = tokens['access_token']
		self.xbox_refresh_token = tokens['refresh_token']
		self.xbox_token_expires_in = tokens['expires_in']
		self.xbox_token_scope = tokens['scope']
		self.xbox_user_id = tokens['user_id']

		more_tokens = self.post_live_auth()

		mc_tokens = self.authenticate_mc(more_tokens["userhash"], more_tokens["XSTS"])

		self.mc_token_type = mc_tokens["token_type"]
		self.mc_access_token = mc_tokens["access_token"]
		self.mc_username = mc_tokens["username"]
		self.mc_expires_in = mc_tokens["expires_in"]

		self._raise_if_doesnt_own_game()

		self.get_profile()

	def join_server(self, server_id):
		if not self.authenticated:
			raise MinecraftError("AuthenticationToken hasn't been authenticated yet!")

		self.log.info(f"Joining server: {server_id}")

		payload = {
			"accessToken": self.mc_access_token,
			"selectedProfile": self.profile.to_dict(),
			"serverId": server_id
		}
		req = requests.post(self.SESSION_SERVER + "/join", json=payload, headers=self.SESSION_HEADERS)

		if not req.raise_for_status():
			return True
		else:
			MojangAuth.MojangAuthenticationToken.raise_from_request(req)
