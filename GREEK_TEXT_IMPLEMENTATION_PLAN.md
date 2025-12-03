# Greek Text (LXX) Implementation Plan
## Research Summary & Implementation Strategy

---

## 📚 Research Findings

### 1. **Psalm Numbering Differences (MT vs LXX)**

The Septuagint (LXX) and Masoretic Text (MT) have systematic numbering differences:

| Hebrew (MT) | Greek (LXX) | Note |
|-------------|-------------|------|
| **1-8** | **1-8** | ✅ Same numbering |
| **9-10** | **9** | Combined in LXX |
| **11-113** | **10-112** | LXX = MT - 1 (one behind) |
| **114-115** | **113** | Combined in LXX |
| **116** | **114-115** | Split in LXX |
| **117-146** | **116-145** | LXX = MT - 1 (one behind) |
| **147** | **146-147** | Split in LXX |
| **148-150** | **148-150** | ✅ Same numbering |
| **—** | **151** | LXX only (apocryphal) |

**Impact:** The famous Psalm 23 (MT) = Psalm 22 (LXX)

### 2. **Multiple Greek Text Editions**

There is no single "Septuagint" text. Multiple editions exist:

#### **Major Critical Editions:**
1. **Rahlfs-Hanhart (1935/2006)** - Semi-critical, most widely used
   - Based primarily on: Codex Vaticanus (B), Codex Sinaiticus (א), Codex Alexandrinus (A)
   - Standard reference edition

2. **Göttingen Septuagint** - Fully critical (ongoing project)
   - *Psalmi cum Odis* edited by Alfred Rahlfs (1979)
   - New critical edition project started 2020
   - Most scholarly, most complex apparatus

#### **Key Manuscripts:**
- **Codex Vaticanus (B)** - 4th century, purest text
- **Codex Sinaiticus (א)** - 4th century, partial survival
- **Codex Alexandrinus (A)** - 5th century, hexaplaric influence

**Scholarly Consensus:** Rahlfs-Hanhart differs minimally from Göttingen in most places. Rahlfs over-valued Vaticanus.

### 3. **Superscription Differences**

The LXX superscriptions differ **substantially** from MT:

#### **Davidic Attributions:**
- **MT:** 73 psalms attributed to David
- **LXX:** **85 psalms** attributed to David
  - **Adds David to:** Pss 33, 42, 43, 67, 71, 91, 93-99, 104, 137 (12 additional)
  - **Removes David from:** Pss 122, 124, 131, 133

#### **Historical Superscriptions:**
- LXX adds **14 additional historical titles** (mostly Book V)
- Connects Pss 27, 71, 97, 143, 144 with David's biography

#### **Translation Peculiarities:**
- LXX is usually very literal, but superscriptions differ radically
- Suggests textual fluidity and ongoing interpretive activity
- Manuscript variations exist even within LXX tradition

### 4. **Verse Numbering Differences**

**Critical Issue:** Superscription counting varies:

- **Hebrew tradition:** Often counts superscription as verse 1
  - Example: Psalm 3:1 (MT) = superscription
  - Psalm 3:2 (MT) = first line of psalm body

- **Greek tradition:** Sometimes doesn't count superscription as verse 1
  - Example: Psalm 3:1 (LXX) = first line of psalm body
  - Superscription is unnumbered or verse 0

**Impact:** **62 psalms** have verse number offsets (1-2 verses difference)

**Example:**
- MT Psalm 22:1 "My God, my God, why have you forsaken me?"
- LXX Psalm 21:2 (same text, different verse number)

---

## 🏗️ Proposed Database Schema

### **New Tables:**

#### **1. `greek_texts` (Main LXX text table)**
```sql
id: int (primary key)
edition: str  -- "Rahlfs-Hanhart", "Göttingen", "Vaticanus", etc.
lxx_psalm_number: int  -- Greek numbering (1-151)
mt_psalm_id: int (foreign key to psalms.id)  -- Link to Hebrew psalm
greek_heading: str  -- Full Greek superscription
greek_heading_transliteration: str  -- Romanized Greek
english_translation_heading: str  -- English translation of Greek heading
heading_agrees_with_mt: bool  -- Does Greek heading match Hebrew?
heading_differences_note: str  -- Description of differences
davidic_attribution_lxx: bool  -- David in LXX superscription?
historical_note_lxx: str  -- LXX-specific historical notes
created_at: datetime
updated_at: datetime
```

#### **2. `psalm_number_alignment` (Mapping table)**
```sql
id: int (primary key)
mt_psalm_number: int  -- Hebrew numbering (1-150)
lxx_psalm_number: str  -- Greek numbering (can be "9-10" for combined, "114a/114b" for split)
alignment_type: str  -- "exact", "combined", "split", "offset"
notes: str  -- Explanation of alignment
```

#### **3. `verse_number_alignment` (Optional, for precision)**
```sql
id: int (primary key)
psalm_id: int (foreign key to psalms.id)
greek_text_id: int (foreign key to greek_texts.id)
mt_verse_number: int
lxx_verse_number: int
superscription_counted_mt: bool
superscription_counted_lxx: bool
```

### **Schema Updates:**

#### **Update `psalms` table:**
```python
# Add helper fields
has_lxx_variant: bool = Field(default=False)  -- Has Greek variant?
lxx_attribution_differs: bool = Field(default=False)  -- Attribution differs in LXX?
lxx_psalm_numbers: str = Field(default=None)  -- "22" or "146-147" for split
```

---

## 🎯 Implementation Approach

### **Phase 1: Core Infrastructure** ⚙️

1. **Create new models** (`models.py`)
   - `GreekText` model
   - `PsalmNumberAlignment` model
   - Optional: `VerseNumberAlignment` model

2. **Create alignment mapping** (`lxx_alignment.py`)
   - Hard-coded lookup table for MT ↔ LXX numbering
   - Helper functions: `mt_to_lxx()`, `lxx_to_mt()`
   - Handle split/combined psalms

3. **Update database utilities** (`database.py`)
   - Add Greek text queries
   - Comparison functions
   - Alignment helpers

### **Phase 2: Data Collection** 📖

**Decision Point:** Which edition(s) to include?

**Recommended Approach:**
- **Primary:** Rahlfs-Hanhart (most accessible, standard)
- **Optional:** Add Codex Vaticanus variants for key psalms
- **Future:** Allow multiple editions per psalm

**Data Sources:**
- NETS (New English Translation of the Septuagint) - superscriptions
- Brenton's translation - widely available
- Academic resources for Greek text
- Manual curation for first 20-30 psalms with detailed comparison

### **Phase 3: UI Updates** 🖥️

#### **Detail Page Enhancements:**

Add expandable Greek text section:
```
┌─────────────────────────────────────┐
│ 📜 Hebrew (MT) - Psalm 23           │
│ מִזְמוֹר לְדָוִד                      │
│ "A Psalm of David"                  │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 🏛️ Greek (LXX) - Psalm 22          │  ← Different number!
│ Ψαλμὸς τῷ Δαυίδ                     │
│ "A Psalm of David"                  │
│ ✅ Heading agrees with Hebrew       │
└─────────────────────────────────────┘
```

#### **Comparison View:**
```
┌──────────────────────────────────────────┐
│ Heading Comparison: Psalm 91 (MT)       │
├──────────────────────────────────────────┤
│ Hebrew (MT):  [No superscription]        │
│ Greek (LXX):  "Αἶνος ᾠδῆς τῷ Δαυίδ"     │
│               "A Praise of a Song of     │
│                David"                    │
│ ❌ LXX adds Davidic attribution          │
└──────────────────────────────────────────┘
```

#### **Filter Additions:**
- "Show only psalms with LXX variants"
- "Show attribution differences (MT vs LXX)"
- "LXX Edition" dropdown (if multiple editions)

#### **Statistics Page:**
- "73 Davidic psalms in MT vs 85 in LXX"
- Chart: Attribution differences
- Alignment visualization

### **Phase 4: Export Enhancements** 📊

#### **CSV/Excel Export:**
Add columns:
- `LXX Psalm Number`
- `Greek Heading`
- `Greek Heading English`
- `Heading Agreement` (Yes/No)
- `LXX Edition`
- `Alignment Type` (exact/combined/split/offset)

### **Phase 5: Advanced Features** 🚀

1. **Verse-level alignment** (optional)
   - Map individual verse numbers
   - Handle superscription counting differences

2. **Multiple editions comparison**
   - Side-by-side Rahlfs vs Göttingen
   - Manuscript variant notes

3. **NT quotation tracking**
   - Note which LXX version NT authors used
   - Track quotation differences (MT vs LXX source)

---

## 📋 Detailed Implementation Steps

### **Step 1: Update Models**

```python
# models.py additions

class GreekText(SQLModel, table=True):
    """Greek (LXX) text data for Psalms"""
    __tablename__ = "greek_texts"

    id: Optional[int] = Field(default=None, primary_key=True)
    edition: str = Field(index=True)  # "Rahlfs-Hanhart", etc.
    lxx_psalm_number: str = Field(index=True)  # Can be "9", "114a", etc.

    # Link to Hebrew psalm
    mt_psalm_id: int = Field(foreign_key="psalms.id")

    # Greek superscription
    greek_heading: Optional[str] = None
    greek_heading_transliteration: Optional[str] = None
    english_translation_heading: Optional[str] = None

    # Comparison with MT
    heading_agrees_with_mt: bool = Field(default=True)
    heading_differences_note: Optional[str] = None

    # LXX-specific attribution
    davidic_attribution_lxx: bool = Field(default=False)
    historical_note_lxx: Optional[str] = None

    # Additional notes
    manuscript_notes: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    psalm: "Psalm" = Relationship(back_populates="greek_texts")


class PsalmNumberAlignment(SQLModel, table=True):
    """Mapping between MT and LXX psalm numbering"""
    __tablename__ = "psalm_number_alignments"

    id: Optional[int] = Field(default=None, primary_key=True)
    mt_psalm_number: int = Field(index=True)
    lxx_psalm_number: str = Field(index=True)  # Can be compound
    alignment_type: str  # "exact", "combined", "split", "offset"
    notes: Optional[str] = None


# Update Psalm model
class Psalm(SQLModel, table=True):
    # ... existing fields ...

    # Add Greek text relationship
    greek_texts: List["GreekText"] = Relationship(back_populates="psalm")

    @property
    def lxx_psalm_numbers(self) -> List[str]:
        """Get LXX psalm numbers for this MT psalm"""
        return [gt.lxx_psalm_number for gt in self.greek_texts]
```

### **Step 2: Create Alignment Utilities**

```python
# lxx_alignment.py (new file)

# Hard-coded alignment table
MT_TO_LXX_ALIGNMENT = {
    # Exact matches
    **{i: str(i) for i in range(1, 9)},  # 1-8 same

    # Combined psalms
    9: "9a", 10: "9b",  # MT 9-10 → LXX 9

    # Offset by -1
    **{i: str(i-1) for i in range(11, 114)},  # MT 11-113 → LXX 10-112

    # Combined psalms
    114: "113a", 115: "113b",  # MT 114-115 → LXX 113

    # Split psalm
    116: "114/115",  # MT 116 → LXX 114-115

    # Offset by -1 again
    **{i: str(i-1) for i in range(117, 147)},  # MT 117-146 → LXX 116-145

    # Split psalm
    147: "146/147",  # MT 147 → LXX 146-147

    # Exact matches
    148: "148", 149: "149", 150: "150",
}

def mt_to_lxx(mt_number: int) -> str:
    """Convert MT psalm number to LXX"""
    return MT_TO_LXX_ALIGNMENT.get(mt_number, str(mt_number))

def lxx_to_mt(lxx_number: int) -> List[int]:
    """Convert LXX psalm number to MT (can be multiple)"""
    # Reverse lookup
    results = []
    for mt, lxx in MT_TO_LXX_ALIGNMENT.items():
        if str(lxx_number) in lxx:
            results.append(mt)
    return results

def get_alignment_type(mt_number: int) -> str:
    """Get alignment type for a psalm"""
    if mt_number in [1,2,3,4,5,6,7,8,148,149,150]:
        return "exact"
    elif mt_number in [9,10,114,115]:
        return "combined"
    elif mt_number in [116, 147]:
        return "split"
    else:
        return "offset"
```

### **Step 3: Seed Greek Text Data**

Create `seed_greek_texts.py` with:
- Alignment table population
- First 20 psalms with Greek superscriptions
- Comparison notes (agrees/differs)
- Davidic attribution tracking

---

## ⚠️ Complexity & Challenges

### **1. Data Acquisition**
- Greek text data is less accessible than Hebrew
- Multiple editions require careful sourcing
- Manual curation needed for accuracy

### **2. Verse-Level Alignment**
- 62 psalms affected by verse numbering differences
- Requires detailed mapping (time-consuming)
- **Recommendation:** Start with psalm-level only, add verse-level later

### **3. UI Complexity**
- Dual numbering can confuse users
- Need clear visual distinction
- Consider "preference" setting (show MT or LXX numbers)

### **4. NT Quotation Tracking**
- Some NT quotes use LXX wording (differs from MT)
- Need to note which version NT authors used
- Example: Hebrews 10:5 quotes LXX Ps 39:7, not MT

---

## 🎯 Recommended Phased Rollout

### **Phase 1 (Core):** ⭐ Start here
- Add `GreekText` and `PsalmNumberAlignment` models
- Populate alignment table (all 150 psalms)
- Add Greek superscriptions for first 20 psalms (Rahlfs-Hanhart)
- Basic UI: Show Greek heading on detail page
- Export: Add LXX psalm number column

**Time estimate:** Medium complexity, high value

### **Phase 2 (Enhanced):**
- Complete Greek superscriptions for all 150 psalms
- Add comparison indicators (agrees/differs)
- Filter by "LXX attribution differs"
- Statistics on attribution differences

### **Phase 3 (Advanced):**
- Verse-level alignment for key psalms
- Multiple editions support (Rahlfs + Göttingen variants)
- NT quotation source tracking (MT vs LXX)

---

## 🤔 Decision Points for User

Before implementation, please decide:

1. **Which Greek edition(s)?**
   - ☐ Rahlfs-Hanhart only (recommended for start)
   - ☐ Add Göttingen variants
   - ☐ Add manuscript variants (Vaticanus, Sinaiticus)

2. **Scope of initial data:**
   - ☐ Alignment table only (all 150 psalms)
   - ☐ + Greek superscriptions (first 20 psalms with detail)
   - ☐ + Greek superscriptions (all 150 psalms, basic)

3. **Verse-level alignment:**
   - ☐ Psalm-level only (simpler, recommended start)
   - ☐ + Verse-level for key messianic psalms
   - ☐ + Verse-level for all psalms (most complex)

4. **UI approach:**
   - ☐ Show both MT and LXX numbers always
   - ☐ User preference (choose primary numbering)
   - ☐ Toggle between MT/LXX views

5. **Greek text display:**
   - ☐ Superscriptions only (headings)
   - ☐ + Full Greek psalm text (future)

---

## 📚 Sources

Research based on:
- [Septuagint Psalm Numbering - OCA](https://www.oca.org/liturgics/outlines/septuagint-numbering-psalms)
- [Psalm Numbering Differences - Jimmy Akin](https://jimmyakin.com/2012/06/why-are-the-psalms-numbered-differently.html)
- [Septuagint Editions - Wikipedia](https://en.wikipedia.org/wiki/Septuagint)
- [Critical Editions - Göttingen](https://septuaginta.uni-goettingen.de/ioscs/editions/)
- [LXX Psalm Superscriptions - Three Things](https://three-things.ca/category/codex/series/lxx-psalm-superscriptions/)
- [Reading Psalm Superscriptions - Gospel Coalition](https://www.thegospelcoalition.org/themelios/article/reading-psalm-superscriptions-through-the-centuries/)
- [Rahlfs-Hanhart Basis - LXX Reader's Edition](https://lxxre.wordpress.com/2018/05/14/why-did-we-choose-rahlfs-hanhart-as-the-basis-for-this-readers-edition/)

---

## ✅ Next Steps

1. **Review this plan** - Provide feedback on scope and priorities
2. **Make decisions** - Answer the 5 decision points above
3. **Implementation** - I'll build Phase 1 based on your preferences

**Estimated implementation time for Phase 1:** 2-3 hours
**Database schema changes:** 2 new tables, updates to existing models
**UI changes:** Detail page enhancements, filter additions, export columns

---

*This plan balances scholarly rigor with practical implementation. We can start simple (Phase 1) and expand based on your needs.*
