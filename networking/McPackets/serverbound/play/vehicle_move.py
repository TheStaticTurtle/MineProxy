import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class VehicleMove(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'x': common.types.common.Double,
			'y': common.types.common.Double,
			'z': common.types.common.Double,
			'yaw': common.types.common.Float,
			'pitch': common.types.common.Float,
		}

	def __init__(self, context):
		super().__init__(context)
		self.x = None
		self.y = None
		self.z = None
		self.yaw = None
		self.pitch = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x10
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
