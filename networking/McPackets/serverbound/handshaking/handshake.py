import common.types.common
import common.types.enums
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket

class Handshake(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Handshaking
	STRUCTURE = {
		'protocol_version': common.types.common.VarInt,
		'server_address': common.types.common.String,
		'server_port': common.types.common.UnsignedShort,
		'_next_state': common.types.common.VarInt,
	}

	def __init__(self, context):
		super().__init__(context)

		self.protocol_version = None
		self.server_address = None
		self.server_port = None
		self._next_state = None

	@property
	def ID(self):
		return 0x00

	@property
	def next_state(self):
		return McState(int(self._next_state))

	@next_state.setter
	def next_state(self, value: common.types.enums.McState):
		self._next_state = value.value
