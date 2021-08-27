import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class WindowProperty(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'window_id': common.types.common.UnsignedByte,
		'property': common.types.common.Short,
		'value': common.types.common.Short,
	}

	def __init__(self, context):
		super().__init__(context)
		self.window_id = None
		self.property = None
		self.value = None

	@property
	def ID(self):
		return 0x31