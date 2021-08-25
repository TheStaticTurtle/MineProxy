from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Handshake(SimplePacket.Packet):
	TYPE = McPacketType.ServerBound
	SUBTYPE = McState.Handshaking
	STRUCTURE = {
		'protocol_version': types.VarInt,
		'server_address': types.String,
		'server_port': types.UnsignedShort,
		'_next_state': types.VarInt,
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
		return types.McState(int(self._next_state))

	@next_state.setter
	def next_state(self, value: types.McState):
		self._next_state = value.value
