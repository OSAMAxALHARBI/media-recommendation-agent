from dataclasses import dataclass, field, asdict
from typing import Literal, Optional, List, Dict, Any
from datetime import datetime

MediaType = Literal["anime", "movie", "tv", "manga"]
MediaStatus = Literal["watching", "reading", "completed", "dropped", "planned", "on_hold"]

@dataclass
class MediaItem:
    id: str
    source: Literal["tmdb", "anilist"]
    type: MediaType
    title: str
    overview: str
    year: Optional[int] = None
    genres: List[str] = field(default_factory=list)
    score: Optional[float] = None
    total_episodes: Optional[int] = None
    total_chapters: Optional[int] = None
    progress_episodes: int = 0
    progress_chapters: int = 0
    status: MediaStatus = "planned"
    added_date: str = field(default_factory=lambda: datetime.now().isoformat())
    poster_url: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MediaItem':
        return cls(**data)

@dataclass
class UserPreferences:
    favorite_genres: List[str] = field(default_factory=list)
    liked_items: List[str] = field(default_factory=list)
    disliked_items: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ConversationMessage:
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())