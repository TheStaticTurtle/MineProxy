import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class DisplayScoreboard(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'position': common.types.complex.ScoreboardPositionEnum,
			'score_name': common.types.common.String,
		}

	def __init__(self, context):
		super().__init__(context)
		self.position = None
		self.score_name = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x38
		if self.context.protocol_version == 47:
			return 0x3D
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")