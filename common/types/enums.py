from enum import Enum


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