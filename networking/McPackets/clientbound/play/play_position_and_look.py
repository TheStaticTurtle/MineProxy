from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class PositionAndLook(SimplePacket.Packet):
	ID = 0x08
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'x': types.Double,
		'y': types.Double,
		'z': types.Double,
		'yaw': types.Float,
		'pitch': types.Float,
		'flags': types.Byte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.x = None
		self.y = None
		self.z = None
		self.yaw = None
		self.pitch = None
		self.flags = None
