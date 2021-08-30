import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType, CombatEventEvent
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class PlayerListHeaderAndFooter(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'header': common.types.complex.JSONString,
			'footer': common.types.complex.JSONString,
		}

	def __init__(self, context):
		super().__init__(context)
		self.header = None
		self.footer = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x48
		if self.context.protocol_version == 47:
			return 0x47
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
