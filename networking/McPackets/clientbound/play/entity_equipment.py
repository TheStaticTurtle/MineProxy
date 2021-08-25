from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class EntityEquipment(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'entity_id': types.VarInt,
		'slot': types.Short,
		'item': types.Slot,
	}

	def __init__(self, context):
		super().__init__(context)
		self.entity_id = None
		self.slot = None
		self.item = None

	@property
	def ID(self):
		return 0x04