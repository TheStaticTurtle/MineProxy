import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class TabComplete(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'matches': common.types.complex.VarIntStringArray,
		}

	def __init__(self, context):
		super().__init__(context)
		self.matches = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x0E
		if self.context.protocol_version == 47:
			return 0x3A
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")