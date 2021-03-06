import json

import common.types.common
import common.types.complex
from common.context import Context
from common.types.enums import McState, McPacketType
from networking.McPackets.Buffer import Buffer
import logging


def create_simple_packet(context: Context, packet_id: int, packet_data: bytes):
	packet = Packet(context)
	packet.raw_id = packet_id
	packet.raw_data = packet_data
	return packet


class Packet:
	TYPE = McPacketType.Unknown
	SUBTYPE = McState.Unknown

	@property
	def STRUCTURE(self):
		return {
	}
	STRUCTURE_REPR_HIDDEN_FIELDS = []

	def __init__(self, context: Context):
		self.context = context
		self.NAME = ""
		self.NAME += self.TYPE.name + "/" if self.TYPE != McPacketType.Unknown else ""
		self.NAME += self.SUBTYPE.name + "/" if self.SUBTYPE != McState.Unknown else ""
		self.NAME += self.__class__.__name__

		self.raw_id = None
		self.raw_data = None
		self.log = logging.getLogger(self.NAME)

		for key in self.STRUCTURE.keys():
			setattr(self, key, None)

	def is_basic(self):
		return self.__class__ == Packet

	@property
	def ID(self):
		return self.raw_id

	@classmethod
	def from_buffer(cls, context, buffer):
		new_packet = cls(context)
		for key in new_packet.STRUCTURE.keys():
			try:
				value, _ = new_packet.STRUCTURE[key].read(context, buffer)
				new_packet.__setattr__(key, value)
			except Exception as e:
				raise RuntimeError(f"{new_packet.NAME}: Error while reading key {key} for type {new_packet.STRUCTURE[key].__class__.__name__}: {str(e)}")

		new_packet.apply_meta_fields()
		return new_packet

	@classmethod
	def from_basic_packet(cls, packet):
		if isinstance(packet, Packet):
			buffer = Buffer()
			buffer.write(packet.raw_data)
			buffer.reset_cursor()
			return cls.from_buffer(packet.context, buffer)

		else:
			raise RuntimeError(f"Can't create {type(cls)} from {type(packet)} ")

	def apply_meta_fields(self):
		pass

	def craft(self):
		if self.ID is None:
			raise NotImplementedError("Can't craft packet")

		if self.raw_data is not None and len(self.raw_data) > 0:
			return common.types.common.VarInt.write(self.context, self.ID) + self.raw_data
		else:
			buffer = b""
			for key in self.STRUCTURE.keys():
				try:
					value = self.__getattribute__(key)
					buffer += self.STRUCTURE[key].write(self.context, value)
				except Exception as e:
					raise RuntimeError(f"{self.NAME}: Error while writing key {key} for type {self.STRUCTURE[key].__class__.__name__}: {str(e)}")

			return common.types.common.VarInt.write(self.context, self.ID) + buffer

	def __str__(self):
		return repr(self)

	def __repr__(self):
		r = f"<{self.NAME} "
		if self.is_basic():
			return r + f"id=0x{self.ID:02x} len={len(self.raw_data)}>"
		else:
			for key in self.STRUCTURE.keys():
				if key in self.STRUCTURE_REPR_HIDDEN_FIELDS or key[1:] in self.STRUCTURE_REPR_HIDDEN_FIELDS:
					continue
				if key[0] == "_" and hasattr(self, key[1:]):
					key = key[1:]

				if key in self.STRUCTURE and self.STRUCTURE[key] == common.types.complex.JSONString:
					r += f"{key}={json.dumps(self.__getattribute__(key))} "
				else:
					r += f"{key}={self.__getattribute__(key)} "
		return r[:-1] + ">"
