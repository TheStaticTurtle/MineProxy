import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class Explosion(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
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
		return 0x27
