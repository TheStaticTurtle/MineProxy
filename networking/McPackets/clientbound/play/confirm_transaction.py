import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class ConfirmTransaction(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'window_id': common.types.common.UnsignedByte,
		'action_number': common.types.common.Short,
		'accepted': common.types.common.Boolean,
	}

	def __init__(self, context):
		super().__init__(context)
		self.window_id = None
		self.action_number = None
		self.accepted = None

	@property
	def ID(self):
		return 0x32