"""
Book of Psalms Database - Streamlit Web Application

A scholarly tool for browsing, searching, and analyzing the 150 Psalms.
"""
import streamlit as st
import pandas as pd
from sqlmodel import Session, select
from typing import List
import io

from database import (
    engine, init_db, search_psalms, get_all_authors,
    get_all_genres, get_all_musical_terms, get_statistics,
    get_greek_text, get_lxx_statistics, get_textual_witnesses,
    get_witness_statistics
)
from models import Psalm, GreekText, TextualWitness
from lxx_alignment import format_dual_number


# Page configuration
st.set_page_config(
    page_title="Book of Psalms Database",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling and Hebrew RTL support
st.markdown("""
    <style>
    .hebrew-text {
        direction: rtl;
        font-size: 1.3em;
        font-family: 'Times New Roman', 'SBL Hebrew', serif;
        color: #1e3a8a;
        line-height: 1.8;
    }
    .greek-text {
        direction: ltr;
        font-size: 1.2em;
        font-family: 'Times New Roman', 'Galatia SIL', 'Gentium', serif;
        color: #047857;
        line-height: 1.8;
    }
    .latin-text {
        direction: ltr;
        font-size: 1.2em;
        font-family: 'Times New Roman', 'Palatino Linotype', serif;
        color: #92400e;
        line-height: 1.8;
        font-style: italic;
    }
    .comparison-box {
        background-color: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    .diff-box {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    .psalm-card {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.25rem;
    }
    .stat-box {
        background-color: #eff6ff;
        padding: 1.5rem;
        border-radius: 0.5rem;
        text-align: center;
        border: 1px solid #bfdbfe;
    }
    .genre-badge {
        background-color: #dbeafe;
        color: #1e40af;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        margin: 0.25rem;
        display: inline-block;
    }
    .section-header {
        color: #1e40af;
        border-bottom: 2px solid #3b82f6;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .lxx-number {
        color: #059669;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)


def initialize_database():
    """Initialize database on first run"""
    init_db()


def format_genres(genres: List[str]) -> str:
    """Format genre list as HTML badges"""
    if not genres:
        return ""
    badges = "".join([f'<span class="genre-badge">{g}</span>' for g in genres])
    return badges


def create_dataframe(psalms: List[Psalm], include_greek: bool = True) -> pd.DataFrame:
    """Convert psalm list to pandas DataFrame for display and export"""
    data = []

    with Session(engine) as session:
        for psalm in psalms:
            row = {
                "MT Psalm": psalm.psalm_number,
                "Author (MT)": psalm.author_attribution or "Anonymous",
                "Genres": ", ".join(psalm.genres) if psalm.genres else "",
                "Acrostic": psalm.acrostic,
                "Hebrew Heading": psalm.hebrew_heading or "",
                "English Heading (MT)": psalm.english_heading_translation or "",
                "Key Themes": psalm.key_themes or "",
                "NT Quotations": "Yes" if psalm.has_nt_quotation else "No",
                "Selah Count": psalm.selah_count,
                "Musical Terms (MT)": psalm.musical_liturgical_terms or "",
            }

            # Add Greek text data if available
            if include_greek:
                greek_text = get_greek_text(session, psalm.id)
                if greek_text:
                    row["LXX Psalm"] = greek_text.lxx_psalm_number
                    row["Greek Heading"] = greek_text.greek_heading or ""
                    row["English Heading (LXX)"] = greek_text.english_translation_heading or ""
                    row["Heading Agrees"] = "Yes" if greek_text.heading_agrees_with_mt else "No"
                    row["Author (LXX)"] = greek_text.author_attribution_lxx or ""
                    row["Davidic (LXX)"] = "Yes" if greek_text.davidic_attribution_lxx else "No"
                else:
                    row["LXX Psalm"] = ""
                    row["Greek Heading"] = ""
                    row["English Heading (LXX)"] = ""
                    row["Heading Agrees"] = ""
                    row["Author (LXX)"] = ""
                    row["Davidic (LXX)"] = ""

            data.append(row)

    return pd.DataFrame(data)


def display_psalm_card(psalm: Psalm):
    """Display a psalm as a clickable card"""
    with st.container():
        col1, col2, col3 = st.columns([1, 5, 2])

        with col1:
            # Show dual numbering if LXX data available
            if psalm.lxx_psalm_number:
                st.markdown(f"### {psalm.psalm_number}")
                st.markdown(f'<span class="lxx-number">LXX {psalm.lxx_psalm_number}</span>', unsafe_allow_html=True)
            else:
                st.markdown(f"### {psalm.psalm_number}")

        with col2:
            st.markdown(f"**{psalm.author_attribution or 'Anonymous'}**")
            if psalm.genres:
                st.markdown(format_genres(psalm.genres), unsafe_allow_html=True)

        with col3:
            if st.button("View Details →", key=f"btn_{psalm.id}"):
                st.session_state.selected_psalm = psalm.psalm_number
                st.session_state.page = "detail"
                st.rerun()

        if psalm.key_themes:
            st.caption(f"🏷️ {psalm.key_themes[:100]}...")

        st.markdown("---")


def main_page():
    """Main browse and search page"""
    st.title("📖 Book of Psalms Database")
    st.markdown("*A scholarly tool for exploring all 150 Psalms*")
    st.markdown("")

    # Sidebar filters
    st.sidebar.header("🔍 Search & Filter")

    # Text search
    search_query = st.sidebar.text_input(
        "Search text",
        placeholder="Search Hebrew, English, themes, notes..."
    )

    # Author filter
    with Session(engine) as session:
        authors = ["All"] + get_all_authors(session)
        author_filter = st.sidebar.selectbox("Author", authors)

        # Genre filter
        genres = ["All"] + get_all_genres(session)
        genre_filter = st.sidebar.selectbox("Genre", genres)

        # Musical terms filter
        musical_terms = ["All"] + get_all_musical_terms(session)
        musical_filter = st.sidebar.selectbox("Musical/Liturgical Term", musical_terms)

    # Acrostic filter
    acrostic_filter = st.sidebar.selectbox("Acrostic", ["All", "Yes", "No", "Partial"])

    # NT quotation filter
    nt_options = {
        "All": None,
        "Has NT Quotations": True,
        "No NT Quotations": False
    }
    nt_filter_label = st.sidebar.selectbox("NT Quotations", list(nt_options.keys()))
    nt_filter = nt_options[nt_filter_label]

    st.sidebar.markdown("---")

    # Clear filters button
    if st.sidebar.button("🔄 Clear All Filters"):
        st.rerun()

    # Perform search
    with Session(engine) as session:
        results = search_psalms(
            session,
            search_query=search_query if search_query else None,
            author=author_filter if author_filter != "All" else None,
            genre=genre_filter if genre_filter != "All" else None,
            acrostic=acrostic_filter if acrostic_filter != "All" else None,
            has_nt_quotation=nt_filter,
            musical_term=musical_filter if musical_filter != "All" else None
        )

    # Display results
    st.markdown(f"### Found {len(results)} Psalms")

    # Export buttons
    if results:
        col1, col2, col3 = st.columns([2, 1, 1])

        with col2:
            # CSV export
            df = create_dataframe(results)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export as CSV",
                data=csv,
                file_name="psalms_export.csv",
                mime="text/csv"
            )

        with col3:
            # Excel export
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Psalms')
            st.download_button(
                label="📥 Export as Excel",
                data=buffer.getvalue(),
                file_name="psalms_export.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    st.markdown("---")

    # Display results as cards
    if results:
        for psalm in results:
            display_psalm_card(psalm)
    else:
        st.info("No psalms found matching your criteria. Try adjusting your filters.")


def detail_page():
    """Detailed view of a single psalm"""
    if "selected_psalm" not in st.session_state:
        st.session_state.page = "main"
        st.rerun()
        return

    psalm_num = st.session_state.selected_psalm

    # Back button
    if st.button("← Back to Browse"):
        st.session_state.page = "main"
        st.rerun()

    # Load psalm
    with Session(engine) as session:
        psalm = session.exec(
            select(Psalm).where(Psalm.psalm_number == psalm_num)
        ).first()

        if not psalm:
            st.error("Psalm not found")
            return

        # Get Greek text if available
        greek_text = get_greek_text(session, psalm.id)

        # Get all textual witnesses
        witnesses = get_textual_witnesses(session, psalm.id)

        # Header with dual numbering
        if greek_text:
            st.title(f"Psalm {psalm.psalm_number} (LXX {greek_text.lxx_psalm_number})")
        else:
            st.title(f"Psalm {psalm.psalm_number}")

        # Hebrew heading (RTL)
        if psalm.hebrew_heading:
            st.markdown('<h3 class="section-header">📜 Hebrew Superscription (MT)</h3>', unsafe_allow_html=True)
            st.markdown(f'<div class="hebrew-text">{psalm.hebrew_heading}</div>', unsafe_allow_html=True)

        # English heading
        if psalm.english_heading_translation:
            st.markdown('<h3 class="section-header">English Translation of Hebrew Heading</h3>', unsafe_allow_html=True)
            st.info(psalm.english_heading_translation)

        # Greek (LXX) superscription section
        if greek_text:
            st.markdown("---")
            st.markdown('<h3 class="section-header">🏛️ Greek Superscription (LXX - Rahlfs-Hanhart)</h3>', unsafe_allow_html=True)

            if greek_text.greek_heading:
                st.markdown(f'<div class="greek-text">{greek_text.greek_heading}</div>', unsafe_allow_html=True)

                if greek_text.english_translation_heading:
                    st.caption(f"*Translation: {greek_text.english_translation_heading}*")

                # Show agreement/difference indicator
                if greek_text.heading_agrees_with_mt:
                    st.markdown('<div class="comparison-box">✅ <strong>Heading agrees with Hebrew</strong></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="diff-box">⚠️ <strong>Heading differs from Hebrew</strong></div>', unsafe_allow_html=True)
                    if greek_text.heading_differences_note:
                        st.info(f"**Note:** {greek_text.heading_differences_note}")

                # Show Davidic attribution comparison if different
                mt_davidic = psalm.author_attribution == "David"
                lxx_davidic = greek_text.davidic_attribution_lxx

                if mt_davidic != lxx_davidic:
                    st.markdown("#### Attribution Comparison")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**MT:** {'✅ Davidic' if mt_davidic else '❌ Not Davidic'}")
                    with col2:
                        st.markdown(f"**LXX:** {'✅ Davidic' if lxx_davidic else '❌ Not Davidic'}")
            else:
                st.caption("*No superscription in LXX*")

        # Textual Witnesses section (Vulgate, Peshitta, Targum, etc.)
        if witnesses:
            st.markdown("---")
            st.markdown('<h3 class="section-header">📚 Other Ancient Witnesses</h3>', unsafe_allow_html=True)

            for witness in witnesses:
                # Icon and label based on tradition
                tradition_icons = {
                    "Vulgate": "🇻🇦",
                    "Peshitta": "🇸🇾",
                    "Targum": "🕍",
                }
                icon = tradition_icons.get(witness.tradition, "📜")

                st.markdown(f"#### {icon} {witness.tradition} ({witness.language})")

                if witness.edition:
                    st.caption(f"*Edition: {witness.edition}*")

                if witness.original_text:
                    # Display original text based on language
                    if witness.language == "Latin":
                        st.markdown(f'<div class="latin-text">{witness.original_text}</div>', unsafe_allow_html=True)
                    elif witness.language == "Greek":
                        st.markdown(f'<div class="greek-text">{witness.original_text}</div>', unsafe_allow_html=True)
                    elif witness.language in ["Syriac", "Aramaic"]:
                        # For Syriac/Aramaic, just display as normal text (could be RTL if needed)
                        st.markdown(f'<div style="font-size: 1.2em; line-height: 1.8;">{witness.original_text}</div>', unsafe_allow_html=True)
                    else:
                        st.write(witness.original_text)

                    if witness.english_translation:
                        st.caption(f"*Translation: {witness.english_translation}*")

                    # Show agreement/difference indicator
                    if witness.agrees_with_mt:
                        st.markdown('<div class="comparison-box">✅ <strong>Agrees with MT</strong></div>', unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="diff-box">⚠️ <strong>Differs from MT</strong></div>', unsafe_allow_html=True)
                        if witness.differences_from_mt:
                            st.info(f"**Differences:** {witness.differences_from_mt}")

                    # Show authorship comparison if different
                    if witness.author_attribution:
                        mt_author = psalm.author_attribution
                        witness_author = witness.author_attribution

                        if mt_author != witness_author:
                            st.markdown(f"**Attribution:** {witness_author} (MT: {mt_author or 'None'})")

                    # Show musical terms if present
                    if witness.musical_terms:
                        st.markdown(f"**Musical/Liturgical Terms:** {witness.musical_terms}")

                    # Show historical note if present
                    if witness.historical_note:
                        st.markdown(f"**Historical Context:** {witness.historical_note}")

                    # Show textual notes if present
                    if witness.textual_notes:
                        with st.expander("📝 Text-Critical Notes"):
                            st.write(witness.textual_notes)
                else:
                    st.caption("*No superscription in this witness*")

                st.markdown("")  # Spacing

        # Metadata columns
        st.markdown('<h3 class="section-header">Metadata</h3>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Author Attribution**")
            st.write(psalm.author_attribution or "Anonymous")

            st.markdown("**Acrostic**")
            st.write(psalm.acrostic)

        with col2:
            st.markdown("**Genres**")
            if psalm.genres:
                st.markdown(format_genres(psalm.genres), unsafe_allow_html=True)
            else:
                st.write("—")

            st.markdown("**Selah Count**")
            st.write(f"סֶלָה appears {psalm.selah_count} time(s)")

        with col3:
            st.markdown("**NT Quotations**")
            st.write("Yes" if psalm.has_nt_quotation else "No")

        # Musical/Liturgical Terms
        if psalm.musical_liturgical_terms:
            st.markdown('<h3 class="section-header">Musical & Liturgical Terms</h3>', unsafe_allow_html=True)
            terms_html = "".join([f'<span class="genre-badge">{term}</span>' for term in psalm.musical_terms_list])
            st.markdown(terms_html, unsafe_allow_html=True)

        # Historical superscription
        if psalm.historical_superscription:
            st.markdown('<h3 class="section-header">Historical Context</h3>', unsafe_allow_html=True)
            st.write(psalm.historical_superscription)

        # Key themes
        if psalm.key_themes:
            st.markdown('<h3 class="section-header">Key Themes</h3>', unsafe_allow_html=True)
            st.write(psalm.key_themes)

        # NT Quotations detail
        if psalm.nt_quotations:
            st.markdown('<h3 class="section-header">New Testament Quotations</h3>', unsafe_allow_html=True)
            st.write(psalm.nt_quotations)

        # Scholarly notes
        if psalm.notes:
            st.markdown('<h3 class="section-header">Scholarly Notes</h3>', unsafe_allow_html=True)
            st.write(psalm.notes)

        # Timestamps
        st.markdown("---")
        st.caption(f"Added: {psalm.created_at.strftime('%Y-%m-%d')} | Updated: {psalm.updated_at.strftime('%Y-%m-%d')}")


def statistics_page():
    """Statistics and visualizations page"""
    st.title("📊 Psalms Statistics")
    st.markdown("*Insights and analysis across all 150 Psalms*")
    st.markdown("")

    with Session(engine) as session:
        stats = get_statistics(session)

        # Overview stats
        st.markdown("## Overview")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("Total Psalms", stats["total_psalms"])
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("NT Quotations", stats["nt_quotation_count"])
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("Total Selah", stats["total_selah"])
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("Psalms with Selah", stats["psalms_with_selah"])
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Authors distribution
        st.markdown("## Distribution by Author")
        author_df = pd.DataFrame(
            list(stats["author_counts"].items()),
            columns=["Author", "Count"]
        ).sort_values("Count", ascending=False)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.bar_chart(author_df.set_index("Author"))

        with col2:
            st.dataframe(author_df, hide_index=True, use_container_width=True)

        st.markdown("---")

        # Genre distribution
        st.markdown("## Distribution by Genre")
        genre_df = pd.DataFrame(
            list(stats["genre_counts"].items()),
            columns=["Genre", "Count"]
        ).sort_values("Count", ascending=False)

        col1, col2 = st.columns([2, 1])

        with col1:
            st.bar_chart(genre_df.set_index("Genre"))

        with col2:
            st.dataframe(genre_df, hide_index=True, use_container_width=True)

        st.markdown("---")

        # Acrostic distribution
        st.markdown("## Acrostic Psalms")
        acrostic_df = pd.DataFrame(
            list(stats["acrostic_counts"].items()),
            columns=["Acrostic", "Count"]
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            st.bar_chart(acrostic_df.set_index("Acrostic"))

        with col2:
            st.dataframe(acrostic_df, hide_index=True, use_container_width=True)

        st.markdown("---")

        # LXX Comparison Statistics
        st.markdown("## Hebrew (MT) vs Greek (LXX) Comparison")
        lxx_stats = get_lxx_statistics(session)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("Davidic (MT)", lxx_stats.get("total_davidic_mt", 0))
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("Davidic (LXX)", lxx_stats.get("total_davidic_lxx", 0))
            st.markdown('</div>', unsafe_allow_html=True)

        with col3:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("Headings Agree", lxx_stats.get("heading_agreements", 0))
            st.markdown('</div>', unsafe_allow_html=True)

        with col4:
            st.markdown('<div class="stat-box">', unsafe_allow_html=True)
            st.metric("Headings Differ", lxx_stats.get("heading_differences", 0))
            st.markdown('</div>', unsafe_allow_html=True)

        # Davidic attribution comparison chart
        st.markdown("### Davidic Attribution Differences")
        col1, col2 = st.columns([2, 1])

        with col1:
            davidic_comparison = pd.DataFrame({
                "Category": ["Both MT & LXX", "MT Only", "LXX Only"],
                "Count": [
                    lxx_stats.get("davidic_in_both", 0),
                    lxx_stats.get("davidic_in_mt_only", 0),
                    lxx_stats.get("davidic_in_lxx_only", 0)
                ]
            })
            st.bar_chart(davidic_comparison.set_index("Category"))

        with col2:
            st.dataframe(davidic_comparison, hide_index=True, use_container_width=True)
            st.caption(f"LXX adds David to {lxx_stats.get('davidic_in_lxx_only', 0)} additional psalms")

        st.markdown("---")

        # Textual Witness Statistics
        witness_stats = get_witness_statistics(session)

        if witness_stats["total_witnesses"] > 0:
            st.markdown("## Textual Witnesses Comparison")
            st.caption("*Ancient versions for text-critical analysis*")

            # Statistics by tradition
            traditions = witness_stats["traditions"]

            cols = st.columns(len(traditions))
            for idx, (tradition, stats) in enumerate(traditions.items()):
                with cols[idx]:
                    st.markdown('<div class="stat-box">', unsafe_allow_html=True)
                    st.markdown(f"### {tradition}")
                    st.metric("Total Psalms", stats["total"])
                    st.metric("With Superscription", stats["with_superscription"])
                    st.metric("Davidic", stats["davidic"])
                    st.markdown('</div>', unsafe_allow_html=True)

            # Detailed comparison table
            st.markdown("### Tradition Comparison")

            comparison_data = []
            for tradition, stats in traditions.items():
                comparison_data.append({
                    "Tradition": tradition,
                    "Total": stats["total"],
                    "With Superscription": stats["with_superscription"],
                    "Davidic": stats["davidic"],
                    "Agrees with MT": stats["agrees_with_mt"],
                    "Differs from MT": stats["differs_from_mt"],
                })

            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, hide_index=True, use_container_width=True)

            # Multi-witness Davidic comparison
            st.markdown("### Davidic Attribution Across Witnesses")

            davidic_data = {
                "MT": stats.get("author_counts", {}).get("David", 0),
                "LXX": lxx_stats.get("total_davidic_lxx", 0),
            }

            for tradition, stats in traditions.items():
                davidic_data[tradition] = stats["davidic"]

            davidic_df = pd.DataFrame(list(davidic_data.items()), columns=["Witness", "Davidic Psalms"])
            st.bar_chart(davidic_df.set_index("Witness"))

            st.markdown("---")

        # Interesting queries
        st.markdown("## Quick Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### Top Author-Genre Combinations")
            # Get laments by David
            david_laments = session.exec(
                select(Psalm).where(Psalm.author_attribution == "David")
            ).all()
            lament_count = sum(1 for p in david_laments if "Lament" in p.genres)

            st.write(f"**Davidic Laments:** {lament_count}")
            st.write(f"**Total Davidic Psalms:** {stats['author_counts'].get('David', 0)}")

        with col2:
            st.markdown("### Messianic Psalms")
            messianic = session.exec(select(Psalm)).all()
            messianic_count = sum(1 for p in messianic if "Messianic" in p.genres or "Royal" in p.genres)
            st.write(f"**Royal/Messianic Psalms:** {messianic_count}")


def main():
    """Main application router"""
    # Initialize database
    initialize_database()

    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "main"

    # Navigation
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Navigation")

    if st.sidebar.button("🏠 Browse Psalms", use_container_width=True):
        st.session_state.page = "main"
        st.rerun()

    if st.sidebar.button("📊 Statistics", use_container_width=True):
        st.session_state.page = "statistics"
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "**Book of Psalms Database** v2.0\n\n"
        "A scholarly tool for exploring the 150 Psalms with:\n\n"
        "• Hebrew (MT) & Greek (LXX) texts\n"
        "• Dual MT/LXX numbering\n"
        "• Genre classification\n"
        "• Authorship data (MT vs LXX)\n"
        "• New Testament quotations\n"
        "• Rahlfs-Hanhart Septuagint\n\n"
        "Built with Python, SQLModel, and Streamlit."
    )

    # Route to appropriate page
    if st.session_state.page == "main":
        main_page()
    elif st.session_state.page == "detail":
        detail_page()
    elif st.session_state.page == "statistics":
        statistics_page()


if __name__ == "__main__":
    main()
