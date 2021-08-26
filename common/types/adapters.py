import typing
from enum import Enum

from common.types import Type
from common.types.common import Boolean, VarInt


class BooleanPrefixedOptional(Type):
	def __init__(self, type: Type):
		self.type = type
		self.value = None

	def read(self, context, file_object):
		is_present, _ = Boolean.read(context, file_object)
		if is_present:
			self.value, _ = self.type.read(context, file_object)
		else:
			self.value = None

	def write(self, context, value):
		out = Boolean.write(context, value is not None)
		if value is not None:
			out += self.type.write(context, value)
		return out


class EnumVarTnt(Type):
	def __init__(self, enum: typing.Type[Enum]):
		self.enum = enum

	def read(self, context, file_object):
		value, _ = VarInt.read(context, file_object)
		return self.enum(value), _

	def write(self, context, value: Enum):
		return VarInt.write(context, value.value)


class FixedPoint(Type):
	__slots__ = 'type', 'denominator'

	def __init__(self, type: typing.Type[Type], fractional_bits=5):
		self.type = type
		self.denominator = 2**fractional_bits

	def read(self, context, file_object):
		v, l = self.type.read(context, file_object)
		return v / self.denominator, l

	def write(self, context, value):
		return self.type.write(context, int(value * self.denominator))


class Velocity(Type):
	__slots__ = 'type', 'divider'

	def __init__(self, integer_type: typing.Type[Type], divider=8000.0):
		self.type = integer_type
		self.divider = divider

	def read(self, context, file_object):
		v, l = self.type.read(context, file_object)
		return float(v) / self.divider, l

	def write(self, context, value):
		return self.type.write(context, int(value * self.divider))