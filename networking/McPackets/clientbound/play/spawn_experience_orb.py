import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer
from networking.McPackets.SimplePacket import Packet


class SpawnExperienceOrb(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'x': common.types.complex.Double if self.context.protocol_version >= 107 else common.types.complex.FixedPointInteger5B,
			'y': common.types.complex.Double if self.context.protocol_version >= 107 else common.types.complex.FixedPointInteger5B,
			'z': common.types.complex.Double if self.context.protocol_version >= 107 else common.types.complex.FixedPointInteger5B,
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
		if self.context.protocol_version >= 107:
			return 0x01
		if self.context.protocol_version == 47:
			return 0x11
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")