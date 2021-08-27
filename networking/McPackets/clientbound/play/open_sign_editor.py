import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class OpenSignEditor(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'location': common.types.complex.Position,
	}

	def __init__(self, context):
		super().__init__(context)
		self.location = None

	@property
	def ID(self):
		return 0x36