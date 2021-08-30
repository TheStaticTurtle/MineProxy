import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class EntityLookAndRelativeMove(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'delta_x': common.types.common.Short if self.context.protocol_version >= 107 else common.types.complex.FixedPointByte,
			'delta_y': common.types.common.Short if self.context.protocol_version >= 107 else common.types.complex.FixedPointByte,
			'delta_z': common.types.common.Short if self.context.protocol_version >= 107 else common.types.complex.FixedPointByte,
			'yaw': common.types.complex.Angle,
			'pitch': common.types.complex.Angle,
			'on_ground': common.types.common.Boolean,
		}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.delta_x = None
		self.delta_y = None
		self.delta_z = None
		self.yaw = None
		self.pitch = None
		self.on_ground = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x26
		if self.context.protocol_version == 47:
			return 0x17
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
