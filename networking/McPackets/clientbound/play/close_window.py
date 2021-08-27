import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class CloseWindow(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'window_id': common.types.common.UnsignedByte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.window_id = None

	@property
	def ID(self):
		return 0x2E