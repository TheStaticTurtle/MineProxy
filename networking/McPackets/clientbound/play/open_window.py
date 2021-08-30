import common.types.common
import common.types.complex
from common.types.enums import McState, McPacketType
from networking.McPackets import SimplePacket
from networking.McPackets.Buffer import Buffer


class OpenWindow(SimplePacket.Packet):
	TYPE = McPacketType.Clientbound
	SUBTYPE = McState.Play
	
	@property
	def STRUCTURE(self):
		return {
			'window_id': common.types.common.UnsignedByte,
			'window_type': common.types.common.String,
			'window_title': common.types.complex.JSONString,
			'umber_of_slots': common.types.common.UnsignedByte,
			# 'entity_id': common.types.common.Integer,
		}

	def __init__(self, context):
		super().__init__(context)
		self.window_id = None
		self.window_type = None
		self.window_title = None
		self.umber_of_slots = None
		self.entity_id = None

	@property
	def ID(self):
		if self.context.protocol_version >= 107:
			return 0x13
		if self.context.protocol_version == 47:
			return 0x2D
		raise RuntimeError(f"Invalid protocol version for packet {self.__class__.__name__}")

	@classmethod
	def from_basic_packet(cls, packet):
		buffer = Buffer()
		buffer.write(packet.raw_data)
		buffer.reset_cursor()

		new_packet = cls(packet.context)
		for key in new_packet.STRUCTURE.keys():
			try:
				value, _ = new_packet.STRUCTURE[key].read(packet.context, buffer)
				new_packet.__setattr__(key, value)
			except Exception as e:
				raise RuntimeError(f"{new_packet.NAME}: Error while writing key {key} for type {new_packet.STRUCTURE[key].__class__.__name__}: {str(e)}")

		if new_packet.window_type == "EntityHorse":
			new_packet.entity_id, _ = common.types.common.Integer.read(packet.context, buffer)

		new_packet.apply_meta_fields()
		return new_packet


	def craft(self):
		buffer = b""
		for key in self.STRUCTURE.keys():
			try:
				value = self.__getattribute__(key)
				buffer += self.STRUCTURE[key].write(self.context, value)
			except Exception as e:
				raise RuntimeError(f"{self.NAME}: Error while writing key {key} for type {self.STRUCTURE[key].__class__.__name__}: {str(e)}")

		if self.window_type == "EntityHorse":
			buffer += common.types.common.Integer.write(self.context, self.entity_id)

		return common.types.common.VarInt.write(self.context, self.ID) + buffer


