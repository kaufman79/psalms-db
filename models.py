"""
Database models for the Book of Psalms Database.
Uses SQLModel for type-safe ORM with Pydantic validation.
"""
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime


class Genre(SQLModel, table=True):
    """Genre/category for Psalms (Lament, Praise, etc.)"""
    __tablename__ = "genres"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None

    # Relationship
    psalm_genres: List["PsalmGenre"] = Relationship(back_populates="genre")


class PsalmGenre(SQLModel, table=True):
    """Many-to-many junction table between Psalms and Genres"""
    __tablename__ = "psalm_genres"

    id: Optional[int] = Field(default=None, primary_key=True)
    psalm_id: int = Field(foreign_key="psalms.id")
    genre_id: int = Field(foreign_key="genres.id")

    # Relationships
    psalm: "Psalm" = Relationship(back_populates="psalm_genres")
    genre: Genre = Relationship(back_populates="psalm_genres")


class Psalm(SQLModel, table=True):
    """Main Psalm model with all scholarly metadata"""
    __tablename__ = "psalms"

    id: Optional[int] = Field(default=None, primary_key=True)
    psalm_number: int = Field(unique=True, index=True)

    # Hebrew and English headings
    hebrew_heading: Optional[str] = Field(default=None)
    english_heading_translation: Optional[str] = Field(default=None)

    # Authorship and attribution
    author_attribution: Optional[str] = Field(default=None, index=True)

    # Musical and liturgical terms (stored as comma-separated)
    musical_liturgical_terms: Optional[str] = Field(default=None)

    # Structural features
    acrostic: str = Field(default="No")  # Yes/No/Partial
    historical_superscription: Optional[str] = Field(default=None)

    # Content metadata
    key_themes: Optional[str] = Field(default=None)
    nt_quotations: Optional[str] = Field(default=None)
    notes: Optional[str] = Field(default=None)

    # Selah count
    selah_count: int = Field(default=0)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    psalm_genres: List[PsalmGenre] = Relationship(back_populates="psalm")

    @property
    def genres(self) -> List[str]:
        """Return list of genre names"""
        return [pg.genre.name for pg in self.psalm_genres]

    @property
    def has_nt_quotation(self) -> bool:
        """Check if psalm has NT quotations"""
        return bool(self.nt_quotations and self.nt_quotations.strip())

    @property
    def musical_terms_list(self) -> List[str]:
        """Return musical terms as list"""
        if not self.musical_liturgical_terms:
            return []
        return [term.strip() for term in self.musical_liturgical_terms.split(",")]
