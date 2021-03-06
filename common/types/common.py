import struct
import uuid
from abc import ABC

from common.types import Type


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
	def write(h, value):
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


class UUID(Type):
	@staticmethod
	def read(context, file_object):
		return str(uuid.UUID(bytes=file_object.read(16))), 16

	@staticmethod
	def write(context, value):
		return uuid.UUID(value).bytes


class UnsignedLong(Type):
	@staticmethod
	def read(context, file_object):
		return struct.unpack('>Q', file_object.read(8))[0], 8

	@staticmethod
	def write(context, value):
		return struct.pack('>Q', value)