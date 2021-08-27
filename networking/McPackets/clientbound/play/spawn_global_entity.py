import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class SpawnGlobalEntity(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'type': common.types.common.Byte,
		'x': common.types.common.Integer,
		'y': common.types.common.Integer,
		'z': common.types.common.Integer,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.type = None
		self.x = None
		self.y = None
		self.z = None

	@property
	def ID(self):
		return 0x2C
