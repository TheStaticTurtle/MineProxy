import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class TimeUpdate(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
		'world_age': common.types.common.Long,
		'time_of_day': common.types.common.Long,
	}

	def __init__(self, context):
		super().__init__(context)
		self.world_age = None
		self.time_of_day = None

	@property
	def ID(self):
		return 0x03

