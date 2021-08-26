import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class EntityLookAndRelativeMove(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'delta_x': common.types.complex.FixedPointByte,
		'delta_y': common.types.complex.FixedPointByte,
		'delta_z': common.types.complex.FixedPointByte,
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
		return 0x17
