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

class GameStateChangeReason(Enum):
	InvalidBed = 0
	EndRaining = 1
	BeginRaining = 2
	ChangeGameMode = 3
	EnterCredits = 4
	DemoMessage = 5
	ArrowHittingPlayer = 6
	FadeValue = 7
	FadeTime = 8
	PlayMobAppearance = 9

class UpdateEntityAction(Enum):
	SetSpawnPotentials = 1
	SetCommandBlockText = 2
	SetBeaconLevel = 3
	SetMobHeadRotation = 4
	SetFlowerType = 5
	SetBanner = 6

class ScoreboardPosition(Enum):
	List = 0
	Sidebar = 1
	BellowName = 2

class CombatEventEvent(Enum):
	EnterCombat = 0
	EndCombat = 1
	EntityDead = 2