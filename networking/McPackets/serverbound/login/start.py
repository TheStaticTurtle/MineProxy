from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Start(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'name': types.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.name = None

	@property
	def ID(self):
		return 0x00