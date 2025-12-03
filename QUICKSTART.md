# 🚀 Quick Start Guide v2.0

Get your Psalms database running with **both Hebrew and Greek texts** in **under 3 minutes!**

## Installation & Launch

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database (first time only)
python seed.py                # Seed Hebrew (MT) data
python seed_greek_texts.py    # Seed Greek (LXX) data + alignment tables

# 3. Launch the app
streamlit run app.py
```

**Alternative: Use the launch script**
```bash
./run.sh
```

The application will automatically open in your browser at `http://localhost:8501`

## What You Get

### Hebrew (Masoretic Text)
✅ **All 150 Psalms** with comprehensive metadata
✅ **First 20 Psalms** with complete scholarly data including:
  - Hebrew superscriptions (מִזְמוֹר לְדָוִד, לַמְנַצֵּחַ, etc.)
  - Genre classifications
  - Authorship attribution (67 Davidic psalms)
  - Musical/liturgical terms
  - NT quotations with references
  - Key themes and scholarly notes

✅ **Remaining 130 Psalms** with metadata (author, genres)

### Greek (Septuagint - Rahlfs-Hanhart)
✅ **All 150 Psalms** with Greek superscriptions
✅ **LXX Numbering System** properly aligned with MT
  - Example: Psalm 23 (MT) = Psalm 22 (LXX)
✅ **Authorship Tracking**: 77 Davidic psalms in LXX (10 more than MT!)
✅ **Heading Comparison**: Visual indicators showing where MT and LXX differ
✅ **Complete Alignment Table**: MT↔LXX numbering for all 150 psalms

## Features You Can Use Right Away

### 1. **Browse & Search with Dual Numbering**
- View all 150 psalms as cards with **dual MT/LXX numbering**
- Example: See "23" with "LXX 22" displayed
- Full-text search across Hebrew, Greek, English, themes, and notes
- Click any psalm to see detailed view with both traditions

### 2. **Filter**
Use sidebar filters to find specific psalms:
- By author (David, Asaph, Sons of Korah, etc.)
- By genre (Lament, Praise, Wisdom, etc.)
- By musical terms (לַמְנַצֵּחַ, בִּנְגִינוֹת, etc.)
- Acrostic structure (Yes/No/Partial)
- NT quotations (Has/Doesn't have)

### 3. **View Details with MT-LXX Comparison**
Click any psalm to see:
- **Dual numbering in title**: "Psalm 23 (LXX 22)"
- **Hebrew superscription** with right-to-left display
- **Greek superscription** from Rahlfs-Hanhart edition
- **Agreement indicators**: ✅ if headings match, ⚠️ if they differ
- **Attribution comparison**: Side-by-side when MT and LXX differ
- All metadata, themes, and scholarly notes

### 4. **Export with LXX Data**
- Export filtered results as CSV or Excel
- Includes both MT and LXX data:
  - MT Psalm number & LXX Psalm number
  - Hebrew heading & Greek heading
  - MT author & LXX author
  - Heading agreement status
- Perfect for comparative research

### 5. **Statistics with MT-LXX Comparison**
- View distribution charts for authors and genres
- **NEW:** MT vs LXX comparison section:
  - 67 Davidic psalms (MT) vs 77 Davidic psalms (LXX)
  - 127 headings agree, 23 differ
  - Visual charts showing attribution overlap
- See insights like "How many Davidic laments?"
- Explore genre breakdowns

## Example Searches

**Find all Davidic laments:**
1. Filter by Author: "David"
2. Filter by Genre: "Lament"
3. Result: See them with dual numbering

**Find psalms quoted in NT:**
1. Filter by NT Quotations: "Has NT Quotations"
2. Compare MT and LXX versions

**Search for specific themes:**
1. Type "refuge" in search box
2. See all psalms mentioning refuge (searches both MT and LXX)

**Compare MT and LXX attributions:**
1. Navigate to Statistics page
2. View "Hebrew (MT) vs Greek (LXX) Comparison" section
3. See which psalms have different attributions

**Explore LXX-specific features:**
1. Click on Psalm 91 (LXX 90)
2. Notice: MT has no Davidic attribution, but LXX does!
3. See the Greek heading: "αἶνος ᾠδῆς τῷ Δαυίδ"

## Psalm Numbering Examples

Understanding the dual numbering system:

| What You're Looking For | Hebrew (MT) | Greek (LXX) |
|------------------------|-------------|-------------|
| The Lord is my shepherd | Psalm 23 | Psalm 22 |
| Out of the depths | Psalm 130 | Psalm 129 |
| Hallelujah, praise God | Psalm 150 | Psalm 150 |
| My God, why forsaken me? | Psalm 22 | Psalm 21 |

The app handles this automatically - just browse and it shows both!

## Next Steps

### Enrichment Opportunities
- Add more detailed data for psalms 21-150 by editing:
  - `seed.py` for Hebrew (MT) data
  - `seed_greek_texts.py` for Greek (LXX) data
- Customize genres in the database
- Add your own scholarly notes and commentary
- Contribute comparative analysis between MT and LXX

### Advanced Usage
- Explore the alignment table in `lxx_alignment.py`
- Understand the numbering conversion functions
- Add additional Greek text editions (Göttingen, manuscript variants)
- Implement verse-level alignment for specific psalms

**Enjoy exploring the dual-tradition Psalms database!** 📖 🏛️
