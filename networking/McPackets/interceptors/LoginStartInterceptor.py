from common.authentication import Profile
from common.context import Context
from ..serverbound import login
from ..SimplePacketInterceptor import SimplePacketInterceptor

class LoginStartInterceptor(SimplePacketInterceptor):
	NAME = "LoginStartInterceptor"
	packet_class = login.Start

	def __init__(self, context: Context, profile: Profile):
		super().__init__(context)
		self.profile = profile

	def _intercept(self, packet: login.Start):
		self.log.info(f"Intercepted {packet}, spoofing original name to: {self.profile.name}")
		packet.name = self.profile.name

		return packet