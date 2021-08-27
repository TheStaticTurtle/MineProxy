import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType, CombatEventEvent
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class SetCompression(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'threshold': common.types.common.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)
		self.threshold = None

	@property
	def ID(self):
		return 0x46
