import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType, CombatEventEvent
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class RessourcePackSend(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
		'url': common.types.common.String,
		'sha1_hash': common.types.common.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.url = None
		self.sha1_hash = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x32
		if self.context.protocol_version == 47:
			return 0x48
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
