import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class PlayerBlockPlacement(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'location': common.types.complex.Position,
		'face': common.types.common.Byte,
		'held_item': common.types.complex.Slot,
		'cursor_position_x': common.types.common.Byte,
		'cursor_position_y': common.types.common.Byte,
		'cursor_position_z': common.types.common.Byte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.location = None
		self.face = None
		self.held_item = None
		self.cursor_position_x = None
		self.cursor_position_y = None
		self.cursor_position_z = None

	@property
	def ID(self):
		return 0x08
