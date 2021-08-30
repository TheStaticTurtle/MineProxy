import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class SpawnPlayer(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'entity_id': common.types.common.VarInt,
			'player_uuid': common.types.common.UUID,
			'x': common.types.common.Integer,
			'y': common.types.common.Integer,
			'z': common.types.common.Integer,
			'yaw': common.types.complex.Float,
			'pitch': common.types.complex.Float,
			'current_item': common.types.common.Short,
			'metadata': common.types.complex.EntityMetadata,
		}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.player_uuid = None
		self.x = None
		self.y = None
		self.z = None
		self.yaw = None
		self.pitch = None
		self.current_item = None
		self.metadata = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x05
		if self.context.protocol_version == 47:
			return 0x0C
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
