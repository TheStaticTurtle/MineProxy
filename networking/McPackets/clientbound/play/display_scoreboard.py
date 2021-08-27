import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class DisplayScoreboard(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'position': common.types.complex.ScoreboardPositionEnum,
		'score_name': common.types.common.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.position = None
		self.score_name = None

	@property
	def ID(self):
		return 0x3D