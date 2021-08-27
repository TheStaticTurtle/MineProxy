import logging
import typing
from enum import Enum

from common.types import Type
from common.types.common import Boolean, VarInt


class BooleanPrefixedOptional(Type):
	def __init__(self, type: typing.Type[Type]):
		self.type = type

	def read(self, context, file_object):
		is_present, _ = Boolean.read(context, file_object)
		if is_present:
			value, _ = self.type.read(context, file_object)
			return value, 0
		return None, 0

	def write(self, context, value):
		out = Boolean.write(context, value is not None)
		if value is not None:
			out += self.type.write(context, value)
		return out


class EnumGeneric(Type):
	def __init__(self, value_type: typing.Type[Type], enum: typing.Type[Enum]):
		self.value_type = value_type
		self.enum = enum

	def read(self, context, file_object):
		value, _ = self.value_type.read(context, file_object)
		return self.enum(value), _

	def write(self, context, value: Enum):
		return self.value_type.write(context, value.value)

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


class PrefixedArray(Type):
	__slots__ = 'element_count_type', 'element_type'

	def __init__(self, element_count_type: typing.Type[Type], element_type: typing.Type[Type]):
		self.element_count_type = element_count_type
		self.element_type = element_type

	def read(self, context, file_object):
		elements = []
		element_count, _ = self.element_count_type.read(context, file_object)
		for i in range(element_count):
			try:
				x, _ = self.element_type.read(context, file_object)
				elements.append(x)
			except Exception as e:
				logging.getLogger(f"PrefixedArray<{self.element_count_type.__class__.__name__}>").warning(f"Read {i}/{element_count} : {e}")
		return elements, 0

	def write(self, context, values):
		out = self.element_count_type.write(context, len(values))
		for value in values:
			out += self.element_type.write(context, value)
		return out