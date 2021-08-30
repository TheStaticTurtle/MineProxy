import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class ConfirmTransaction(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'window_id': common.types.common.Byte if self.context.protocol_version >= 107 else common.types.common.UnsignedByte,
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
		if self.context.protocol_version >= 107:
			return 0x11
		if self.context.protocol_version == 47:
			return 0x32
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")