import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ClientSettings(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'locale': common.types.common.String,
		'view_distance': common.types.common.Byte,
		'chat_mode': common.types.complex.ClientSettingsChatModesEnum,
		'chat_colors': common.types.common.Boolean,
		'displayed_skin_parts': common.types.common.UnsignedByte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.locale = None
		self.view_distance = None
		self.chat_mode = None
		self.chat_colors = None
		self.displayed_skin_parts = None

	@property
	def ID(self):
		return 0x15
