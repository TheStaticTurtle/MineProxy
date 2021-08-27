import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class PlayerLook(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'yaw': common.types.common.Float,
		'pitch': common.types.common.Float,
		'on_ground': common.types.common.Boolean,
	}

	def __init__(self, context):
		super().__init__(context)
		self.yaw = None
		self.pitch = None
		self.on_ground = None

	@property
	def ID(self):
		return 0x05
