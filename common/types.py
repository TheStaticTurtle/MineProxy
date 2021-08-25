import io
import json
import struct
import uuid
from abc import ABC
from enum import Enum
import pynbt


class McState(Enum):
	Handshaking = 0
	Status = 1
	Login = 2
	Play = 3
	Unknown = 4


class McPacketType(Enum):
	Clientbound = 0
	ServerBound = 1
	Unknown = 2


class Type(object):
	@staticmethod
	def read(context, file_object):
		raise NotImplementedError("Base data type not serializable")

	@staticmethod
	def write(context, value):
		raise NotImplementedError("Base data type not serializable")


class Boolean(Type):
	@staticmethod
	def read(context, file_object):
		return struct.unpack('?', file_object.read(1))[0], 1

	@staticmethod
	def write(context, value):
		return struct.pack('?', value)


class UnsignedByte(Type):
	@staticmethod
	def read(context, file_object):
		return struct.unpack('>B', file_object.read(1))[0], 1

	@staticmethod
	def write(context, value):
		return struct.pack('>B', value)


class Byte(Type):
	@staticmethod
	def read(context, file_object):
		return struct.unpack('>b', file_object.read(1))[0], 1

	@staticmethod
	def write(context, value):
		return struct.pack('>b', value)


class Short(Type):
	@staticmethod
	def read(context, file_object):
		return struct.unpack('>h', file_object.read(2))[0], 2

	@staticmethod
	def write(context, value):
		return struct.pack('>h', value)


class UnsignedShort(Type):
	@staticmethod
	def read(context, file_object):
		return struct.unpack('>H', file_object.read(2))[0], 2

	@staticmethod
	def write(context, value):
		return struct.pack('>H', value)


class Integer(Type):
	@staticmethod
	def read(context, file_object):
		return struct.unpack('>i', file_object.read(4))[0], 4

	@staticmethod
	def write(context, value):
		return struct.pack('>i', value)


VARINT_SIZE_TABLE = {
	2 ** 7: 1,
	2 ** 14: 2,
	2 ** 21: 3,
	2 ** 28: 4,
	2 ** 35: 5,
	2 ** 42: 6,
	2 ** 49: 7,
	2 ** 56: 8,
	2 ** 63: 9,
	2 ** 70: 10,
	2 ** 77: 11,
	2 ** 84: 12
}


class VarInt(Type):
	@staticmethod
	def read(context, file_object):
		size = 0
		number = 0
		for i in range(5):
			byte = file_object.read(1)
			if len(byte) < 1:
				raise RuntimeError(f"Unexpected end of message at byte {size}")
			size += 1
			byte = ord(byte)
			number |= (byte & 0x7F) << 7 * i
			if not byte & 0x80:
				break
		return number, size

	@staticmethod
	def write(context, value):
		out = bytes()
		while True:
			byte = value & 0x7F
			value >>= 7
			out += struct.pack("B", byte | (0x80 if value > 0 else 0))
			if value == 0:
				break
		return out

	@staticmethod
	def size(value):
		for max_value, size in VARINT_SIZE_TABLE.items():
			if value < max_value:
				return size


class Long(Type):
	@staticmethod
	def read(context, file_object):
		return struct.unpack('>q', file_object.read(8))[0], 8

	@staticmethod
	def write(context, value):
		return struct.pack('>q', value)


class Float(Type):
	@staticmethod
	def read(context, file_object):
		return struct.unpack('>f', file_object.read(4))[0], 4

	@staticmethod
	def write(context, value):
		return struct.pack('>f', value)


class Double(Type):
	@staticmethod
	def read(context, file_object):
		return struct.unpack('>d', file_object.read(8))[0], 8

	@staticmethod
	def write(context, value):
		return struct.pack('>d', value)


class ShortPrefixedByteArray(Type):
	@staticmethod
	def read(context, file_object):
		length = Short.read(context, file_object)
		return struct.unpack(str(length) + "s", file_object.read(length))[0], -1

	@staticmethod
	def write(context, value):
		out = Short.write(context, len(value))
		return out + value


class VarIntPrefixedByteArray(Type):
	@staticmethod
	def read(context, file_object):
		length, _ = VarInt.read(context, file_object)
		return struct.unpack(str(length) + "s", file_object.read(length))[0], length

	@staticmethod
	def write(context, value):
		out = VarInt.write(context, len(value))
		return out + struct.pack(str(len(value)) + "s", value)


class ByteArray(Type):
	@staticmethod
	def read(context, file_object):
		x = file_object.read(99999999)
		return x, len(x)

	@staticmethod
	def write(context, value: bytes):
		return struct.pack(str(len(value)) + "s", value)


class String(Type):
	@staticmethod
	def read(context, file_object):
		length, _ = VarInt.read(context, file_object)
		r = file_object.read(length).decode("utf-8")

		return r, len(r)

	@staticmethod
	def write(context, value):
		value = value.encode('utf-8')
		out = VarInt.write(context, len(value))
		return out + value


class JSONString(Type):
	@staticmethod
	def read(context, file_object):
		length, _ = VarInt.read(context, file_object)
		r = file_object.read(length).decode("utf-8")

		return json.loads(r), -1

	@staticmethod
	def write(context, value):
		value = json.dumps(value).encode('utf-8')
		out = VarInt.write(context, len(value))
		return out + value


class UUID(Type, ABC):
	@staticmethod
	def read(context, file_object):
		return str(uuid.UUID(bytes=file_object.read(16))), 16


class UnsignedLong(Type):
	@staticmethod
	def read(context, file_object):
		return struct.unpack('>Q', file_object.read(8))[0], 8

	@staticmethod
	def write(context, value):
		return struct.pack('>Q', value)


class Position(Type):
	@staticmethod
	def read(context, file_object):
		location, _ = UnsignedLong.read(context, file_object)
		x = int(location >> 38)  # 26 most significant bits

		if context.protocol_version > 443:
			z = int((location >> 12) & 0x3FFFFFF)  # 26 intermediate bits
			y = int(location & 0xFFF)  # 12 least signficant bits
		else:
			y = int((location >> 26) & 0xFFF)  # 12 intermediate bits
			z = int(location & 0x3FFFFFF)  # 26 least significant bits

		if x >= pow(2, 25):
			x -= pow(2, 26)

		if y >= pow(2, 11):
			y -= pow(2, 12)

		if z >= pow(2, 25):
			z -= pow(2, 26)

		return (x, y, z), _

	@staticmethod
	def write(context, position):
		x, y, z = position
		if context.protocol_version > 443:
			value = (x & 0x3FFFFFF) << 38 | (z & 0x3FFFFFF) << 12 | (y & 0xFFF)
			return UnsignedLong.write(context, value)
		else:
			value = (x & 0x3FFFFFF) << 38 | (y & 0xFFF) << 26 | (z & 0x3FFFFFF)
			return UnsignedLong.write(context, value)

class NBT(Type):
	@staticmethod
	def read(context, file_object):
		return pynbt.NBTFile(io=file_object), 0

	@staticmethod
	def write(context, value):
		buffer = io.BytesIO()
		pynbt.NBTFile(value=value).save(buffer)
		return buffer.getvalue()

class Slot(Type):
	def __init__(self, context):
		self.context = context

		self.present = None
		self.item_id = None
		self.item_count = None
		self.nbt = None
		self.nbt_raw = None

		if context.protocol_version <= 47:
			self.item_damage = None

	def __repr__(self):
		if self.present:
			if self.context.protocol_version <= 47:
				return f"<Item present={self.present} item_id={self.item_id} item_count={self.item_count} nbt={self.nbt} item_damage={self.item_damage}>"
			else:
				return f"<Item present={self.present} item_id={self.item_id} item_count={self.item_count} nbt={self.nbt}>"
		else:
			return f"<Item present={self.present}>"

	@staticmethod
	def read(context, file_object):
		q = Slot(context)

		if context.protocol_version <= 47:
			q.item_id, _ = Short.read(context, file_object)
			q.present = q.item_id != -1
			if q.present:
				q.item_count, _ = Byte.read(context, file_object)
				q.item_damage, _ = Short.read(context, file_object)
				q.nbt_raw = file_object.read_all()
				stream = io.BytesIO(q.nbt_raw)
				if stream.read(1) == b'\x00':
					q.nbt = None
				else:
					stream.seek(0)
					q.nbt, _ = NBT.read(context, stream)

		return q, 0

	@staticmethod
	def write(context, value):
		if context.protocol_version <= 47:
			out = Short.write(context, value.item_id)
			if value.present:
				out += Byte.write(context, value.item_count)
				out += Short.write(context, value.item_damage)
				if value.nbt is None:
					out += b"\x00"
				else:
					out += NBT.write(context, value.nbt)

			return out
		return b""