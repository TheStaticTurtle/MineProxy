import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class EntityRelativeMove(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'delta_x': common.types.common.Byte,
		'delta_y': common.types.common.Byte,
		'delta_z': common.types.common.Byte,
		'on_ground': common.types.common.Boolean,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.delta_x = None
		self.delta_y = None
		self.delta_z = None
		self.on_ground = None

	@property
	def ID(self):
		return 0x15
