import io
import json
import logging

import pynbt

from common.types import adapters
from common.types.common import *
from common.types.enums import *
from networking.McPackets.Buffer import Buffer


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
	def read(context, file_object: Buffer):
		q = Slot(context)

		if context.protocol_version <= 47:
			q.item_id, _ = Short.read(context, file_object)
			q.present = q.item_id != -1
			if q.present:
				q.item_count, _ = Byte.read(context, file_object)
				q.item_damage, _ = Short.read(context, file_object)
				if file_object.peek(1) == b'\x00':
					file_object.read(1)  # Read the byte as it's not an NBT tag
					q.nbt = None
				else:
					q.nbt, _ = NBT.read(context, file_object)
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
			logging.getLogger("EntityMetadataType").warning(f"Error, {e} (Packet might not have been terminated correctly)")
		return m, 0

	@staticmethod
	def write(context, value):
		out = b""
		for index in value.values.keys():
			out += UnsignedByte.write(context, value.values[index]["item"])
			out += value.values[index]["type"].write(context, value.values[index]["value"])
		return out + b"\x7F"

McStateEnum = adapters.EnumGeneric(VarInt, McState)

class Angle(Type):
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

class AttributeModifier(Type):
	def __init__(self):
		self.uuid = None
		self.amount = None
		self.operation = None

	def __repr__(self):
		return f"<AttributeModifier uuid={self.uuid} amount={self.amount} operation={self.operation}>"

	@staticmethod
	def read(context, file_object):
		m = AttributeModifier()
		m.uuid, _ = UUID.read(context, file_object)
		m.amount, _ = Double.read(context, file_object)
		m.operation, _ = Byte.read(context, file_object)
		return m, 0

	@staticmethod
	def write(context, value):
		out  = UUID.write(context, value.uuid)
		out += Double.write(context, value.amount)
		out += Byte.write(context, value.operation)
		return out
AttributeModifierArray = adapters.PrefixedArray(VarInt, AttributeModifier)

class Properties(Type):
	def __init__(self):
		self.key = None
		self.value = None
		self.modifiers_array = None

	def __repr__(self):
		return f"<Properties key={self.key} value={self.value} modifiers_array={self.modifiers_array}>"

	@staticmethod
	def read(context, file_object):
		m = Properties()
		m.key, _ = String.read(context, file_object)
		m.value, _ = Double.read(context, file_object)
		m.modifiers_array, _ = AttributeModifierArray.read(context, file_object)
		return m, 0

	@staticmethod
	def write(context, value):
		out  = String.write(context, value.key)
		out += Double.write(context, value.value)
		out += AttributeModifierArray.write(context, value.modifiers_array)
		return out
PropertiesArray = adapters.PrefixedArray(Integer, Properties)

class ChunkRecord(Type):
	def __init__(self):
		self.horizontal_position = None
		self.y_coordinate = None
		self.block_id = None

	def __repr__(self):
		return f"<ChunkRecord horizontal_position={self.horizontal_position} y_coordinate={self.y_coordinate} block_id={self.block_id}>"

	@staticmethod
	def read(context, file_object):
		m = ChunkRecord()
		m.horizontal_position, _ = UnsignedByte.read(context, file_object)
		m.y_coordinate, _ = UnsignedByte.read(context, file_object)
		m.block_id, _ = VarInt.read(context, file_object)
		return m, 0

	@staticmethod
	def write(context, value):
		out  = UnsignedByte.write(context, value.horizontal_position)
		out += UnsignedByte.write(context, value.y_coordinate)
		out += VarInt.write(context, value.block_id)
		return out
ChunkRecordArray = adapters.PrefixedArray(VarInt, ChunkRecord)

class ExplosionRecord(Type):
	def __init__(self):
		self.byte_1 = None
		self.byte_2 = None
		self.byte_3 = None

	def __repr__(self):
		return f"<ExplosionRecord byte_1={self.byte_1} byte_2={self.byte_2} byte_3={self.byte_3}>"

	@staticmethod
	def read(context, file_object):
		m = ChunkRecord()
		m.byte_1, _ = UnsignedByte.read(context, file_object)
		m.byte_2, _ = UnsignedByte.read(context, file_object)
		m.byte_3, _ = UnsignedByte.read(context, file_object)
		return m, 0

	@staticmethod
	def write(context, value):
		out  = UnsignedByte.write(context, value.byte_1)
		out += UnsignedByte.write(context, value.byte_2)
		out += UnsignedByte.write(context, value.byte_3)
		return out
ExplosionRecordArray = adapters.PrefixedArray(Integer, ExplosionRecord)

GameStateChangeReasonEnum = adapters.EnumGeneric(UnsignedByte, GameStateChangeReason)
SlotShortArray = adapters.PrefixedArray(Short, Slot)
UpdateEntityActionEnum = adapters.EnumGeneric(UnsignedByte, UpdateEntityAction)

class OptionalNBT(Type):
	@staticmethod
	def read(context, file_object):
		x = file_object.peek(1)
		if x != b"\x00":
			# file_object.seek(-1, whence=io.SEEK_CUR)
			return pynbt.NBTFile(io=file_object), 0
		return None, 0

	@staticmethod
	def write(context, value):
		if value is None:
			return b"\x00"
		else:
			buffer = io.BytesIO()
			pynbt.NBTFile(value=value).save(buffer)
			return buffer.getvalue()

class Statistic(Type):
	def __init__(self):
		self.name = None
		self.value = None

	def __repr__(self):
		return f"<Statistic name={self.name} value={self.value}>"

	@staticmethod
	def read(context, file_object):
		m = ChunkRecord()
		m.name, _ = String.read(context, file_object)
		m.value, _ = VarInt.read(context, file_object)
		return m, 0

	@staticmethod
	def write(context, value):
		out  = String.write(context, value.name)
		out += VarInt.write(context, value.value)
		return out

StatisticArray = adapters.PrefixedArray(VarInt, Statistic)

VarIntStringArray = adapters.PrefixedArray(VarInt, String)

ScoreboardPositionEnum = adapters.EnumGeneric(Byte, ScoreboardPosition)

CombatEventEventEnum = adapters.EnumGeneric(VarInt, CombatEventEvent)

UseEntityTypeEnum = adapters.EnumGeneric(VarInt, UseEntityType)

PlayerDiggingStatusEnum = adapters.EnumGeneric(VarInt, PlayerDiggingStatus)

EntityActionActionEnum = adapters.EnumGeneric(VarInt, EntityActionAction)

OptionalPosition = adapters.BooleanPrefixedOptional(Position)

ClientSettingsChatModesEnum = adapters.EnumGeneric(Byte, ClientSettingsChatModes)

ClientStatusActionsEnums = adapters.EnumGeneric(VarInt, ClientStatusActions)

ResourcePackStatusResultEnum = adapters.EnumGeneric(VarInt, ResourcePackStatusResult)

AnimationAnimationEnum = adapters.EnumGeneric(UnsignedByte, Animation)