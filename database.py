"""
Database initialization and session management.
"""
from sqlmodel import create_engine, SQLModel, Session, select
from typing import Generator, List, Optional
from pathlib import Path
from models import Psalm, Genre, PsalmGenre

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
