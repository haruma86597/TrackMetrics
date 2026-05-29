from dataclasses import dataclass
import datetime
from enum import StrEnum, unique


@unique
class Round(StrEnum):
    TIMERACE = "ﾀｲﾑﾚｰｽ"
    SEMIFINAL = "準決勝"
    PRELIMINARY = "予選"


@dataclass
class EventData:
    name: str
    time: datetime.time
    game_url: str
    event_url: str
    round: Round
