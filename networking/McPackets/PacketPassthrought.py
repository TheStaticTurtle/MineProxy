import select
import zlib

from common import types
from common.connection import Connection
from common.context import Context
from networking.McPackets import SimplePacket
from .Buffer import Buffer

class PacketPasstrought:
	TIME_OUT = 0

	def __init__(self, context: Context, connection: Connection):
		self.context = context
		self.connection = connection

	def read_one(self):
		ready_to_read = select.select([self.connection.file], [], [], self.TIME_OUT)[0]
		if ready_to_read:
			try:
				packet_length, packet_length_size = types.VarInt.read(self.connection.file)
			except RuntimeError as e:
				if "Unexpected end of message at byte 0" in str(e):
					return None
				raise e

			buffer = Buffer()
			buffer.write(self.connection.file.read(packet_length))
			# Ensure we read all the packet
			while len(buffer.get_writable()) < packet_length:
				buffer.write(self.connection.file.read(packet_length - len(buffer.get_writable())))
			buffer.reset_cursor()

			if self.context.compression_threshold is not None:
				compressed_size, _ = types.VarInt.read(buffer)
				if compressed_size > 0:
					x = buffer.read(compressed_size)
					decompressed_packet = zlib.decompress(x)
					buffer.reset()
					buffer.write(decompressed_packet)
					buffer.reset_cursor()

			packet_id, packet_id_size = types.VarInt.read(buffer)
			packet_data = buffer.read_all()

			return SimplePacket.create_simple_packet(
				packet_id,
				packet_data
			)
		return None

	def build_packet(self, packet):
		buffer = Buffer()

		buffer.write(packet.craft(self.context.protocol_version))

		if self.context.compression_threshold is not None:
			if len(buffer.get_writable()) > self.context.compression_threshold != -1:
				# compress the current payload
				uncompressed_data = buffer.get_writable()
				compressed_data = zlib.compress(uncompressed_data)
				buffer.reset()
				# write out the length of the compressed payload
				buffer.write(types.VarInt.write(len(uncompressed_data)))
				# write the compressed payload itself
				buffer.write(compressed_data)
			else:
				# write out a 0 to indicate uncompressed data
				packet_data = buffer.get_writable()
				buffer.reset()
				buffer.write(types.VarInt.write(0))
				buffer.write(packet_data)

		data = types.VarInt.write(len(buffer.get_writable()))  # Packet Size

		return data + buffer.get_writable()
