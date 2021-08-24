import json

from common import types
from common.types import McPacketType, McState
from networking.McPackets.Buffer import Buffer
import binascii
import logging

def create_simple_packet(packet_id, packet_data):
	packet = Packet()
	packet._id = packet_id
	packet.raw_data = packet_data
	return packet

class Packet:
	ID = None
	TYPE = McPacketType.Unknown
	SUBTYPE = McState.Unknown
	STRUCTURE = {
	}
	STRUCTURE_REPR_HIDDEN_FIELDS = []

	def __init__(self):
		self.NAME = ""
		self.NAME += self.TYPE.name + "/" if self.TYPE != McPacketType.Unknown else ""
		self.NAME += self.SUBTYPE.name + "/" if self.SUBTYPE != McState.Unknown else ""
		self.NAME += self.__class__.__name__

		self._id = self.ID
		self.raw_data = None
		self.log = logging.getLogger(self.NAME)

		for key in self.STRUCTURE.keys():
			setattr(self, key, None)

	@property
	def id(self):
		return self._id

	@classmethod
	def from_basic_packet(cls, packet, protocol_version):
		if isinstance(packet, Packet):
			buffer = Buffer()
			buffer.write(packet.raw_data)
			buffer.reset_cursor()

			new_packet = cls()
			for key in cls.STRUCTURE.keys():
				value, _ = cls.STRUCTURE[key].read(buffer)
				new_packet.__setattr__(key, value)

			return new_packet
		else:
			raise RuntimeError(f"Can't create {type(cls)} from {type(packet)} ")

	def craft(self, protocol_version):
		if self._id is None:
			raise NotImplementedError("Can't craft packet")

		if self.raw_data is not None and len(self.raw_data) > 0:
			return types.VarInt.write(self._id) + self.raw_data
		else:
			buffer = b""
			for key in self.STRUCTURE.keys():
				try:
					value = self.__getattribute__(key)
					buffer += self.STRUCTURE[key].write(value)
				except Exception as e:
					raise RuntimeError(f"{self.NAME}: Error while writing key {key} for type {self.STRUCTURE[key].__class__.__name__}: {str(e)}")
			return types.VarInt.write(self._id) + buffer

	def __str__(self):
		return repr(self)

	def __repr__(self):
		r = f"<{self.NAME} "
		if self.__class__ == Packet:
			return r + f"id=0x{self._id:02x} len={len(self.raw_data)}>"
		else:
			for key in self.STRUCTURE.keys():
				if key in self.STRUCTURE_REPR_HIDDEN_FIELDS or key[1:] in self.STRUCTURE_REPR_HIDDEN_FIELDS:
					continue
				if key[0] == "_" and hasattr(self,key[1:]):
					key = key[1:]

				if key in self.STRUCTURE and self.STRUCTURE[key] == types.JSONString:
					r += f"{key}={json.dumps(self.__getattribute__(key))} "
				else:
					r += f"{key}={self.__getattribute__(key)} "
		return r[:-1] + ">"
