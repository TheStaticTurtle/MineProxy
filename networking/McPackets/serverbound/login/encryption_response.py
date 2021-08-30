import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class EncryptionResponse(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Login
	
	@property
	def STRUCTURE(self):
		return {
		'shared_secret': common.types.common.VarIntPrefixedByteArray,
		'verify_secret': common.types.common.VarIntPrefixedByteArray,
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