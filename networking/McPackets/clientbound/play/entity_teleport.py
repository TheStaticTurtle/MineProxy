import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class EntityTeleport(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'x': common.types.common.Double if self.context.protocol_version >= 107 else common.types.complex.FixedPointInteger5B,
			'y': common.types.common.Double if self.context.protocol_version >= 107 else common.types.complex.FixedPointInteger5B,
			'z': common.types.common.Double if self.context.protocol_version >= 107 else common.types.complex.FixedPointInteger5B,
			'yaw': common.types.complex.Angle,
			'pitch': common.types.complex.Angle,
			'on_ground': common.types.common.Boolean,
		}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.x = None
		self.y = None
		self.z = None
		self.yaw = None
		self.pitch = None
		self.on_ground = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x4A
		if self.context.protocol_version == 47:
			return 0x18
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")