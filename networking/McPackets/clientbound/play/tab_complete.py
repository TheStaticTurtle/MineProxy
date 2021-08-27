import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class TabComplete(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'matches': common.types.complex.VarIntStringArray,
	}

	def __init__(self, context):
		super().__init__(context)
		self.matches = None

	@property
	def ID(self):
		return 0x3A