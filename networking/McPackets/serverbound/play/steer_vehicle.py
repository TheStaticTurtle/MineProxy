import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from common import types

class SteerVehicle(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Play
	STRUCTURE = {
		'sideways': common.types.common.Float,
		'forward': common.types.common.Float,
		'flags': common.types.common.UnsignedByte,
	}

	def __init__(self, context):
		super().__init__(context)
		self.sideways = None
		self.forward = None
		self.flags = None

	@property
	def ID(self):
		return 0x0C
