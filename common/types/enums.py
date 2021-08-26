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

class Animation(Enum):
	SwingArm = 0
	TakeDamage = 1
	LeaveBed = 2
	EatFood = 3
	CriticalEffect = 4
	MagicCriticalEffect = 5

class Direction(Enum):
	Down = 0
	Up = 1
	North = 2
	South = 3
	West = 4
	East = 5
