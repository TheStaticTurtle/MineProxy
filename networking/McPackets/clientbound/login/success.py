# import io
# from networking.McPackets import SimplePacket
# from common import types
#
#
# class LoginSuccess(SimplePacket.Packet):
# 	def __init__(self, id, data_lenght, data):
# 		SimplePacket.Packet.__init__(self, id, data_lenght, data)
# 		self.uuid = None
# 		self.username = ""
#
# 	def __repr__(self):
# 		return f"<ClientBound/LoginSuccess uuid={self.uuid} username={self.username}>"
#
# 	@staticmethod
# 	def from_basic_packet(packet, protocol_version):
# 		stream = io.BytesIO(packet.data)
#
# 		new_packet = LoginSuccess(packet.id, packet.data_lenght, packet.data)
#
# 		if protocol_version >= 107:
# 			new_packet.uuid, _ = types.UUID.read(stream)
# 			new_packet.username, _ = types.String.read(stream)
# 		else:
# 			new_packet.uuid, _ = types.String.read(stream)
# 			new_packet.username, _ = types.String.read(stream)
#
# 		return new_packet

from common.types import McPacketType, McState
from networking.McPackets import SimplePacket
from common import types

class Success(SimplePacket.Packet):
	ID = 0x02
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Login
	STRUCTURE = {
		'uuid': types.String,
		'username': types.String,
	}

	def __init__(self):
		super().__init__()
		self.uuid = None
		self.username = None
