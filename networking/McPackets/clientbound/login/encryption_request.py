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

	def __init__(self):
		super().__init__()
		self.server_id = None
		self.public_key = None
		self.verify_secret = None
