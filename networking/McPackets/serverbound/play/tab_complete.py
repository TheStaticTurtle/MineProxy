import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class TabComplete(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		if self.context.protocol_version == 47:
			return {
				'text': common.types.common.String,
				'looked_at_block': common.types.complex.OptionalPosition,
			}
		if self.context.protocol_version >= 107:
			return {
				'text': common.types.common.String,
				'assume_command': common.types.common.Boolean,
				'looked_at_block': common.types.complex.OptionalPosition,
			}

	def __init__(self, context):
		super().__init__(context)
		self.text = None
		self.looked_at_block = None

		if self.context.protocol_version >= 107:
			self.assume_command = None

	@property
	def ID(self):
		if self.context.protocol_version == 47:
			return 0x14
		if self.context.protocol_version >= 107:
			return 0x01
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
