import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class PositionAndLook(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'x': common.types.common.Double,
		'y': common.types.common.Double,
		'z': common.types.common.Double,
		'yaw': common.types.common.Float,
		'pitch': common.types.common.Float,
		'flags': common.types.common.Byte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.x = None
		self.y = None
		self.z = None
		self.yaw = None
		self.pitch = None
		self.flags = None

	@property
	def ID(self):
		return 0x08

