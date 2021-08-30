import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class Explosion(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'x': common.types.common.Float,
			'y': common.types.common.Float,
			'z': common.types.common.Float,
			'radius': common.types.common.Float,
			'records': common.types.complex.ExplosionRecordArray,
			'player_motion_x': common.types.common.Float,
			'player_motion_y': common.types.common.Float,
			'player_motion_z': common.types.common.Float,
		}

	def __init__(self, context):
		super().__init__(context)
		self.x = None
		self.y = None
		self.z = None
		self.radius = None
		self.records = None
		self.player_motion_x = None
		self.player_motion_y = None
		self.player_motion_z = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x1C
		if self.context.protocol_version == 47:
			return 0x27
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
