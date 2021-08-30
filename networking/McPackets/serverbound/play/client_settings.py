import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class ClientSettings(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		out = {
			'locale': common.types.common.String,
			'view_distance': common.types.common.Byte,
			'chat_mode': common.types.complex.ClientSettingsChatModesEnum,
			'chat_colors': common.types.common.Boolean,
			'displayed_skin_parts': common.types.common.UnsignedByte,
		}
		if self.context.protocol_version >= 107:
			out["main_hand"] = common.types.complex.ClientSettingsMainHandEnum

		return out

	def __init__(self, context):
		super().__init__(context)
		self.locale = None
		self.view_distance = None
		self.chat_mode = None
		self.chat_colors = None
		self.displayed_skin_parts = None
		if self.context.protocol_version >= 107:
			self.main_hand = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x04
		if self.context.protocol_version == 47:
			return 0x15
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")
