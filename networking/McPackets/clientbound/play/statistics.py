import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class Statistics(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'statistics': common.types.complex.StatisticArray,
	}

	def __init__(self, context):
		super().__init__(context)
		self.statistics = None

	@property
	def ID(self):
		return 0x37