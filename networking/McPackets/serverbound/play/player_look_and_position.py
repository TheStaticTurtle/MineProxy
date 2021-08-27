import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class PlayerLookAndPosition(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'x': common.types.common.Double,
		'feet_y': common.types.common.Double,
		'z': common.types.common.Double,
		'yaw': common.types.common.Float,
		'pitch': common.types.common.Float,
		'on_ground': common.types.common.Boolean,
	}

	def __init__(self, context):
		super().__init__(context)
		self.x = None
		self.feet_y = None
		self.z = None
		self.yaw = None
		self.pitch = None
		self.on_ground = None

	@property
	def ID(self):
		return 0x06
