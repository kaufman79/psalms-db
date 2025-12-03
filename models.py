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
    greek_texts: List["GreekText"] = Relationship(back_populates="psalm")
    textual_witnesses: List["TextualWitness"] = Relationship(back_populates="psalm")

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

    @property
    def lxx_psalm_number(self) -> Optional[str]:
        """Get LXX psalm number(s) for this MT psalm"""
        if self.greek_texts:
            return self.greek_texts[0].lxx_psalm_number
        return None

    @property
    def has_greek_text(self) -> bool:
        """Check if psalm has Greek text data"""
        return len(self.greek_texts) > 0


class GreekText(SQLModel, table=True):
    """Greek (LXX) text data for Psalms - Rahlfs-Hanhart edition"""
    __tablename__ = "greek_texts"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Edition info
    edition: str = Field(default="Rahlfs-Hanhart", index=True)

    # LXX numbering (can be compound like "9", "114/115", "146/147")
    lxx_psalm_number: str = Field(index=True)

    # Link to Hebrew/MT psalm
    mt_psalm_id: int = Field(foreign_key="psalms.id", index=True)

    # Greek superscription
    greek_heading: Optional[str] = Field(default=None)
    english_translation_heading: Optional[str] = Field(default=None)

    # Comparison with MT
    heading_agrees_with_mt: bool = Field(default=True)
    heading_differences_note: Optional[str] = Field(default=None)

    # LXX-specific attribution and notes
    davidic_attribution_lxx: bool = Field(default=False)
    author_attribution_lxx: Optional[str] = Field(default=None)
    historical_note_lxx: Optional[str] = Field(default=None)
    musical_terms_lxx: Optional[str] = Field(default=None)

    # Additional scholarly notes
    manuscript_notes: Optional[str] = Field(default=None)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    psalm: Psalm = Relationship(back_populates="greek_texts")


class PsalmNumberAlignment(SQLModel, table=True):
    """Mapping table between MT and LXX psalm numbering systems"""
    __tablename__ = "psalm_number_alignments"

    id: Optional[int] = Field(default=None, primary_key=True)
    mt_psalm_number: int = Field(unique=True, index=True)
    lxx_psalm_number: str = Field(index=True)
    alignment_type: str = Field(index=True)  # "exact", "combined", "split", "offset"
    notes: Optional[str] = Field(default=None)


class TextualWitness(SQLModel, table=True):
    """Textual witnesses for Psalms superscriptions (Vulgate, Peshitta, Targum, etc.)"""
    __tablename__ = "textual_witnesses"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Witness identification
    tradition: str = Field(index=True)  # "Vulgate", "Peshitta", "Targum"
    language: str = Field(index=True)  # "Latin", "Syriac", "Aramaic"
    edition: Optional[str] = Field(default=None)  # e.g., "Nova Vulgata", "Leiden"

    # Link to MT psalm
    mt_psalm_id: int = Field(foreign_key="psalms.id", index=True)
    mt_psalm_number: int = Field(index=True)

    # Superscription in original language
    original_text: Optional[str] = Field(default=None)
    english_translation: Optional[str] = Field(default=None)

    # Authorship attribution
    has_author_attribution: bool = Field(default=False)
    author_attribution: Optional[str] = Field(default=None)
    davidic_attribution: bool = Field(default=False)

    # Musical/liturgical terms
    musical_terms: Optional[str] = Field(default=None)

    # Historical superscription
    historical_note: Optional[str] = Field(default=None)

    # Genre/type designation
    genre_designation: Optional[str] = Field(default=None)

    # Comparison with MT
    agrees_with_mt: bool = Field(default=True)
    differences_from_mt: Optional[str] = Field(default=None)

    # Text-critical notes
    textual_notes: Optional[str] = Field(default=None)
    scholarly_significance: Optional[str] = Field(default=None)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    psalm: Psalm = Relationship(back_populates="textual_witnesses")
