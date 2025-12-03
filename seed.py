"""
Seed the database with Psalm data.
First 20 psalms have complete, scholarly accurate data.
Remaining psalms have basic metadata.
"""
from sqlmodel import Session, select
from database import engine, init_db, add_psalm_with_genres, get_or_create_genre
from models import Psalm, Genre, PsalmGenre


def seed_detailed_psalms(session: Session):
    """
    Seed the first 20 psalms with complete, scholarly accurate data.
    Based on Hebrew Masoretic Text superscriptions and academic consensus.
    """

    detailed_psalms = [
        {
            "psalm_number": 1,
            "hebrew_heading": None,
            "english_heading_translation": None,
            "genres": ["Wisdom", "Torah Psalm"],
            "author_attribution": "Anonymous",
            "musical_liturgical_terms": None,
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Righteous vs wicked, Torah meditation, two ways, blessing, judgment",
            "nt_quotations": None,
            "notes": "No superscription. Serves as introduction to entire Psalter. Wisdom literature. Tree metaphor (v.3). Clear ethical dualism.",
            "selah_count": 0
        },
        {
            "psalm_number": 2,
            "hebrew_heading": None,
            "english_heading_translation": None,
            "genres": ["Royal", "Messianic"],
            "author_attribution": "Anonymous",
            "musical_liturgical_terms": None,
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Anointed king, God's sovereignty, nations in rebellion, Zion, divine sonship",
            "nt_quotations": "Acts 4:25-26, Acts 13:33, Heb 1:5, Heb 5:5, Rev 2:27, Rev 12:5, Rev 19:15",
            "notes": "No superscription but attributed to David in Acts 4:25. Royal enthronement psalm. Heavy NT usage. Messianic interpretation in early church.",
            "selah_count": 0
        },
        {
            "psalm_number": 3,
            "hebrew_heading": "מִזְמוֹר לְדָוִד בְּבָרְחוֹ מִפְּנֵי אַבְשָׁלוֹם בְּנוֹ",
            "english_heading_translation": "A Psalm of David, when he fled from Absalom his son",
            "genres": ["Lament", "Individual Lament", "Trust"],
            "author_attribution": "David",
            "musical_liturgical_terms": "מִזְמוֹר",
            "acrostic": "No",
            "historical_superscription": "When he fled from Absalom his son (2 Sam 15-18)",
            "key_themes": "Enemies, protection, trust in God, morning deliverance, God as shield",
            "nt_quotations": None,
            "notes": "First psalm with superscription. Historical note references 2 Samuel 15-18. Three Selah markers. Morning prayer motif (v.5).",
            "selah_count": 3
        },
        {
            "psalm_number": 4,
            "hebrew_heading": "לַמְנַצֵּחַ בִּנְגִינוֹת מִזְמוֹר לְדָוִד",
            "english_heading_translation": "To the choirmaster: with stringed instruments. A Psalm of David",
            "genres": ["Lament", "Trust", "Evening Prayer"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ, בִּנְגִינוֹת, מִזְמוֹר",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Righteousness, trust, God's favor, joy, peace, safety in sleep",
            "nt_quotations": None,
            "notes": "Evening prayer complement to Ps 3. 'Neginot' = stringed instruments. One Selah. Priestly blessing echo (v.6, cf. Num 6:24-26).",
            "selah_count": 1
        },
        {
            "psalm_number": 5,
            "hebrew_heading": "לַמְנַצֵּחַ אֶל־הַנְּחִילוֹת מִזְמוֹר לְדָוִד",
            "english_heading_translation": "To the choirmaster: for the flutes. A Psalm of David",
            "genres": ["Lament", "Morning Prayer"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ, אֶל־הַנְּחִילוֹת, מִזְמוֹר",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Morning prayer, wicked vs righteous, God's hatred of evil, guidance, refuge",
            "nt_quotations": "Rom 3:13 (v.9)",
            "notes": "Morning prayer (v.3). 'Nehilot' likely = flutes/pipes. Quoted in Romans. Strong ethical dualism. Temple imagery (v.7).",
            "selah_count": 0
        },
        {
            "psalm_number": 6,
            "hebrew_heading": "לַמְנַצֵּחַ בִּנְגִינוֹת עַל־הַשְּׁמִינִית מִזְמוֹר לְדָוִד",
            "english_heading_translation": "To the choirmaster: with stringed instruments; according to The Sheminith. A Psalm of David",
            "genres": ["Lament", "Penitential"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ, בִּנְגִינוֹת, עַל־הַשְּׁמִינִית, מִזְמוֹר",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Sickness, divine anger, tears, enemies, repentance, answered prayer",
            "nt_quotations": "Matt 7:23, Luke 13:27 (v.8)",
            "notes": "First of seven Penitential Psalms. 'Sheminith' = eighth/octave/lower register. Sickness as divine discipline. Sudden shift to confidence (v.8-10).",
            "selah_count": 0
        },
        {
            "psalm_number": 7,
            "hebrew_heading": "שִׁגָּיוֹן לְדָוִד אֲשֶׁר־שָׁר לַיהוָה עַל־דִּבְרֵי־כוּשׁ בֶּן־יְמִינִי",
            "english_heading_translation": "A Shiggaion of David, which he sang to the LORD concerning Cush, a Benjaminite",
            "genres": ["Lament", "Individual Lament"],
            "author_attribution": "David",
            "musical_liturgical_terms": "שִׁגָּיוֹן",
            "acrostic": "No",
            "historical_superscription": "Concerning Cush, a Benjaminite",
            "key_themes": "False accusation, refuge, God as judge, righteousness vindicated, divine justice",
            "nt_quotations": None,
            "notes": "Shiggaion = wild, passionate song (cf. Hab 3:1). Cush unknown—possibly Saul-era enemy. Oath of innocence (v.3-5). Theophany imagery. One Selah.",
            "selah_count": 1
        },
        {
            "psalm_number": 8,
            "hebrew_heading": "לַמְנַצֵּחַ עַל־הַגִּתִּית מִזְמוֹר לְדָוִד",
            "english_heading_translation": "To the choirmaster: according to The Gittith. A Psalm of David",
            "genres": ["Hymn", "Praise", "Creation"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ, עַל־הַגִּתִּית, מִזְמוֹר",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "God's majesty, human dignity, creation, divine name, dominion over creation",
            "nt_quotations": "Matt 21:16 (v.2), 1 Cor 15:27, Eph 1:22, Heb 2:6-8 (v.4-6)",
            "notes": "Creation hymn. 'Gittith' = from Gath or vintage tune. Inclusio (v.1,9). Heavy NT use re: Christ's humanity and dominion. Anthropology text.",
            "selah_count": 0
        },
        {
            "psalm_number": 9,
            "hebrew_heading": "לַמְנַצֵּחַ עַל־מוּת לַבֵּן מִזְמוֹר לְדָוִד",
            "english_heading_translation": "To the choirmaster: according to Muth-labben. A Psalm of David",
            "genres": ["Thanksgiving", "Praise"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ, עַל־מוּת לַבֵּן, מִזְמוֹר",
            "acrostic": "Partial",
            "historical_superscription": None,
            "key_themes": "Thanksgiving, God as judge, enemies destroyed, refuge, justice for oppressed",
            "nt_quotations": None,
            "notes": "Partial acrostic with Ps 10 (together form incomplete alphabetic acrostic). 'Muth-labben' = death of the son (?). Three Selah. Many Septuagint manuscripts combine 9-10.",
            "selah_count": 3
        },
        {
            "psalm_number": 10,
            "hebrew_heading": None,
            "english_heading_translation": None,
            "genres": ["Lament", "Communal Lament"],
            "author_attribution": "Anonymous",
            "musical_liturgical_terms": None,
            "acrostic": "Partial",
            "historical_superscription": None,
            "key_themes": "Wicked oppress poor, God seems distant, cry for justice, God's kingship",
            "nt_quotations": None,
            "notes": "Continues Ps 9 acrostic. No superscription. Vivid description of wicked. Question 'Why?' (v.1). Social justice theme. LXX joins with Ps 9.",
            "selah_count": 0
        },
        {
            "psalm_number": 11,
            "hebrew_heading": "לַמְנַצֵּחַ לְדָוִד",
            "english_heading_translation": "To the choirmaster. Of David",
            "genres": ["Trust", "Confidence"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Refuge in God, testing of righteous, God's throne, divine judgment",
            "nt_quotations": None,
            "notes": "Trust psalm. Refuses to flee like bird (v.1). Temple theology (v.4). God tests righteous and wicked. Ethical foundation shaking (v.3).",
            "selah_count": 0
        },
        {
            "psalm_number": 12,
            "hebrew_heading": "לַמְנַצֵּחַ עַל־הַשְּׁמִינִית מִזְמוֹר לְדָוִד",
            "english_heading_translation": "To the choirmaster: according to The Sheminith. A Psalm of David",
            "genres": ["Lament", "Communal Lament"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ, עַל־הַשְּׁמִינִית, מִזְמוֹר",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Deceitful speech, faithful remnant, pure words of God, protection of poor",
            "nt_quotations": None,
            "notes": "Communal lament. 'Sheminith' again (cf. Ps 6). Focus on false speech vs God's pure words (v.6). Social crisis. Oracle in v.5. One Selah.",
            "selah_count": 1
        },
        {
            "psalm_number": 13,
            "hebrew_heading": "לַמְנַצֵּחַ מִזְמוֹר לְדָוִד",
            "english_heading_translation": "To the choirmaster. A Psalm of David",
            "genres": ["Lament", "Individual Lament"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ, מִזְמוֹר",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "How long?, God's hiddenness, trust, salvation, joy after sorrow",
            "nt_quotations": None,
            "notes": "Classic individual lament structure: complaint (1-2), petition (3-4), trust (5-6). Four 'How long?' questions. Sudden mood shift. Model prayer for suffering.",
            "selah_count": 0
        },
        {
            "psalm_number": 14,
            "hebrew_heading": "לַמְנַצֵּחַ לְדָוִד",
            "english_heading_translation": "To the choirmaster. Of David",
            "genres": ["Wisdom", "Lament"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Fool's atheism, universal corruption, divine judgment, hope for salvation",
            "nt_quotations": "Rom 3:10-12 (v.1-3)",
            "notes": "Wisdom psalm. 'Fool' = practical atheist (v.1). Nearly identical to Ps 53. Quoted extensively in Romans 3. Corrupt generation theme. One Selah.",
            "selah_count": 1
        },
        {
            "psalm_number": 15,
            "hebrew_heading": "מִזְמוֹר לְדָוִד",
            "english_heading_translation": "A Psalm of David",
            "genres": ["Wisdom", "Torah Psalm", "Entrance Liturgy"],
            "author_attribution": "David",
            "musical_liturgical_terms": "מִזְמוֹר",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Ethical requirements for worship, righteousness, integrity, temple entry",
            "nt_quotations": None,
            "notes": "Entrance liturgy (cf. Ps 24). Question-answer format. Ten ethical requirements. Temple piety. Wisdom tradition. No Selah.",
            "selah_count": 0
        },
        {
            "psalm_number": 16,
            "hebrew_heading": "מִכְתָּם לְדָוִד",
            "english_heading_translation": "A Miktam of David",
            "genres": ["Trust", "Confidence"],
            "author_attribution": "David",
            "musical_liturgical_terms": "מִכְתָּם",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Refuge, inheritance, God as portion, resurrection hope, joy in God's presence",
            "nt_quotations": "Acts 2:25-28, Acts 13:35 (v.8-11)",
            "notes": "Trust psalm. 'Miktam' = inscription/atonement(?). Messianic: Peter's Pentecost sermon (Acts 2). Resurrection prophecy (v.10). Fullness of joy.",
            "selah_count": 0
        },
        {
            "psalm_number": 17,
            "hebrew_heading": "תְּפִלָּה לְדָוִד",
            "english_heading_translation": "A Prayer of David",
            "genres": ["Lament", "Individual Lament"],
            "author_attribution": "David",
            "musical_liturgical_terms": "תְּפִלָּה",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Vindication, righteousness, enemies, protection, seeing God's face",
            "nt_quotations": None,
            "notes": "Individual lament. 'Tefillah' = prayer. Oath of innocence. Apple of eye metaphor (v.8). Wings imagery. Beatific vision (v.15).",
            "selah_count": 0
        },
        {
            "psalm_number": 18,
            "hebrew_heading": "לַמְנַצֵּחַ לְעֶבֶד יְהוָה לְדָוִד אֲשֶׁר דִּבֶּר לַיהוָה אֶת־דִּבְרֵי הַשִּׁירָה הַזֹּאת בְּיוֹם הִצִּיל־יְהוָה אוֹתוֹ מִכַּף כָּל־אֹיְבָיו וּמִכַּף שָׁאוּל",
            "english_heading_translation": "To the choirmaster. Of David, the servant of the LORD, who addressed the words of this song to the LORD on the day when the LORD delivered him from the hand of all his enemies, and from the hand of Saul",
            "genres": ["Royal", "Thanksgiving", "Victory"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ",
            "acrostic": "No",
            "historical_superscription": "When the LORD delivered him from all his enemies and from Saul",
            "key_themes": "Deliverance, theophany, God as rock, divine warrior, royal thanksgiving",
            "nt_quotations": "Rom 15:9, 2 Sam 22 (parallel), Heb 2:13",
            "notes": "Longest superscription. Royal thanksgiving. Near duplicate of 2 Sam 22. Vivid theophany (v.7-15). Three Selah. Messianic overtones.",
            "selah_count": 3
        },
        {
            "psalm_number": 19,
            "hebrew_heading": "לַמְנַצֵּחַ מִזְמוֹר לְדָוִד",
            "english_heading_translation": "To the choirmaster. A Psalm of David",
            "genres": ["Hymn", "Wisdom", "Torah Psalm"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ, מִזְמוֹר",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Creation's witness, sun's circuit, Torah perfection, hidden sins, purity",
            "nt_quotations": "Rom 10:18 (v.4)",
            "notes": "Two-part structure: general revelation (1-6), special revelation (7-14). Seven synonyms for Torah. Sun as bridegroom. Perfect prayer conclusion (v.14).",
            "selah_count": 0
        },
        {
            "psalm_number": 20,
            "hebrew_heading": "לַמְנַצֵּחַ מִזְמוֹר לְדָוִד",
            "english_heading_translation": "To the choirmaster. A Psalm of David",
            "genres": ["Royal", "Liturgy"],
            "author_attribution": "David",
            "musical_liturgical_terms": "לַמְנַצֵּחַ, מִזְמוֹר",
            "acrostic": "No",
            "historical_superscription": None,
            "key_themes": "Prayer before battle, king's protection, trust in God not military might",
            "nt_quotations": None,
            "notes": "Royal liturgy. Pre-battle prayer for king. Antiphonal structure. Linked with Ps 21 (before/after battle). One Selah. Chariots vs God's name (v.7).",
            "selah_count": 1
        },
    ]

    for psalm_data in detailed_psalms:
        genres = psalm_data.pop("genres")
        add_psalm_with_genres(session, psalm_data, genres)

    print(f"✓ Seeded {len(detailed_psalms)} detailed psalms (1-20)")


def seed_basic_psalms(session: Session):
    """
    Seed remaining psalms (21-150) with basic metadata.
    These can be enriched later by users.
    """

    # Basic psalm data with common genres and attributions
    basic_data = [
        # Psalms 21-41 (Book 1 - mostly Davidic)
        *[(i, "David", ["Mixed"]) for i in range(21, 42)],
        # Psalms 42-72 (Book 2 - Korah, Asaph, David)
        *[(i, "Sons of Korah", ["Lament"]) for i in range(42, 49)],
        (49, "Sons of Korah", ["Wisdom"]),
        (50, "Asaph", ["Prophetic"]),
        *[(i, "David", ["Lament"]) for i in range(51, 65)],
        (65, "David", ["Thanksgiving"]),
        *[(i, "David", ["Praise"]) for i in range(66, 73)],
        # Psalms 73-89 (Book 3 - Asaph, Korah)
        *[(i, "Asaph", ["Wisdom"]) for i in range(73, 84)],
        *[(i, "Sons of Korah", ["Lament"]) for i in range(84, 89)],
        (89, "Ethan the Ezrahite", ["Lament"]),
        # Psalms 90-106 (Book 4 - mostly anonymous)
        (90, "Moses", ["Lament"]),
        *[(i, "Anonymous", ["Praise"]) for i in range(91, 101)],
        *[(i, "David", ["Praise"]) for i in range(101, 107)],
        # Psalms 107-150 (Book 5)
        *[(i, "Anonymous", ["Thanksgiving"]) for i in range(107, 110)],
        *[(i, "David", ["Royal"]) for i in range(110, 111)],
        *[(i, "Anonymous", ["Praise"]) for i in range(111, 120)],
        # Psalms 120-134 (Songs of Ascents)
        *[(i, "Anonymous", ["Pilgrimage"]) for i in range(120, 135)],
        # Final Hallel
        *[(i, "Anonymous", ["Praise"]) for i in range(135, 151)],
    ]

    for psalm_num, author, genres in basic_data:
        psalm_data = {
            "psalm_number": psalm_num,
            "author_attribution": author,
            "hebrew_heading": None,
            "english_heading_translation": None,
            "acrostic": "No",
            "selah_count": 0,
            "notes": "Basic metadata - to be enriched"
        }

        # Special cases with known features
        if psalm_num in [111, 112, 119, 145]:
            psalm_data["acrostic"] = "Yes"

        if psalm_num == 119:
            psalm_data["genres"] = ["Torah Psalm", "Wisdom"]
            psalm_data["key_themes"] = "Torah meditation, word of God, longest psalm"
        elif psalm_num == 110:
            psalm_data["genres"] = ["Royal", "Messianic"]
            psalm_data["nt_quotations"] = "Matt 22:44, Mark 12:36, Luke 20:42, Acts 2:34, Heb 1:13, Heb 5:6, Heb 7:17"
        elif psalm_num == 22:
            psalm_data["genres"] = ["Lament"]
            psalm_data["nt_quotations"] = "Matt 27:35, Matt 27:39, Matt 27:43, Matt 27:46, John 19:24, Heb 2:12"
            psalm_data["key_themes"] = "Suffering, crucifixion prophecy, messianic"
        else:
            psalm_data["genres"] = genres

        add_psalm_with_genres(session, psalm_data, psalm_data.pop("genres"))

    print(f"✓ Seeded {len(basic_data)} basic psalms (21-150)")


def main():
    """Main seeding function"""
    print("=" * 60)
    print("SEEDING BOOK OF PSALMS DATABASE")
    print("=" * 60)

    # Initialize database
    init_db()

    with Session(engine) as session:
        # Check if already seeded
        existing = session.exec(select(Psalm)).first()
        if existing:
            print("⚠ Database already contains psalms. Skipping seed.")
            print("  Delete psalms.db to re-seed from scratch.")
            return

        # Seed data
        seed_detailed_psalms(session)
        seed_basic_psalms(session)

        # Verify
        total = session.exec(select(Psalm)).all()
        print(f"\n✓ Total psalms in database: {len(total)}")

        genres = session.exec(select(Genre)).all()
        print(f"✓ Total genres: {len(genres)}")
        print(f"  Genres: {', '.join(g.name for g in genres)}")

    print("=" * 60)
    print("✓ SEEDING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
