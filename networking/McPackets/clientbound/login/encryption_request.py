import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class EncryptionRequest(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Login
	
	@property
	def STRUCTURE(self):
		return {
		'server_id': common.types.common.String,
		'public_key': common.types.common.VarIntPrefixedByteArray,
		'verify_secret': common.types.common.VarIntPrefixedByteArray,
	}

	def __init__(self, context):
		super().__init__(context)
		self.server_id = None
		self.public_key = None
		self.verify_secret = None

	@property
	def ID(self):
		return 0x01

	def __repr__(self):
		return f"<{self.NAME} public_key_lenght={len(self.public_key)} verify_secret_lenght={len(self.verify_secret)}>"