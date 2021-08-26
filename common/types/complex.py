import io
import json
import logging

import pynbt

from common.types import adapters
from common.types.common import *


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

class Float3Rotation(Type):
	def __init__(self):
		self.pitch = None
		self.yaw = None
		self.roll = None

	@staticmethod
	def read(context, file_object):
		r = Float3Rotation()
		r.pitch, _ = Float.read(context, file_object)
		r.yaw, _ = Float.read(context, file_object)
		r.roll, _ = Float.read(context, file_object)
		return r, -1

	@staticmethod
	def write(context, value):
		out  = Float.write(context, value.pitch)
		out += Float.write(context, value.yaw)
		out += Float.write(context, value.roll)
		return out

class Int3Position(Type):
	def __init__(self):
		self.x = None
		self.y = None
		self.z = None

	@staticmethod
	def read(context, file_object):
		r = Int3Position()
		r.x, _ = Integer.read(context, file_object)
		r.y, _ = Integer.read(context, file_object)
		r.z, _ = Integer.read(context, file_object)
		return r, -1

	@staticmethod
	def write(context, value):
		out  = Integer.write(context, value.x)
		out += Integer.write(context, value.y)
		out += Integer.write(context, value.z)
		return out

class EntityMetadata(Type):
	def __init__(self):
		self.values = {}

	def __repr__(self):
		return f"<Metadata values={self.values}>"

	@staticmethod
	def read(context, file_object):
		TYPES = {
			0: Byte,
			1: Short,
			2: Integer,
			3: Float,
			4: String,
			5: Slot,
			6: Int3Position,
			7: Float3Rotation,
		}

		m = EntityMetadata()
		try:
			while True:
				item, _ = UnsignedByte.read(context, file_object)
				if item == 0x7F:
					break
				index = item & 0x1F
				type = TYPES[item >> 5]

				m.values[index] = {
					"item": item,
					"type": type,
					"value": type.read(context, file_object)[0]
				}
		except Exception as e:
			logging.getLogger("EntityMetadataType").error(f"Error, {e} (Packet might not have been terminated correctly)")
		return m, 0

	@staticmethod
	def write(context, value):
		out = b""
		for index in value.values.keys():
			out += UnsignedByte.write(context, value.values[index]["item"])
			out += value.values[index]["type"].write(context, value.values[index]["value"])
		return out + b"\x7F"


class Angle(UnsignedByte):
	@staticmethod
	def read(context, file_object):
		v, l = UnsignedByte.read(context, file_object)
		return 360 * v / 256, l

	@staticmethod
	def write(context, value):
		return UnsignedByte.write(context, round(256 * ((value % 360) / 360)))

FixedPointInteger = adapters.FixedPoint(Integer)
FixedPointByte = adapters.FixedPoint(Byte)

VelocityShort = adapters.Velocity(Short)