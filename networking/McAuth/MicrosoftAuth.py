import json
import logging
import re
import urllib.parse
import uuid

import requests

from . import MojangAuth
from .SimpleToken import SimpleToken, Profile, AuthException, MinecraftError

class MicrosoftAuthException(AuthException):
	pass

class XboxException(MicrosoftAuthException):
	pass

class AuthenticationException(XboxException):
	pass

class DoesntOwnGameError(MicrosoftAuthException):
	pass




def merge_dict(*kwarg):
	c = {}
	for d in kwarg:
		for key in d.keys():
			c[key] = d[key]
	return c


class MicrosoftAuthenticationToken(SimpleToken):
	CLIENT_ID = "000000004C12AE6F"
	SCOPE = "service::user.auth.xboxlive.com::MBI_SSL"
	RESPONSE_TYPE = "token"
	REDIRECT_URI = "https://login.live.com/oauth20_desktop.srf"
	USER_AGENT = "XboxReplay; XboxLiveAuth/4.0"
	LANGUAGE = "en-US"

	XBLContractVersion = 2
	XBLAdditionalHeaders = {
		"Accept": 'application/json',
		'X-Xbl-Contract-Version': str(XBLContractVersion)
	}

	SESSION_SERVER = "https://sessionserver.mojang.com/session/minecraft"
	SESSION_HEADERS = {
		"content-type": "application/json"
	}

	def __init__(self):
		super().__init__()
		self.session = requests.session()
		self.username = None
		self.device_token = None
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
		return False

	def _get_base_header(self, additional_headers=None):
		if additional_headers is None:
			additional_headers = {}
		base_headers = {
			"Pragma": 'no-cache',
			"Accept": '*/*',
			"User-Agent": self.USER_AGENT,
			"Cache-Control": 'no-store, must-revalidate, no-cache',
			"Accept-Encoding": 'gzip, deflate, compress',
			"Accept-Language": f"{self.LANGUAGE}, {self.LANGUAGE.split('-')[0]};q=0.9",
		}
		return merge_dict(base_headers, additional_headers)

	@staticmethod
	def _get_authorize_url(client_id=CLIENT_ID, scope=SCOPE, response_type=RESPONSE_TYPE, redirect_uri=REDIRECT_URI):
		qs = urllib.parse.unquote(urllib.parse.urlencode({
			'client_id': client_id,
			'redirect_uri': redirect_uri,
			'response_type': response_type,
			'scope': scope,
		}))
		return f"https://login.live.com/oauth20_authorize.srf?{qs}"

	def pre_auth(self):
		self.log.info("Doing Pre-Live-Auth")
		response = self.session.get(
			self._get_authorize_url(),
			headers=self._get_base_header(additional_headers={'Accept-Encoding': 'identity'})
		)
		url_re = b'urlPost:\\\'([A-Za-z0-9:\?_\-\.&/=]+)'
		ppft_re = b'sFTTag:\\\'.*value="(.*)"/>'
		return {
			"urlPost": re.search(url_re, response.content).group(1),
			"PPFT": re.search(ppft_re, response.content).groups(1)[0],
		}

	def live_auth(self, username, password):
		self.log.info(f"Authenticating with user {username}")

		pre_auth_response = self.pre_auth()

		response = self.session.post(
			pre_auth_response["urlPost"],
			headers=self._get_base_header(additional_headers={'Accept-Encoding': 'identity',
			                                                  'Content-Type': 'application/x-www-form-urlencoded'}),
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

	def _exchange_rps_ticket_for_user_token(self, rpsTicket: str, preamble: str = "t", additional_headers={}):
		self.log.info("Exchanging rps ticket")
		if not rpsTicket.startswith("d=") or not rpsTicket.startswith("t="):
			rpsTicket = f"{preamble}=" + rpsTicket

		response = requests.post(
			"https://user.auth.xboxlive.com/user/authenticate",
			headers=self._get_base_header(additional_headers=merge_dict(additional_headers, self.XBLAdditionalHeaders)),
			json={
				"RelyingParty": 'http://auth.xboxlive.com',
				"TokenType": 'JWT',
				"Properties": {
					"AuthMethod": 'RPS',
					"SiteName": 'user.auth.xboxlive.com',
					"RpsTicket": rpsTicket
				}
			}
		)

		return response.json()

	def _exchange_tokens_for_XSTS_token(self, tokens, XSTS_relying_party=None, sandbox_id="RETAIL", additional_headers={}):
		self.log.info("Exchanging tokens for XSTS token")
		if XSTS_relying_party is None:
			XSTS_relying_party = "http://xboxlive.com"
		response = requests.post(
			"https://xsts.auth.xboxlive.com/xsts/authorize",
			headers=self._get_base_header(additional_headers=merge_dict(additional_headers, self.XBLAdditionalHeaders)),
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
			XSTS_relying_party="rp://api.minecraftservices.com/"
		)

		return {
			"XSTS": response["Token"],
			"userhash": response["DisplayClaims"]["xui"][0]["uhs"]
		}

	def authenticate_mc(self, user_hash, xsts_token):
		self.log.info("Doing minecraft authentication")
		response = requests.post(
			"https://api.minecraftservices.com/authentication/login_with_xbox",
			json={
				"identityToken": f"XBL3.0 x={user_hash};{xsts_token}>",
			}
		)
		return response.json()

	def _raise_if_doesnt_own_game(self):
		url = "https://api.minecraftservices.com/entitlements/mcstore"
		response = requests.get(url,
			headers={
				"Authorization": f"{self.mc_token_type} {self.mc_access_token}"
			}
		)
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
			MojangAuth.MojangAuthenticationToken._raise_from_request(req)