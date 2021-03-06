import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class Start(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Login
	
	@property
	def STRUCTURE(self):
		return {
		'name': common.types.common.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.name = None

	@property
	def ID(self):
		return 0x00