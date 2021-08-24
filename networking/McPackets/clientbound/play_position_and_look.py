import io
from networking.McPackets import SimplePacket
from common import types


class PlayPositionAndLook(SimplePacket.Packet):
	def __init__(self, id, data_lenght, data):
		SimplePacket.Packet.__init__(self, id, data_lenght, data)
		self.x = 0
		self.y = 0
		self.z = 0
		self.yaw = 0
		self.pitch = 0
		self.flags = 0
		self.teleport_id = 0
		self.dismount_vehicle = 0

	def __repr__(self):
		return f"<ClientBound/PlayPositionAndLook x={self.x} y={self.y} z={self.z} yaw={self.yaw} pitch={self.pitch} flags={self.flags} teleport_id={self.teleport_id} dismount_vehicle={self.dismount_vehicle}>"

	@staticmethod
	def from_basic_packet(packet, protocol_version):
		stream = io.BytesIO(packet.data)

		new_packet = PlayPositionAndLook(packet.id, packet.data_lenght, packet.data)
		new_packet.x,_ = types.Double.read(stream)
		new_packet.y,_ = types.Double.read(stream)
		new_packet.z,_ = types.Double.read(stream)
		new_packet.yaw,_ = types.Float.read(stream)
		new_packet.pitch,_ = types.Float.read(stream)
		new_packet.flags,_ = types.Byte.read(stream)
		new_packet.teleport_id,_ = types.VarInt.read(stream)
		new_packet.dismount_vehicle,_ = types.Boolean.read(stream)
		return new_packet
