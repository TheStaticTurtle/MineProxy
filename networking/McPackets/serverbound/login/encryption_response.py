from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class EncryptionResponse(SimplePacket.Packet):
	ID = 0x01
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'shared_secret': types.VarIntPrefixedByteArray,
		'verify_secret': types.VarIntPrefixedByteArray,
	}

	def __init__(self):
		super().__init__()
		self.shared_secret = None
		self.verify_secret = None

	def __repr__(self):
		return f"<{self.NAME} shared_secret_lenght={len(self.shared_secret)} verify_secret_lenght={len(self.verify_secret)}>"