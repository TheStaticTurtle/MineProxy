import io
from networking.McPackets import SimplePacket
from common import types


class Handshake(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.protocol_version = 0
		self.server_address = b""
		self.server_port = 0
		self.next_state = 0

	def __repr__(self):
		return f"<Serverbound/Handshake protocol_version={self.protocol_version} server_address={self.server_address} server_port={self.server_port} next_state={self.next_state}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = Handshake(packet.id, packet.data_lenght, packet.data)
		new_packet.protocol_version, _ = types.VarInt.read(stream)
		new_packet.server_address, _ = types.String.read(stream)
		new_packet.server_port, _ = types.UnsignedShort.read(stream)
		new_packet.next_state = types.McState(types.VarInt.read(stream)[0])

		return new_packet

	def craft(self, protocol_version):
		data = b""
		data += types.VarInt.write(self.id)
		data += types.VarInt.write(self.protocol_version)
		data += types.String.write(self.server_address)
		data += types.UnsignedShort.write(self.server_port)
		data += types.VarInt.write(self.next_state.value)

		return data
