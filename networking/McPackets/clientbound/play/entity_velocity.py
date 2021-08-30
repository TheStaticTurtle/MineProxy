import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer
from networking.McPackets.SimplePacket import Packet


class EntityVelocity(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'velocity_x': common.types.complex.VelocityShort,
			'velocity_y': common.types.complex.VelocityShort,
			'velocity_z': common.types.complex.VelocityShort,
		}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.velocity_x = None
		self.velocity_y = None
		self.velocity_z = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x3B
		if self.context.protocol_version == 47:
			return 0x12
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")