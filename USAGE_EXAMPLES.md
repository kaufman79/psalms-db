# Usage Examples - Book of Psalms Database v2.0

This document provides practical examples for using the Psalms database programmatically, beyond the Streamlit UI.

## Table of Contents
1. [Basic Database Queries](#basic-database-queries)
2. [MT-LXX Numbering Conversion](#mt-lxx-numbering-conversion)
3. [Greek Text Comparison](#greek-text-comparison)
4. [Advanced Filtering](#advanced-filtering)
5. [Statistical Analysis](#statistical-analysis)
6. [Export and Data Processing](#export-and-data-processing)
7. [Edge Cases and Special Psalms](#edge-cases-and-special-psalms)

---

## Basic Database Queries

### Query a Single Psalm

```python
from sqlmodel import Session, select
from database import engine
from models import Psalm

with Session(engine) as session:
    # Get Psalm 23
    psalm23 = session.exec(
        select(Psalm).where(Psalm.psalm_number == 23)
    ).first()

    print(f"Psalm {psalm23.psalm_number}")
    print(f"Author: {psalm23.author_attribution}")
    print(f"Hebrew: {psalm23.hebrew_heading}")
    print(f"Genres: {', '.join(psalm23.genres)}")
```

### Query All Davidic Psalms

```python
from sqlmodel import Session, select
from database import engine
from models import Psalm

with Session(engine) as session:
    davidic_psalms = session.exec(
        select(Psalm).where(Psalm.author_attribution == "David")
    ).all()

    print(f"Found {len(davidic_psalms)} Davidic psalms")
    for psalm in davidic_psalms[:5]:  # First 5
        print(f"  Psalm {psalm.psalm_number}: {', '.join(psalm.genres)}")
```

### Query Psalms by Genre

```python
from sqlmodel import Session, select
from database import engine
from models import Psalm

with Session(engine) as session:
    # Get all laments
    laments = []
    all_psalms = session.exec(select(Psalm)).all()

    for psalm in all_psalms:
        if "Lament" in psalm.genres:
            laments.append(psalm)

    print(f"Found {len(laments)} lament psalms")
```

---

## MT-LXX Numbering Conversion

### Convert MT Number to LXX

```python
from lxx_alignment import mt_to_lxx, lxx_to_mt, format_dual_number, get_alignment_type

# Convert individual psalms
print(mt_to_lxx(23))  # Output: "22"
print(mt_to_lxx(116))  # Output: "114/115" (split in LXX)
print(mt_to_lxx(9))   # Output: "9"
print(mt_to_lxx(10))  # Output: "9" (combined with 9 in LXX)

# Format for display
print(format_dual_number(23))  # Output: "Psalm 23 (LXX 22)"

# Get alignment type
print(get_alignment_type(23))   # Output: "offset"
print(get_alignment_type(116))  # Output: "split"
print(get_alignment_type(9))    # Output: "combined"
```

### Convert LXX Number to MT

```python
from lxx_alignment import lxx_to_mt

# Convert back to MT
print(lxx_to_mt("22"))       # Output: [23]
print(lxx_to_mt("9"))        # Output: [9, 10] (multiple MT psalms)
print(lxx_to_mt("114/115"))  # Output: [116]

# Handle compound numbers
print(lxx_to_mt("114"))      # Output: [116] (part of split)
```

### Batch Conversion

```python
from lxx_alignment import get_all_alignments

# Get complete alignment table
alignments = get_all_alignments()

# Print first 15 alignments
for mt_num, lxx_num, alignment_type, notes in alignments[:15]:
    print(f"MT {mt_num:3d} → LXX {lxx_num:6s} ({alignment_type})")
```

---

## Greek Text Comparison

### Get Greek Text for a Psalm

```python
from sqlmodel import Session, select
from database import engine, get_greek_text
from models import Psalm

with Session(engine) as session:
    # Get Psalm 23
    psalm23 = session.exec(
        select(Psalm).where(Psalm.psalm_number == 23)
    ).first()

    # Get its Greek text
    greek = get_greek_text(session, psalm23.id)

    print(f"MT Psalm {psalm23.psalm_number} = LXX Psalm {greek.lxx_psalm_number}")
    print(f"\nHebrew: {psalm23.hebrew_heading}")
    print(f"Greek:  {greek.greek_heading}")
    print(f"Agrees: {greek.heading_agrees_with_mt}")
```

### Find Psalms Where MT and LXX Differ

```python
from sqlmodel import Session, select
from database import engine, get_greek_text
from models import Psalm

with Session(engine) as session:
    differences = []
    psalms = session.exec(select(Psalm)).all()

    for psalm in psalms:
        greek = get_greek_text(session, psalm.id)
        if greek and not greek.heading_agrees_with_mt:
            differences.append({
                'psalm': psalm.psalm_number,
                'mt_author': psalm.author_attribution,
                'lxx_author': greek.author_attribution_lxx,
                'note': greek.heading_differences_note
            })

    print(f"Found {len(differences)} psalms with heading differences")
    for diff in differences[:5]:  # First 5
        print(f"\nPsalm {diff['psalm']}:")
        print(f"  MT author: {diff['mt_author']}")
        print(f"  LXX author: {diff['lxx_author']}")
        print(f"  Note: {diff['note']}")
```

### Find LXX-Only Davidic Attributions

```python
from sqlmodel import Session, select
from database import engine, get_greek_text
from models import Psalm

with Session(engine) as session:
    lxx_only_davidic = []
    psalms = session.exec(select(Psalm)).all()

    for psalm in psalms:
        greek = get_greek_text(session, psalm.id)
        if greek:
            mt_davidic = psalm.author_attribution == "David"
            lxx_davidic = greek.davidic_attribution_lxx

            # LXX has David, but MT doesn't
            if lxx_davidic and not mt_davidic:
                lxx_only_davidic.append(psalm.psalm_number)

    print(f"LXX adds David to {len(lxx_only_davidic)} psalms:")
    print(f"Psalms: {', '.join(map(str, lxx_only_davidic))}")
```

---

## Advanced Filtering

### Search Across Multiple Fields

```python
from database import search_psalms, engine
from sqlmodel import Session

with Session(engine) as session:
    # Search for "refuge" in any text field
    results = search_psalms(
        session,
        search_query="refuge"
    )

    print(f"Found {len(results)} psalms mentioning 'refuge'")
    for psalm in results[:5]:
        print(f"  Psalm {psalm.psalm_number}: {psalm.key_themes[:50]}...")
```

### Complex Multi-Filter Query

```python
from database import search_psalms, engine
from sqlmodel import Session

with Session(engine) as session:
    # Find Davidic laments with NT quotations
    results = search_psalms(
        session,
        author="David",
        genre="Lament",
        has_nt_quotation=True
    )

    print(f"Found {len(results)} Davidic laments quoted in NT:")
    for psalm in results:
        print(f"  Psalm {psalm.psalm_number}: {psalm.nt_quotations}")
```

### Find Acrostic Psalms

```python
from sqlmodel import Session, select
from database import engine
from models import Psalm

with Session(engine) as session:
    acrostics = session.exec(
        select(Psalm).where(Psalm.acrostic == "Yes")
    ).all()

    print(f"Complete acrostic psalms: {len(acrostics)}")
    for psalm in acrostics:
        print(f"  Psalm {psalm.psalm_number}: {', '.join(psalm.genres)}")
```

---

## Statistical Analysis

### Get Complete Statistics

```python
from database import get_statistics, get_lxx_statistics, engine
from sqlmodel import Session

with Session(engine) as session:
    # MT statistics
    stats = get_statistics(session)
    print("=== MT Statistics ===")
    print(f"Total psalms: {stats['total_psalms']}")
    print(f"Davidic psalms: {stats['author_counts'].get('David', 0)}")
    print(f"NT quotations: {stats['nt_quotation_count']}")
    print(f"Total selah: {stats['total_selah']}")

    # LXX statistics
    lxx_stats = get_lxx_statistics(session)
    print("\n=== LXX Comparison ===")
    print(f"Davidic in MT: {lxx_stats['total_davidic_mt']}")
    print(f"Davidic in LXX: {lxx_stats['total_davidic_lxx']}")
    print(f"Headings agree: {lxx_stats['heading_agreements']}")
    print(f"Headings differ: {lxx_stats['heading_differences']}")
```

### Genre Distribution Analysis

```python
from database import get_statistics, engine
from sqlmodel import Session
import pandas as pd

with Session(engine) as session:
    stats = get_statistics(session)

    # Convert to DataFrame for analysis
    genre_df = pd.DataFrame(
        list(stats['genre_counts'].items()),
        columns=['Genre', 'Count']
    ).sort_values('Count', ascending=False)

    print(genre_df.to_string())

    # Calculate percentages
    genre_df['Percentage'] = (genre_df['Count'] / 150 * 100).round(1)
    print(f"\n{genre_df.to_string()}")
```

### Find Messianic Psalms

```python
from sqlmodel import Session, select
from database import engine
from models import Psalm

with Session(engine) as session:
    messianic_psalms = []
    all_psalms = session.exec(select(Psalm)).all()

    for psalm in all_psalms:
        # Check if Royal or Messianic genre, or has significant NT quotations
        if ("Royal" in psalm.genres or
            "Messianic" in psalm.genres or
            (psalm.nt_quotations and len(psalm.nt_quotations) > 50)):
            messianic_psalms.append(psalm)

    print(f"Found {len(messianic_psalms)} messianic/royal psalms")
    for psalm in messianic_psalms:
        print(f"  Psalm {psalm.psalm_number}: {', '.join(psalm.genres)}")
        if psalm.nt_quotations:
            print(f"    NT: {psalm.nt_quotations[:80]}...")
```

---

## Export and Data Processing

### Export to DataFrame

```python
from sqlmodel import Session, select
from database import engine, get_greek_text
from models import Psalm
import pandas as pd

with Session(engine) as session:
    psalms = session.exec(select(Psalm)).all()

    data = []
    for psalm in psalms:
        greek = get_greek_text(session, psalm.id)

        row = {
            'MT_Number': psalm.psalm_number,
            'LXX_Number': greek.lxx_psalm_number if greek else None,
            'Author_MT': psalm.author_attribution,
            'Author_LXX': greek.author_attribution_lxx if greek else None,
            'Genres': ', '.join(psalm.genres),
            'Hebrew_Heading': psalm.hebrew_heading,
            'Greek_Heading': greek.greek_heading if greek else None,
            'Heading_Agrees': greek.heading_agrees_with_mt if greek else None,
            'NT_Quotations': 'Yes' if psalm.has_nt_quotation else 'No',
            'Selah_Count': psalm.selah_count
        }
        data.append(row)

    df = pd.DataFrame(data)

    # Save to CSV
    df.to_csv('psalms_export.csv', index=False)
    print(f"Exported {len(df)} psalms to psalms_export.csv")

    # Or Excel
    df.to_excel('psalms_export.xlsx', index=False)
    print(f"Exported {len(df)} psalms to psalms_export.xlsx")
```

### Generate Custom Report

```python
from sqlmodel import Session, select
from database import engine, get_greek_text
from models import Psalm

with Session(engine) as session:
    psalms = session.exec(select(Psalm)).all()

    report = []
    report.append("# Davidic Attribution Differences Report\n")
    report.append("## Psalms Where LXX Adds Davidic Attribution\n")

    for psalm in psalms:
        greek = get_greek_text(session, psalm.id)
        if greek:
            mt_davidic = psalm.author_attribution == "David"
            lxx_davidic = greek.davidic_attribution_lxx

            if lxx_davidic and not mt_davidic:
                report.append(f"\n### Psalm {psalm.psalm_number} (LXX {greek.lxx_psalm_number})")
                report.append(f"- **MT**: {psalm.author_attribution or 'No attribution'}")
                report.append(f"- **LXX**: {greek.author_attribution_lxx}")
                report.append(f"- **Greek Heading**: {greek.greek_heading}")
                if greek.heading_differences_note:
                    report.append(f"- **Note**: {greek.heading_differences_note}")

    # Save report
    with open('davidic_differences_report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report))

    print("Generated report: davidic_differences_report.md")
```

---

## Edge Cases and Special Psalms

### Handle Split Psalms (MT 116, 147)

```python
from sqlmodel import Session, select
from database import engine, get_greek_text
from models import Psalm
from lxx_alignment import mt_to_lxx

with Session(engine) as session:
    # MT Psalm 116 splits into LXX 114 and 115
    psalm116 = session.exec(
        select(Psalm).where(Psalm.psalm_number == 116)
    ).first()

    greek = get_greek_text(session, psalm116.id)

    print(f"MT Psalm {psalm116.psalm_number}")
    print(f"LXX Number: {greek.lxx_psalm_number}")  # "114/115"
    print(f"Alignment: {mt_to_lxx(116)}")
    print(f"\nThis psalm is split in the LXX tradition")
```

### Handle Combined Psalms (MT 9-10, 114-115)

```python
from sqlmodel import Session, select
from database import engine, get_greek_text
from models import Psalm
from lxx_alignment import lxx_to_mt

with Session(engine) as session:
    # MT Psalms 9 and 10 are combined as LXX Psalm 9
    psalm9 = session.exec(
        select(Psalm).where(Psalm.psalm_number == 9)
    ).first()
    psalm10 = session.exec(
        select(Psalm).where(Psalm.psalm_number == 10)
    ).first()

    greek9 = get_greek_text(session, psalm9.id)
    greek10 = get_greek_text(session, psalm10.id)

    print(f"MT Psalm 9  → LXX {greek9.lxx_psalm_number}")
    print(f"MT Psalm 10 → LXX {greek10.lxx_psalm_number}")
    print(f"\nBoth are LXX Psalm 9 (combined)")

    # Reverse lookup
    mt_psalms = lxx_to_mt("9")
    print(f"LXX Psalm 9 corresponds to MT Psalms: {mt_psalms}")
```

### Handle Psalms with No Superscription

```python
from sqlmodel import Session, select
from database import engine
from models import Psalm

with Session(engine) as session:
    # Find psalms with no Hebrew superscription
    no_superscription = session.exec(
        select(Psalm).where(Psalm.hebrew_heading.is_(None))
    ).all()

    print(f"Found {len(no_superscription)} psalms with no MT superscription")
    for psalm in no_superscription[:10]:  # First 10
        greek = get_greek_text(session, psalm.id)
        has_greek = "Has Greek heading" if greek and greek.greek_heading else "No Greek heading"
        print(f"  Psalm {psalm.psalm_number}: {has_greek}")
```

### Handle Selah Counting

```python
from sqlmodel import Session, select
from database import engine
from models import Psalm

with Session(engine) as session:
    # Find psalms with most selah occurrences
    psalms = session.exec(
        select(Psalm).where(Psalm.selah_count > 0)
    ).all()

    # Sort by selah count
    sorted_psalms = sorted(psalms, key=lambda p: p.selah_count, reverse=True)

    print("Psalms with most Selah occurrences:")
    for psalm in sorted_psalms[:5]:  # Top 5
        print(f"  Psalm {psalm.psalm_number}: {psalm.selah_count} occurrences (סֶלָה)")
```

---

## Advanced Use Cases

### Build a Concordance

```python
from sqlmodel import Session, select
from database import engine
from models import Psalm
from collections import defaultdict

with Session(engine) as session:
    psalms = session.exec(select(Psalm)).all()

    # Build keyword index
    keyword_index = defaultdict(list)

    for psalm in psalms:
        # Index themes
        if psalm.key_themes:
            words = psalm.key_themes.lower().split()
            for word in words:
                if len(word) > 4:  # Index words longer than 4 chars
                    keyword_index[word].append(psalm.psalm_number)

    # Search concordance
    keyword = "justice"
    if keyword in keyword_index:
        print(f"'{keyword}' appears in psalms: {keyword_index[keyword]}")
```

### Compare Liturgical Traditions

```python
from lxx_alignment import MT_TO_LXX_MAP

# Orthodox/Catholic often use LXX numbering
# Protestant/Jewish use MT numbering

def liturgical_comparison(mt_number: int):
    """Show how different traditions reference the same psalm"""
    lxx_number = MT_TO_LXX_MAP[mt_number]

    print(f"Psalm {mt_number} in different traditions:")
    print(f"  Hebrew Bible / Protestant: Psalm {mt_number}")
    print(f"  Septuagint / Orthodox / Catholic: Psalm {lxx_number}")
    print(f"  Dead Sea Scrolls: Psalm {mt_number}")

# Examples
liturgical_comparison(23)  # Shepherd's Psalm
liturgical_comparison(51)  # Miserere
liturgical_comparison(130) # De Profundis
```

---

## Error Handling

```python
from sqlmodel import Session, select
from database import engine
from models import Psalm

def get_psalm_safely(psalm_number: int):
    """Safely get a psalm with error handling"""
    try:
        with Session(engine) as session:
            psalm = session.exec(
                select(Psalm).where(Psalm.psalm_number == psalm_number)
            ).first()

            if not psalm:
                raise ValueError(f"Psalm {psalm_number} not found")

            return psalm

    except Exception as e:
        print(f"Error retrieving psalm {psalm_number}: {e}")
        return None

# Usage
psalm = get_psalm_safely(23)
if psalm:
    print(f"Successfully retrieved Psalm {psalm.psalm_number}")
else:
    print("Failed to retrieve psalm")
```

---

## Contributing

If you develop additional usage patterns or discover edge cases, please contribute them to this document!

**Questions?** See the main README.md or open an issue.
