from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class EncryptionResponse(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'shared_secret': types.VarIntPrefixedByteArray,
		'verify_secret': types.VarIntPrefixedByteArray,
	}

	def __init__(self, context):
		super().__init__(context)
		self.shared_secret = None
		self.verify_secret = None

	def __repr__(self):
		return f"<{self.NAME} shared_secret_lenght={len(self.shared_secret)} verify_secret_lenght={len(self.verify_secret)}>"

	@property
	def ID(self):
		return 0x01