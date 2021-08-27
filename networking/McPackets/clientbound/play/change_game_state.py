import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class ChangeGameState(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'reason': common.types.complex.GameStateChangeReasonEnum,
		'value': common.types.common.Float,
	}

	def __init__(self, context):
		super().__init__(context)
		self.reason = None
		self.value = None

	@property
	def ID(self):
		return 0x2B
