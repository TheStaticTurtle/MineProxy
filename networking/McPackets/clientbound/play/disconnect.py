import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class Disconnect(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'reason': common.types.common.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.reason = None

	@property
	def ID(self):
		return 0x40
