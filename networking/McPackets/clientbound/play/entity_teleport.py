import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class EntityTeleport(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'x': common.types.complex.FixedPointInteger,
		'y': common.types.complex.FixedPointInteger,
		'z': common.types.complex.FixedPointInteger,
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
		return 0x18
