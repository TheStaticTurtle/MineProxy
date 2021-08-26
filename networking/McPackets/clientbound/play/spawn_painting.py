import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer
from networking.McPackets.SimplePacket import Packet


class SpawnPainting(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'title': common.types.common.String,
		'location': common.types.complex.Position,
		'direction': common.types.common.UnsignedByte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.title = None
		self.location = None
		self.direction = None

	@property
	def ID(self):
		return 0x10