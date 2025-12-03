# 📖 Book of Psalms Database

A complete, scholarly tool for browsing, searching, and analyzing all 150 Psalms of the Hebrew Bible. Built with Python, SQLModel, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-green.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red.svg)

## 🌟 Features

### Core Functionality
- **Complete Database**: All 150 Psalms with scholarly metadata
- **Advanced Search**: Full-text search across Hebrew headings, English translations, themes, and notes
- **Multi-Filter System**: Filter by author, genre, musical terms, acrostic structure, and NT quotations
- **Detailed Views**: Rich detail pages with Hebrew text displayed right-to-left
- **Data Export**: Export search results as CSV or Excel with one click
- **Statistics Dashboard**: Visual insights with charts and distribution analysis

### Scholarly Features
- **Hebrew Superscriptions**: Original Hebrew text (לַמְנַצֵּחַ, מִזְמוֹר, etc.)
- **Genre Classification**: Lament, Praise, Royal, Wisdom, Torah, and more
- **Authorship Data**: David, Asaph, Sons of Korah, Moses, Anonymous, etc.
- **Musical Terms**: Liturgical and musical terminology preserved
- **Acrostic Identification**: Yes/No/Partial classification
- **NT Quotations**: Track where Psalms are quoted in the New Testament
- **Selah Counting**: Automatic counting of סֶלָה occurrences

### Data Quality
- **First 20 Psalms**: Complete, accurate scholarly data with Hebrew text, genres, themes, and NT references
- **Remaining Psalms (21-150)**: Basic metadata with genre and authorship (ready for enrichment)

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Installation

1. **Clone or download this repository**
```bash
git clone <your-repo-url>
cd psalms-db
```

2. **Install dependencies** (one command!)
```bash
pip install -r requirements.txt
```

3. **Initialize the database**
```bash
python seed.py
```

This will create `psalms.db` and populate it with all 150 Psalms.

4. **Run the application**
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

**That's it! You're ready to explore the Psalms.** ⏱️ *Total setup time: Under 2 minutes*

## 📁 Project Structure

```
psalms-db/
├── app.py              # Main Streamlit application
├── models.py           # SQLModel database models (Psalm, Genre, PsalmGenre)
├── database.py         # Database initialization, queries, and utilities
├── seed.py             # Database seeding script
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── psalms.db           # SQLite database (created after running seed.py)
```

## 🎯 Usage Guide

### Browse and Search

1. **Main Browse Page**: View all 150 Psalms as cards
2. **Search Box**: Enter keywords to search Hebrew headings, English translations, themes, and notes
3. **Filters**: Use sidebar filters to narrow results:
   - Author (David, Asaph, etc.)
   - Genre (Lament, Praise, etc.)
   - Musical Terms
   - Acrostic (Yes/No/Partial)
   - NT Quotations (Has/Doesn't have)

### View Details

Click **"View Details →"** on any psalm card to see:
- Hebrew superscription (right-to-left display)
- English translation of heading
- Complete metadata (author, genres, acrostic status)
- Musical and liturgical terms
- Historical context (if applicable)
- Key themes and theological content
- New Testament quotations with verse references
- Scholarly notes
- Selah count

### Export Data

From the browse page:
1. Apply your desired filters
2. Click **"📥 Export as CSV"** or **"📥 Export as Excel"**
3. Save the file with all visible psalm data

### View Statistics

Navigate to **📊 Statistics** to see:
- Distribution of psalms by author (with charts)
- Distribution by genre
- Acrostic psalm counts
- Quick insights (e.g., "How many Davidic laments?")
- Messianic/Royal psalm counts
- Selah usage statistics

## 🗄️ Database Schema

### Tables

#### `psalms`
Main psalm data with all scholarly metadata:
- `psalm_number` (1-150)
- `hebrew_heading` (Hebrew superscription text)
- `english_heading_translation`
- `author_attribution` (David, Asaph, etc.)
- `musical_liturgical_terms` (comma-separated)
- `acrostic` (Yes/No/Partial)
- `historical_superscription` (context note)
- `key_themes` (theological content)
- `nt_quotations` (NT verse references)
- `notes` (scholarly commentary)
- `selah_count` (number of סֶלָה occurrences)

#### `genres`
Genre/category lookup table:
- `id`, `name`, `description`

#### `psalm_genres`
Many-to-many junction table linking psalms to genres

## 🎓 Scholarly Notes

### Data Sources
The first 20 psalms contain accurate data based on:
- Hebrew Masoretic Text superscriptions
- Academic genre classifications
- Historical-critical scholarship
- NT quotation tracking

### Genre Classifications
- **Lament**: Individual or communal expressions of distress
- **Praise/Hymn**: Celebration of God's character and acts
- **Thanksgiving**: Gratitude for deliverance
- **Royal**: Concerning the king or Davidic covenant
- **Wisdom**: Ethical instruction and reflection
- **Trust/Confidence**: Expression of faith in God
- **Torah Psalm**: Meditation on God's law
- **Pilgrimage**: Songs of Ascents (120-134)
- **Messianic**: Royal psalms with messianic interpretation

### Musical Terms Explained
- **לַמְנַצֵּחַ** (lamnatseach): "To the choirmaster"
- **מִזְמוֹר** (mizmor): "Psalm" (song with instrumental accompaniment)
- **שִׁיר** (shir): "Song"
- **תְּפִלָּה** (tefillah): "Prayer"
- **בִּנְגִינוֹת** (bineginot): "With stringed instruments"
- **עַל־הַגִּתִּית** (al-hagittit): "According to The Gittith" (perhaps tune name)
- **סֶלָה** (selah): Liturgical/musical notation (meaning uncertain)

## 🛠️ Customization

### Adding More Data

To enrich psalms 21-150 with detailed data:

1. Edit `seed.py` and add entries to the `detailed_psalms` list
2. Delete `psalms.db`
3. Run `python seed.py` again

### Modifying the Schema

1. Update `models.py` with new fields
2. Delete `psalms.db`
3. Run `python seed.py`

## 📊 Technology Stack

- **Python 3.11+**: Core language
- **Streamlit**: Web framework for rapid UI development
- **SQLModel**: Modern ORM combining SQLAlchemy + Pydantic
- **SQLite**: Lightweight, file-based database
- **Pandas**: Data manipulation and export
- **OpenPyXL**: Excel file generation

## 🤝 Contributing

To contribute additional psalm data or features:

1. Fork the repository
2. Make your changes
3. Test thoroughly
4. Submit a pull request

Focus areas for contribution:
- Complete data for psalms 21-150
- Additional scholarly notes
- Improved genre classifications
- Historical context for superscriptions
- UI/UX improvements

## 📝 License

This project is provided as-is for educational and scholarly use.

Biblical text and scholarly metadata are in the public domain.

## 🙏 Acknowledgments

Built with passion for biblical scholarship and modern software development.

Special thanks to the Hebrew Bible scholarship community and open-source contributors.

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contribute improvements via pull request

---

**Built with ❤️ for Bible scholars, students, and enthusiasts**

*"Blessed is the one... whose delight is in the law of the LORD, and who meditates on his law day and night."* — Psalm 1:1-2
