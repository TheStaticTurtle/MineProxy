import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class ChangeGameState(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'reason': common.types.complex.GameStateChangeReasonEnum,
			'value': common.types.common.Float,
		}

	def __init__(self, context):
		super().__init__(context)
		self.reason = None
		self.value = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x1E
		if self.context.protocol_version == 47:
			return 0x2B
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
