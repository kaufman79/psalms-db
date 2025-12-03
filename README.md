# 📖 Book of Psalms Database v2.0

A complete, scholarly tool for browsing, searching, and analyzing all 150 Psalms with **both Hebrew (Masoretic Text) and Greek (Septuagint) traditions**. Built with Python, SQLModel, and Streamlit.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![SQLite](https://img.shields.io/badge/Database-SQLite-green.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red.svg)
![Version](https://img.shields.io/badge/Version-2.0-brightgreen.svg)

## 🌟 Features

### Core Functionality
- **Complete Database**: All 150 Psalms with scholarly metadata
- **Dual Text Traditions**: Hebrew (MT) and Greek (LXX) superscriptions side-by-side
- **MT-LXX Numbering Alignment**: Automatic conversion (e.g., Psalm 23 MT = Psalm 22 LXX)
- **Advanced Search**: Full-text search across Hebrew headings, Greek headings, English translations, themes, and notes
- **Multi-Filter System**: Filter by author, genre, musical terms, acrostic structure, and NT quotations
- **Detailed Views**: Rich detail pages with Hebrew (RTL) and Greek (LTR) text properly displayed
- **Data Export**: Export search results as CSV or Excel with MT and LXX data
- **Statistics Dashboard**: Visual insights with charts, distribution analysis, and MT-LXX comparison

### Scholarly Features

#### Hebrew (Masoretic Text)
- **Hebrew Superscriptions**: Original Hebrew text (לַמְנַצֵּחַ, מִזְמוֹר, etc.)
- **Genre Classification**: Lament, Praise, Royal, Wisdom, Torah, and more
- **Authorship Data**: David (67 psalms), Asaph, Sons of Korah, Moses, Solomon, Anonymous
- **Musical Terms**: Liturgical and musical terminology preserved
- **Acrostic Identification**: Yes/No/Partial classification (Pss 9-10, 25, 34, 37, 111, 112, 119, 145)
- **NT Quotations**: Track where Psalms are quoted in the New Testament
- **Selah Counting**: Automatic counting of סֶלָה occurrences

#### Greek (Septuagint - Rahlfs-Hanhart Edition)
- **Greek Superscriptions**: Complete Greek text for all 150 Psalms (ψαλμός, τῷ Δαυίδ, etc.)
- **LXX Numbering**: Different numbering system properly aligned with MT
- **Authorship Differences**: LXX attributes 77 psalms to David (10 more than MT!)
- **Heading Comparison**: 127 headings agree with MT, 23 differ
- **Attribution Tracking**: Visual indicators when MT and LXX differ
- **Scholarly Notes**: Explanations of differences between traditions

### MT-LXX Alignment System

The application handles all numbering differences automatically:

| Hebrew (MT) | Greek (LXX) | Type |
|-------------|-------------|------|
| Psalms 1-8 | Psalms 1-8 | Exact match |
| **Psalms 9-10** | **Psalm 9** | Combined in LXX |
| Psalms 11-113 | Psalms 10-112 | LXX = MT - 1 |
| **Psalms 114-115** | **Psalm 113** | Combined in LXX |
| **Psalm 116** | **Psalms 114-115** | Split in LXX |
| Psalms 117-146 | Psalms 116-145 | LXX = MT - 1 |
| **Psalm 147** | **Psalms 146-147** | Split in LXX |
| Psalms 148-150 | Psalms 148-150 | Exact match |

**Result:** The famous Shepherd's Psalm is **Psalm 23 (MT)** but **Psalm 22 (LXX)**

### Data Quality
- **First 20 Psalms**: Complete, accurate scholarly data with Hebrew text, Greek text, genres, themes, and NT references
- **Remaining Psalms (21-150)**: Comprehensive metadata with MT and LXX superscriptions
- **All 150 Psalms**: Complete Greek (LXX) superscriptions from Rahlfs-Hanhart edition
- **Alignment Table**: Complete MT↔LXX numbering mapping for all 150 psalms

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
# Seed Hebrew (MT) data
python seed.py

# Seed Greek (LXX) data and alignment tables
python seed_greek_texts.py
```

This will create `psalms.db` and populate it with all 150 Psalms in both traditions.

4. **Run the application**
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

**That's it! You're ready to explore the Psalms.** ⏱️ *Total setup time: Under 3 minutes*

## 📁 Project Structure

```
psalms-db/
├── app.py                          # Main Streamlit application with dual text display
├── models.py                       # SQLModel database models (Psalm, Genre, GreekText, etc.)
├── database.py                     # Database initialization, queries, and LXX utilities
├── seed.py                         # MT (Hebrew) database seeding script
├── seed_greek_texts.py             # LXX (Greek) database seeding script
├── lxx_alignment.py                # MT-LXX numbering conversion utilities
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── QUICKSTART.md                   # Quick setup guide
├── GREEK_TEXT_IMPLEMENTATION_PLAN.md  # Technical implementation documentation
└── psalms.db                       # SQLite database (created after running seed scripts)
```

## 🎯 Usage Guide

### Browse and Search

1. **Main Browse Page**: View all 150 Psalms as cards with dual MT/LXX numbering
2. **Search Box**: Enter keywords to search Hebrew headings, Greek headings, English translations, themes, and notes
3. **Filters**: Use sidebar filters to narrow results:
   - Author (David, Asaph, etc.)
   - Genre (Lament, Praise, etc.)
   - Musical Terms
   - Acrostic (Yes/No/Partial)
   - NT Quotations (Has/Doesn't have)

### View Details

Click **"View Details →"** on any psalm card to see:
- **Dual numbering**: "Psalm 23 (LXX 22)" in the title
- **Hebrew superscription** (right-to-left display with proper formatting)
- **English translation** of Hebrew heading
- **Greek superscription** (Rahlfs-Hanhart edition)
- **English translation** of Greek heading
- **Agreement indicator**: ✅ if headings agree, ⚠️ if they differ
- **Attribution comparison**: Visual comparison when MT and LXX differ
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
3. Save the file with all visible psalm data including:
   - MT Psalm number
   - LXX Psalm number
   - Hebrew heading
   - Greek heading
   - English translations (both MT and LXX)
   - Heading agreement status
   - Author attributions (both MT and LXX)
   - All other metadata

### View Statistics

Navigate to **📊 Statistics** to see:
- Distribution of psalms by author (with charts)
- Distribution by genre
- Acrostic psalm counts
- **MT vs LXX Comparison**:
  - Davidic attribution differences (67 in MT vs 77 in LXX)
  - Heading agreement statistics (127 agree, 23 differ)
  - Visual charts showing attribution overlap
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

#### `greek_texts`
Greek (LXX) superscription data for all 150 Psalms:
- `id`, `edition` (Rahlfs-Hanhart)
- `lxx_psalm_number` (can be compound like "114/115")
- `mt_psalm_id` (foreign key to psalms)
- `greek_heading` (Greek superscription text)
- `english_translation_heading` (English translation of Greek)
- `heading_agrees_with_mt` (boolean)
- `heading_differences_note` (explanation of differences)
- `davidic_attribution_lxx` (boolean)
- `author_attribution_lxx` (author in LXX)
- `historical_note_lxx`, `musical_terms_lxx`
- `manuscript_notes`

#### `psalm_number_alignments`
MT ↔ LXX numbering mapping for all 150 psalms:
- `mt_psalm_number` (1-150)
- `lxx_psalm_number` (can be compound)
- `alignment_type` (exact/combined/split/offset)
- `notes` (explanation of alignment)

#### `genres`
Genre/category lookup table:
- `id`, `name`, `description`

#### `psalm_genres`
Many-to-many junction table linking psalms to genres

## 🎓 Scholarly Notes

### Data Sources

**Hebrew (Masoretic Text):**
- Hebrew Masoretic Text superscriptions
- Academic genre classifications
- Historical-critical scholarship
- NT quotation tracking

**Greek (Septuagint):**
- Rahlfs-Hanhart edition (standard critical text)
- NETS (New English Translation of the Septuagint)
- Academic research on LXX-MT superscription differences
- Textual criticism and manuscript studies

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

**Hebrew Terms:**
- **לַמְנַצֵּחַ** (lamnatseach): "To the choirmaster"
- **מִזְמוֹר** (mizmor): "Psalm" (song with instrumental accompaniment)
- **שִׁיר** (shir): "Song"
- **תְּפִלָּה** (tefillah): "Prayer"
- **בִּנְגִינוֹת** (bineginot): "With stringed instruments"
- **עַל־הַגִּתִּית** (al-hagittit): "According to The Gittith" (perhaps tune name)
- **סֶלָה** (selah): Liturgical/musical notation (meaning uncertain)

**Greek Terms:**
- **ψαλμός** (psalmos): "Psalm"
- **τῷ Δαυίδ** (tō Dauid): "Of/to/for David"
- **ᾠδή** (ōdē): "Song/Ode"
- **εἰς τὸ τέλος** (eis to telos): "To the end" / "For the choirmaster"
- **Αλληλουια** (Allēlouia): "Hallelujah" / "Praise the LORD"
- **προσευχή** (proseuchē): "Prayer"

### Major MT-LXX Differences

#### Davidic Attribution Changes
**LXX adds David to 10 additional psalms:**
- Psalms 33, 43, 71, 91, 93-99, 104, 137

**LXX removes David from 4 psalms:**
- Psalms 122, 124, 131, 133

**Result:** 67 Davidic psalms in MT → 77 Davidic psalms in LXX

#### Psalm Numbering
The LXX numbering differs systematically from MT due to:
1. **Combining Psalms**: MT 9-10 → LXX 9, MT 114-115 → LXX 113
2. **Splitting Psalms**: MT 116 → LXX 114-115, MT 147 → LXX 146-147
3. **Resulting Offset**: Most psalms have LXX number = MT number - 1

This is why Orthodox and Catholic liturgies often use different psalm numbers than Protestant Bibles.

#### Historical Superscriptions
The LXX adds 14 historical superscriptions not found in MT, mostly in Book V. Examples:
- Psalm 71 (LXX): Adds reference to "sons of Jonadab and those first taken captive"
- Psalm 96 (LXX): "When the house was being built after the captivity"
- Psalms 146-148 (LXX): Attributes to "Haggai and Zechariah"

## 🛠️ Customization

### Adding More Detailed Data

To enrich any psalm with more detailed data:

1. Edit `seed.py` for Hebrew (MT) data:
   - Add entries to the `detailed_psalms` list
2. Edit `seed_greek_texts.py` for Greek (LXX) data:
   - Add entries to the `greek_data` list with full superscriptions
3. Delete `psalms.db`
4. Run both seed scripts again:
   ```bash
   python seed.py
   python seed_greek_texts.py
   ```

### Modifying the Schema

1. Update `models.py` with new fields
2. Delete `psalms.db`
3. Run both seed scripts

### Adding Additional LXX Editions

The system is designed to support multiple Greek text editions. To add Göttingen or manuscript variants:

1. Update `GreekText` model to specify edition
2. Add new entries in `seed_greek_texts.py` with `edition="Göttingen"` or `edition="Vaticanus"`
3. Update UI to allow edition selection

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
- Complete detailed data for all 150 psalms (both MT and LXX)
- Additional scholarly notes and commentary
- Improved genre classifications
- Historical context for superscriptions
- UI/UX improvements
- Additional Greek text editions (Göttingen, manuscript variants)
- Verse-level MT-LXX alignment for specific psalms

## 📚 References and Resources

### Primary Sources
- **Hebrew Bible**: Biblia Hebraica Stuttgartensia (BHS)
- **Septuagint**: Rahlfs-Hanhart edition (2006)
- **NETS**: New English Translation of the Septuagint

### Scholarly Resources
- Brueggemann, Walter. *The Psalms and the Life of Faith*
- Craigie, Peter C. *Psalms 1-50* (Word Biblical Commentary)
- Hossfeld, Frank-Lothar & Zenger, Erich. *Psalms* (Hermeneia Commentary)
- Pietersma, Albert & Wright, Benjamin G. *NETS: A New English Translation of the Septuagint*

### Online Resources
- [LXX Psalm Superscriptions Research](https://three-things.ca/category/codex/series/lxx-psalm-superscriptions/)
- [Septuagint Wikipedia](https://en.wikipedia.org/wiki/Septuagint)
- [NETS Edition](https://ccat.sas.upenn.edu/nets/)

## 📝 License

This project is provided as-is for educational and scholarly use.

Biblical text and scholarly metadata are in the public domain.

## 🙏 Acknowledgments

Built with passion for biblical scholarship and modern software development.

Special thanks to:
- The Hebrew Bible scholarship community
- Septuagint scholars and the NETS translation team
- Alfred Rahlfs for his critical LXX edition
- Open-source contributors

## 📧 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Contribute improvements via pull request
- Contact for scholarly collaboration

---

**Built with ❤️ for Bible scholars, students, and enthusiasts**

*"Blessed is the one... whose delight is in the law of the LORD, and who meditates on his law day and night."* — Psalm 1:1-2 (MT) / Psalm 1:1-2 (LXX)
