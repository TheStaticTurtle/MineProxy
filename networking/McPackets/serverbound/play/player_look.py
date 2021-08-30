import common.types.common
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class PlayerLook(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
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
		if self.context.protocol_version >= 107:
			return 0x0E
		if self.context.protocol_version == 47:
			return 0x05
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
