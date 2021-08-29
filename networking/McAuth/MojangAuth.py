import logging

import requests

from .SimpleToken import SimpleToken, Profile, AuthException


class YggdrasilError(AuthException):
    pass

class MojangAuthenticationToken(SimpleToken):
    AGENT_NAME = "Minecraft"
    AGENT_VERSION = 1
    AUTH_SERVER = "https://authserver.mojang.com"
    SESSION_SERVER = "https://sessionserver.mojang.com/session/minecraft"
    HEADERS = {
        "content-type": "application/json"
    }


    def __init__(self):
        super().__init__()
        self.username = None
        self.client_token = None

    @property
    def authenticated(self):
        if not self.username:
            return False
        if not self.mc_access_token:
            return False
        if not self.client_token:
            return False
        return True

    def authenticate(self, username, password):
        self.log.info(f"Logging in with email: {username}")
        payload = {
            "agent": {
                "name": self.AGENT_NAME,
                "version": self.AGENT_VERSION
            },
            "username": username,
            "password": password
        }

        req = requests.post(self.AUTH_SERVER + "/authenticate", json=payload, headers=self.HEADERS)
        self._raise_from_request(req)

        json_resp = req.json()
        self.username = username
        self.mc_access_token = json_resp["accessToken"]
        self.client_token = json_resp["clientToken"]

        self.get_profile()
        # self.profile = Profile()
        # self.profile.id = json_resp["selectedProfile"]["id"]
        # self.profile.name = json_resp["selectedProfile"]["name"]

        self.log.info(f"Logged in, username: {self.profile.name}")

    def refresh_access_token(self):
        self.log.info(f"Refreshing token")
        if self.mc_access_token is None:
            raise ValueError("'access_token' not set!'")

        if self.client_token is None:
            raise ValueError("'client_token' is not set!")

        payload = {
            "accessToken": self.mc_access_token,
            "clientToken": self.client_token
        }
        req = requests.post(self.AUTH_SERVER + "/refresh", json=payload, headers=self.HEADERS)
        self._raise_from_request(req)

        json_resp = req.json()

        self.mc_access_token = json_resp["accessToken"]
        self.client_token = json_resp["clientToken"]

        self.get_profile()
        # self.profile = Profile()
        # self.profile.id = json_resp["selectedProfile"]["id"]
        # self.profile.name = json_resp["selectedProfile"]["name"]

        self.log.info(f"Re-Logged in, username: {json_resp['selectedProfile']['name']}")

    def validate_access_token(self):
        if self.mc_access_token is None:
            raise ValueError("'access_token' not set!")

        req = requests.post(self.AUTH_SERVER + "/validate", json={"accessToken": self.mc_access_token}, headers=self.HEADERS)
        self._raise_from_request(req)


    @classmethod
    def sign_out(cls, username, password):
        req = requests.post(cls.AUTH_SERVER + "/signout", json={"username": username, "password": password}, headers=cls.HEADERS)
        cls._raise_from_request(req)

    def invalidate(self):
        payload = {
            "accessToken": self.mc_access_token,
            "clientToken": self.client_token
        }
        req = requests.post(self.AUTH_SERVER + "/invalidate", json=payload, headers=self.HEADERS)
        self._raise_from_request(req)

        if not req.raise_for_status() and not req.text:
            return True
        else:
            raise YggdrasilError("Failed to invalidate tokens.")

    def join_server(self, server_id):
        if not self.authenticated:
            err = "AuthenticationToken hasn't been authenticated yet!"
            raise YggdrasilError(err)

        self.log.info(f"Joining server: {server_id}")

        payload = {
            "accessToken": self.mc_access_token,
            "selectedProfile": self.profile.to_dict(),
            "serverId": server_id
        }
        req = requests.post(self.SESSION_SERVER + "/join", json=payload, headers=self.HEADERS)

        if not req.raise_for_status():
            return True
        else:
            self._raise_from_request(req)

    @classmethod
    def _raise_from_request(cls, req):
        if req.status_code == requests.codes['ok']:
            return None

        try:
            json_resp = req.json()
            if "error" not in json_resp and "errorMessage" not in json_resp:
                raise YggdrasilError("Malformed error message.")

            message = f"[{req.status_code}] {json_resp['error']}: '{json_resp['errorMessage']}'"

        except ValueError:
            message = f"Unknown requests error. Status code: {req.status_code}s"

        raise YggdrasilError(message)