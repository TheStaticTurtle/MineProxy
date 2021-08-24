from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class EncryptionRequest(SimplePacket.Packet):
	ID = 0x01
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'server_id': types.String,
		'public_key': types.VarIntPrefixedByteArray,
		'verify_secret': types.VarIntPrefixedByteArray,
	}

	def __init__(self, context):
		super().__init__(context)
		self.server_id = None
		self.public_key = None
		self.verify_secret = None

	def __repr__(self):
		return f"<{self.NAME} public_key_lenght={len(self.public_key)} verify_secret_lenght={len(self.verify_secret)}>"