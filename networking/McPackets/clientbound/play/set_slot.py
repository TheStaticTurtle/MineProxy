import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class SetSlot(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'window_id': common.types.common.UnsignedByte,
		'slot': common.types.common.Short,
		'slot_data': common.types.complex.Slot,
	}

	def __init__(self, context):
		super().__init__(context)
		self.window_id = None
		self.slot = None
		self.slot_data = None

	@property
	def ID(self):
		return 0x2F