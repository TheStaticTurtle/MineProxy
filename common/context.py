import logging

import common.types.enums
from common import types

class Context:
	def __init__(self):
		self.log = logging.getLogger("Context")
		self._protocol_version = None
		self._current_state = None
		self._compression_threshold = None

		self._on_protocol_version_change_callbacks = []
		self._on_current_state_change_callbacks = []
		self._on_compression_threshold_change_callbacks = []

	def add_protocol_change_callback(self, fn):
		self._on_protocol_version_change_callbacks.append(fn)

	@property
	def protocol_version(self):
		if self._protocol_version is None:
			self.log.warning("Protocol version is None this might cause issue if packet is not an Handshake packet")
		return self._protocol_version

	@protocol_version.setter
	def protocol_version(self, value: int):
		self._protocol_version = value
		for fn in self._on_protocol_version_change_callbacks:
			fn()


	def add_current_state_callback(self, fn):
		self._on_current_state_change_callbacks.append(fn)

	@property
	def current_state(self):
		if self._current_state is None:
			self.log.error("Current status is None")
			raise RuntimeError("Current status is None")
		return self._current_state

	@current_state.setter
	def current_state(self, value: common.types.enums.McState):
		self._current_state = value
		for fn in self._on_current_state_change_callbacks:
			fn()


	def add_compression_threshold_callback(self, fn):
		self._on_compression_threshold_change_callbacks.append(fn)

	@property
	def compression_threshold(self):
		return self._compression_threshold

	@compression_threshold.setter
	def compression_threshold(self, value: int):
		self._compression_threshold = value
		for fn in self._on_compression_threshold_change_callbacks:
			fn()
