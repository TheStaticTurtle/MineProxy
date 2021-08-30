import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType, CombatEventEvent
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class UpdateEntityNBT(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
		'entity_id': common.types.common.VarInt,
		'tag': common.types.complex.NBT,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.tag = None

	@property
	def ID(self):
		return 0x49
