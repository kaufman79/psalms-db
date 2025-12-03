"""
Database initialization and session management.
"""
from sqlmodel import create_engine, SQLModel, Session, select
from typing import Generator, List, Optional
from pathlib import Path
from models import Psalm, Genre, PsalmGenre, GreekText, PsalmNumberAlignment

# Database path
DB_PATH = Path(__file__).parent / "psalms.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create engine with echo for debugging (set to False in production)
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    """Initialize the database and create all tables"""
    SQLModel.metadata.create_all(engine)
    print(f"✓ Database initialized at {DB_PATH}")


def get_session() -> Generator[Session, None, None]:
    """Get a database session (for dependency injection)"""
    with Session(engine) as session:
        yield session


def get_or_create_genre(session: Session, genre_name: str) -> Genre:
    """Get existing genre or create new one"""
    genre = session.exec(select(Genre).where(Genre.name == genre_name)).first()
    if not genre:
        genre = Genre(name=genre_name)
        session.add(genre)
        session.commit()
        session.refresh(genre)
    return genre


def add_psalm_with_genres(
    session: Session,
    psalm_data: dict,
    genre_names: List[str]
) -> Psalm:
    """
    Add a psalm with associated genres.

    Args:
        session: Database session
        psalm_data: Dictionary with psalm fields
        genre_names: List of genre names to associate

    Returns:
        Created Psalm object
    """
    # Create psalm
    psalm = Psalm(**psalm_data)
    session.add(psalm)
    session.flush()  # Get the psalm ID

    # Add genres
    for genre_name in genre_names:
        genre = get_or_create_genre(session, genre_name)
        psalm_genre = PsalmGenre(psalm_id=psalm.id, genre_id=genre.id)
        session.add(psalm_genre)

    session.commit()
    session.refresh(psalm)
    return psalm


def search_psalms(
    session: Session,
    search_query: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    acrostic: Optional[str] = None,
    has_nt_quotation: Optional[bool] = None,
    musical_term: Optional[str] = None
) -> List[Psalm]:
    """
    Search and filter psalms with multiple criteria.

    Args:
        session: Database session
        search_query: Full-text search string
        author: Filter by author attribution
        genre: Filter by genre name
        acrostic: Filter by acrostic (Yes/No/Partial)
        has_nt_quotation: Filter psalms with NT quotations
        musical_term: Filter by musical/liturgical term

    Returns:
        List of matching Psalm objects
    """
    statement = select(Psalm).order_by(Psalm.psalm_number)

    # Text search across multiple fields
    if search_query:
        search_pattern = f"%{search_query}%"
        statement = statement.where(
            (Psalm.hebrew_heading.like(search_pattern)) |
            (Psalm.english_heading_translation.like(search_pattern)) |
            (Psalm.notes.like(search_pattern)) |
            (Psalm.key_themes.like(search_pattern)) |
            (Psalm.nt_quotations.like(search_pattern))
        )

    # Author filter
    if author and author != "All":
        statement = statement.where(Psalm.author_attribution == author)

    # Acrostic filter
    if acrostic and acrostic != "All":
        statement = statement.where(Psalm.acrostic == acrostic)

    # NT quotation filter
    if has_nt_quotation is not None:
        if has_nt_quotation:
            statement = statement.where(Psalm.nt_quotations.isnot(None))
            statement = statement.where(Psalm.nt_quotations != "")
        else:
            statement = statement.where(
                (Psalm.nt_quotations.is_(None)) |
                (Psalm.nt_quotations == "")
            )

    # Musical term filter
    if musical_term and musical_term != "All":
        statement = statement.where(
            Psalm.musical_liturgical_terms.like(f"%{musical_term}%")
        )

    results = session.exec(statement).all()

    # Genre filter (requires join)
    if genre and genre != "All":
        filtered_results = []
        for psalm in results:
            if genre in psalm.genres:
                filtered_results.append(psalm)
        return filtered_results

    return list(results)


def get_all_authors(session: Session) -> List[str]:
    """Get unique list of all authors"""
    psalms = session.exec(select(Psalm)).all()
    authors = set(p.author_attribution for p in psalms if p.author_attribution)
    return sorted(list(authors))


def get_all_genres(session: Session) -> List[str]:
    """Get all genre names"""
    genres = session.exec(select(Genre)).all()
    return sorted([g.name for g in genres])


def get_all_musical_terms(session: Session) -> List[str]:
    """Get unique musical/liturgical terms"""
    psalms = session.exec(select(Psalm)).all()
    terms = set()
    for psalm in psalms:
        if psalm.musical_liturgical_terms:
            terms.update(psalm.musical_terms_list)
    return sorted(list(terms))


def get_statistics(session: Session) -> dict:
    """Generate database statistics"""
    psalms = session.exec(select(Psalm)).all()

    # Count by author
    author_counts = {}
    for psalm in psalms:
        author = psalm.author_attribution or "Anonymous"
        author_counts[author] = author_counts.get(author, 0) + 1

    # Count by genre
    genre_counts = {}
    for psalm in psalms:
        for genre in psalm.genres:
            genre_counts[genre] = genre_counts.get(genre, 0) + 1

    # Count acrostics
    acrostic_counts = {"Yes": 0, "No": 0, "Partial": 0}
    for psalm in psalms:
        acrostic_counts[psalm.acrostic] = acrostic_counts.get(psalm.acrostic, 0) + 1

    # Count NT quotations
    nt_quotation_count = sum(1 for p in psalms if p.has_nt_quotation)

    # Selah statistics
    total_selah = sum(p.selah_count for p in psalms)
    psalms_with_selah = sum(1 for p in psalms if p.selah_count > 0)

    return {
        "total_psalms": len(psalms),
        "author_counts": author_counts,
        "genre_counts": genre_counts,
        "acrostic_counts": acrostic_counts,
        "nt_quotation_count": nt_quotation_count,
        "total_selah": total_selah,
        "psalms_with_selah": psalms_with_selah,
    }


# ========================================
# Greek Text (LXX) Functions
# ========================================

def add_greek_text(
    session: Session,
    mt_psalm_id: int,
    lxx_psalm_number: str,
    greek_data: dict
) -> GreekText:
    """
    Add Greek (LXX) text data for a psalm.

    Args:
        session: Database session
        mt_psalm_id: ID of the MT psalm
        lxx_psalm_number: LXX psalm number (can be compound like "114/115")
        greek_data: Dictionary with Greek text fields

    Returns:
        Created GreekText object
    """
    greek_text = GreekText(
        mt_psalm_id=mt_psalm_id,
        lxx_psalm_number=lxx_psalm_number,
        **greek_data
    )
    session.add(greek_text)
    session.commit()
    session.refresh(greek_text)
    return greek_text


def get_greek_text(session: Session, mt_psalm_id: int) -> Optional[GreekText]:
    """Get Greek text for a given MT psalm ID"""
    return session.exec(
        select(GreekText).where(GreekText.mt_psalm_id == mt_psalm_id)
    ).first()


def get_lxx_statistics(session: Session) -> dict:
    """
    Generate statistics comparing MT and LXX.

    Returns dict with:
        - psalms_with_greek_text: Number of psalms with LXX data
        - heading_agreements: Number where heading agrees
        - heading_differences: Number where heading differs
        - davidic_in_mt_only: Davidic attribution in MT but not LXX
        - davidic_in_lxx_only: Davidic attribution in LXX but not MT
        - davidic_in_both: Davidic in both
    """
    psalms = session.exec(select(Psalm)).all()
    greek_texts = session.exec(select(GreekText)).all()

    heading_agreements = sum(1 for gt in greek_texts if gt.heading_agrees_with_mt)
    heading_differences = sum(1 for gt in greek_texts if not gt.heading_agrees_with_mt)

    # Count Davidic attributions
    davidic_in_both = 0
    davidic_in_mt_only = 0
    davidic_in_lxx_only = 0

    for psalm in psalms:
        mt_davidic = psalm.author_attribution == "David"
        greek_text = get_greek_text(session, psalm.id)

        if greek_text:
            lxx_davidic = greek_text.davidic_attribution_lxx

            if mt_davidic and lxx_davidic:
                davidic_in_both += 1
            elif mt_davidic and not lxx_davidic:
                davidic_in_mt_only += 1
            elif not mt_davidic and lxx_davidic:
                davidic_in_lxx_only += 1

    return {
        "psalms_with_greek_text": len(greek_texts),
        "heading_agreements": heading_agreements,
        "heading_differences": heading_differences,
        "davidic_in_both": davidic_in_both,
        "davidic_in_mt_only": davidic_in_mt_only,
        "davidic_in_lxx_only": davidic_in_lxx_only,
        "total_davidic_mt": davidic_in_both + davidic_in_mt_only,
        "total_davidic_lxx": davidic_in_both + davidic_in_lxx_only,
    }


def seed_alignment_table(session: Session):
    """
    Populate the psalm_number_alignments table with all 150 MT psalms.
    This should be called once during database initialization.
    """
    from lxx_alignment import get_all_alignments

    # Check if already populated
    existing = session.exec(select(PsalmNumberAlignment)).first()
    if existing:
        return

    alignments = get_all_alignments()
    for mt_num, lxx_num, alignment_type, notes in alignments:
        alignment = PsalmNumberAlignment(
            mt_psalm_number=mt_num,
            lxx_psalm_number=lxx_num,
            alignment_type=alignment_type,
            notes=notes
        )
        session.add(alignment)

    session.commit()
    print(f"✓ Seeded {len(alignments)} psalm number alignments")
