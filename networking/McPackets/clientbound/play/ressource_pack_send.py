import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType, CombatEventEvent
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class RessourcePackSend(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'url': common.types.common.String,
		'sha1_hash': common.types.common.String,
	}

	def __init__(self, context):
		super().__init__(context)
		self.url = None
		self.sha1_hash = None

	@property
	def ID(self):
		return 0x48
