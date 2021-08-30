import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class Statistics(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'statistics': common.types.complex.StatisticArray,
		}

	def __init__(self, context):
		super().__init__(context)
		self.statistics = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x07
		if self.context.protocol_version == 47:
			return 0x37
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")