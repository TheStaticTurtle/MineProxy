import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType, CombatEventEvent
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class Camera(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
		'camera_id': common.types.common.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)
		self.camera_id = None

	@property
	def ID(self):
		return 0x43
