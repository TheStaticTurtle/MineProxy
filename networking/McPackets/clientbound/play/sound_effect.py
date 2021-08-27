import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class SoundEffect(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'sound_name': common.types.common.String,
		'x': common.types.common.Integer,
		'y': common.types.common.Integer,
		'z': common.types.common.Integer,
		'volume': common.types.complex.Float,
		'pitch': common.types.common.UnsignedByte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.sound_name = None
		self.x = None
		self.y = None
		self.z = None
		self.volume = None
		self.pitch = None

	@property
	def ID(self):
		return 0x29
