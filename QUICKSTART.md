# 🚀 Quick Start Guide

Get your Psalms database running in **under 2 minutes!**

## Installation & Launch

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database (first time only)
python seed.py

# 3. Launch the app
streamlit run app.py
```

**Alternative: Use the launch script**
```bash
./run.sh
```

The application will automatically open in your browser at `http://localhost:8501`

## What You Get

✅ **All 150 Psalms** with metadata
✅ **First 20 Psalms** with complete scholarly data including:
  - Hebrew superscriptions (מִזְמוֹר לְדָוִד, לַמְנַצֵּחַ, etc.)
  - Genre classifications
  - Authorship attribution
  - Musical/liturgical terms
  - NT quotations with references
  - Key themes and scholarly notes

✅ **Remaining 130 Psalms** with basic metadata (author, primary genre)

## Features You Can Use Right Away

### 1. **Browse & Search**
- View all 150 psalms as cards
- Full-text search across Hebrew, English, themes, and notes
- Click any psalm to see detailed view

### 2. **Filter**
Use sidebar filters to find specific psalms:
- By author (David, Asaph, Sons of Korah, etc.)
- By genre (Lament, Praise, Wisdom, etc.)
- By musical terms (לַמְנַצֵּחַ, בִּנְגִינוֹת, etc.)
- Acrostic structure (Yes/No/Partial)
- NT quotations (Has/Doesn't have)

### 3. **Export**
- Export filtered results as CSV or Excel
- Perfect for research and study

### 4. **Statistics**
- View distribution charts
- See insights like "How many Davidic laments?"
- Explore genre breakdowns

## Example Searches

**Find all Davidic laments:**
1. Filter by Author: "David"
2. Filter by Genre: "Lament"

**Find psalms quoted in NT:**
1. Filter by NT Quotations: "Has NT Quotations"

**Search for specific themes:**
1. Type "refuge" in search box
2. See all psalms mentioning refuge

## Next Steps

- Enrich psalms 21-150 with detailed data by editing `seed.py`
- Customize genres in the database
- Add your own scholarly notes

**Enjoy exploring the Psalms!** 📖
