import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer
from networking.McPackets.SimplePacket import Packet


class SpawnExperienceOrb(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': common.types.common.VarInt,
		'x': common.types.complex.FixedPointInteger,
		'y': common.types.complex.FixedPointInteger,
		'z': common.types.complex.FixedPointInteger,
		'count': common.types.common.Short,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.x = None
		self.y = None
		self.z = None
		self.count = None

	@property
	def ID(self):
		return 0x11