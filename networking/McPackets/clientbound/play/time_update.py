from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class TimeUpdate(SimplePacket.Packet):
	ID = 0x03
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'world_age': types.Long,
		'time_of_day': types.Long,
	}

	def __init__(self, context):
		super().__init__(context)
		self.world_age = None
		self.time_of_day = None
