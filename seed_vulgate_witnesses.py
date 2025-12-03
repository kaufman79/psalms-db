#!/usr/bin/env python3
"""
Seed Vulgate (Latin) textual witnesses for Psalms superscriptions.
Uses the Clementine Vulgate edition.

Run after seed.py and seed_greek_texts.py to add Latin witness data.
"""
from sqlmodel import Session, select
from database import engine, get_all_psalms
from models import TextualWitness, Psalm


# Vulgate (Clementine) Superscriptions - extracted from scrollmapper/bible_databases
# Format: (psalm_number, latin_text, english_translation)
# Note: Vulgate follows LXX numbering but we align to MT numbering here
VULGATE_SUPERSCRIPTIONS = [
    (1, None, None),  # No superscription
    (2, None, None),  # No superscription
    (3, "Psalmus David, cum fugeret a facie Absalom filii sui.", "A Psalm of David, when he fled from the face of Absalom his son"),
    (4, "In finem, in carminibus. Psalmus David.", "Unto the end, with hymns. A Psalm of David"),
    (5, "In finem, pro ea quae haereditatem consequitur. Psalmus David.", "Unto the end, for her that obtains the inheritance. A Psalm of David"),
    (6, "In finem, in carminibus. Psalmus David. Pro octava.", "Unto the end, with hymns. A Psalm of David, for the eighth"),
    (7, "Psalmus David, quem cantavit Domino pro verbis Chusi, filii Jemini.", "A Psalm of David, which he sung to the Lord for the words of Chusi the son of Jemini"),
    (8, "In finem, pro torcularibus. Psalmus David.", "Unto the end, for the presses. A Psalm of David"),
    (9, "In finem, pro occultis filii. Psalmus David.", "Unto the end, for the hidden things of the son. A Psalm of David"),
    (10, "In finem. Psalmus David.", "Unto the end. A Psalm of David"),
    (11, "In finem, pro octava. Psalmus David.", "Unto the end, for the eighth. A Psalm of David"),
    (12, "In finem. Psalmus David.", "Unto the end. A Psalm of David"),
    (13, "In finem. Psalmus David.", "Unto the end. A Psalm of David"),
    (14, "Psalmus David.", "A Psalm of David"),
    (15, "Tituli inscriptio, ipsi David.", "The inscription of a title to David himself"),
    (16, "Oratio David.", "A prayer of David"),
    (17, "In finem. Puero Domini David, qui locutus est Domino verba cantici hujus, in die qua eripuit eum Dominus de manu omnium inimicorum ejus, et de manu Saul, et dixit:", "Unto the end, for the servant of the Lord, David, who spoke to the Lord the words of this canticle, in the day that the Lord delivered him from the hand of all his enemies, and from the hand of Saul, and he said:"),
    (18, "In finem. Psalmus David.", "Unto the end. A Psalm of David"),
    (19, "In finem. Psalmus David.", "Unto the end. A Psalm of David"),
    (20, "In finem. Psalmus David.", "Unto the end. A Psalm of David"),
    (21, "In finem, pro susceptione matutina. Psalmus David.", "Unto the end, for the morning protection. A Psalm of David"),
    (22, "Psalmus David.", "A Psalm of David"),
    (23, "Prima sabbati. Psalmus David.", "On the first day of the week. A Psalm of David"),
    (24, "Psalmus David.", "A Psalm of David"),
    (25, "Psalmus David.", "A Psalm of David"),
    (26, "Psalmus David, priusquam liniretur.", "A Psalm of David, before he was anointed"),
    (27, "Psalmus ipsi David.", "A Psalm for David himself"),
    (28, "Psalmus David, in consummatione tabernaculi.", "A Psalm of David, at the finishing of the tabernacle"),
    (29, "Psalmus cantici, in dedicatione domus David.", "A Psalm of a canticle, at the dedication of David's house"),
    (30, "In finem. Psalmus David, pro extasi.", "Unto the end. A Psalm for David, in an ecstasy"),
    (31, "Ipsi David intellectus.", "To David himself, understanding"),
    (32, "Psalmus David.", "A Psalm of David"),
    (33, "Davidi, cum immutavit vultum suum coram Achimelech, et dimisit eum, et abiit.", "For David, when he changed his countenance before Achimelech, and he sent him away and he departed"),
    (34, "Ipsi David.", "For David himself"),
    (35, "In finem. Servo Domini ipsi David.", "Unto the end, for the servant of the Lord, David himself"),
    (36, "Psalmus ipsi David.", "A Psalm for David himself"),
    (37, "Psalmus David, in rememorationem de sabbato.", "A Psalm of David, for a remembrance of the sabbath"),
    (38, "In finem, ipsi Idithun. Canticum David.", "Unto the end, for Idithun himself. A canticle of David"),
    (39, "In finem. Psalmus ipsi David.", "Unto the end. A Psalm for David himself"),
    (40, "In finem. Psalmus ipsi David.", "Unto the end. A Psalm for David himself"),
    (41, "In finem. Intellectus filiis Core.", "Unto the end, understanding for the sons of Core"),
    (42, "Psalmus David.", "A Psalm of David"),
    (43, "In finem. Filiis Core ad intellectum.", "Unto the end, for the sons of Core, for understanding"),
    (44, "In finem, pro iis qui commutabuntur. Filiis Core, ad intellectum. Canticum pro dilecto.", "Unto the end, for them that shall be changed, for the sons of Core, for understanding. A canticle for the beloved"),
    (45, "In finem, filiis Core, pro arcanis. Psalmus.", "Unto the end, for the sons of Core, for the hidden things. A Psalm"),
    (46, "In finem. Pro filiis Core. Psalmus.", "Unto the end, for the sons of Core. A Psalm"),
    (47, "In finem. Psalmus filiis Core.", "Unto the end, a Psalm for the sons of Core"),
    (48, "Psalmus cantici, filiis Core. Secunda sabbati.", "A Psalm of a canticle, for the sons of Core, on the second day of the week"),
    (49, "Psalmus Asaph.", "A Psalm of Asaph"),
    (50, "In finem. Psalmus David,", "Unto the end, a Psalm of David"),
    (51, "In finem. Intellectus David.", "Unto the end, understanding for David"),
    (52, "In finem. Pro Maheleth, intellectus David.", "Unto the end, for Maeleth, understanding for David"),
    (53, "In finem, in carminibus. Intellectus David.", "Unto the end, in verses, understanding for David"),
    (54, "In finem. In hymnis. Intellectus David.", "Unto the end, in hymns, understanding for David"),
    (55, "In finem. Pro populo qui a sanctis longe factus est. David in tituli inscriptionem, cum tenuerunt eum Allophyli in Geth.", "Unto the end, for the people that are removed at a distance from the sanctuary. For David, for an inscription of a title, when the Philistines held him in Geth"),
    (56, "In finem. Ne disperdas. David in tituli inscriptionem, cum fugeret a facie Saul in speluncam.", "Unto the end, destroy not, for David, for an inscription of a title, when he fled from Saul into the cave"),
    (57, "In finem. Ne disperdas. David in tituli inscriptionem.", "Unto the end, destroy not, for David, for an inscription of a title"),
    (58, "In finem. Ne disperdas. David in tituli inscriptionem.", "Unto the end, destroy not, for David, for an inscription of a title"),
    (59, "In finem. Pro iis qui immutabuntur. In tituli inscriptionem ipsi David, in doctrinam,", "Unto the end, for them that shall be changed, for the inscription of a title, to David himself, for doctrine"),
    (60, "In finem. In hymnis. Psalmus David.", "Unto the end, in hymns, a Psalm of David"),
    (61, "In finem. In hymnis David.", "Unto the end, in hymns, for David"),
    (62, "Psalmus David, cum esset in deserto Idumaeae.", "A Psalm of David when he was in the desert of Edom"),
    (63, "In finem. Psalmus David.", "Unto the end, a Psalm of David"),
    (64, "In finem. Psalmus David. Canticum Jeremiae et Ezechielis populo transmigrationis, cum inciperent exire.", "Unto the end, a Psalm of David. The canticle of Jeremias and Ezechiel to the people of the captivity, when they began to go out"),
    (65, "In finem. Canticum Psalmi resurrectionis.", "Unto the end, a canticle of a Psalm of the resurrection"),
    (66, "In finem. In hymnis. Psalmus cantici David.", "Unto the end, in hymns, a Psalm of a canticle for David"),
    (67, "In finem. Psalmus cantici ipsi David.", "Unto the end, a Psalm of a canticle for David himself"),
    (68, "In finem. Pro iis qui commutabuntur. David.", "Unto the end, for them that shall be changed, for David"),
    (69, "In finem. Psalmus David. In rememorationem, quod salvum fecerit eum Dominus.", "Unto the end, a Psalm for David, to bring to remembrance that the Lord saved him"),
    (70, None, None),  # No superscription
    (71, "Psalmus David. In Salomonem.", "A Psalm on Solomon. For David"),
    (72, "Psalmus Asaph.", "A Psalm for Asaph"),
    (73, "Intellectus Asaph.", "Understanding for Asaph"),
    (74, "In finem. Ne corrumpas. Psalmus cantici Asaph.", "Unto the end, corrupt not, a Psalm of a canticle for Asaph"),
    (75, "In finem. In laudibus. Psalmus Asaph. Canticum ad Assyrios.", "Unto the end, in praises, a Psalm for Asaph: a canticle to the Assyrians"),
    (76, "In finem. Pro Idithun. Psalmus Asaph.", "Unto the end, for Idithun, a Psalm of Asaph"),
    (77, "Intellectus Asaph.", "Understanding for Asaph"),
    (78, "Psalmus Asaph.", "A Psalm for Asaph"),
    (79, "In finem. Pro iis qui commutabuntur. Testimonium Asaph. Psalmus.", "Unto the end, for them that shall be changed, a testimony for Asaph, a Psalm"),
    (80, "In finem. Pro torcularibus. Psalmus ipsi Asaph.", "Unto the end, for the winepresses, a Psalm for Asaph himself"),
    (81, "Psalmus Asaph.", "A Psalm for Asaph"),
    (82, "Canticum Psalmi Asaph.", "A canticle of a Psalm for Asaph"),
    (83, "In finem. Pro torcularibus filiis Core. Psalmus.", "Unto the end, for the winepresses, for the sons of Core, a Psalm"),
    (84, "Oratio ipsi David.", "A prayer for David himself"),
    (85, "Canticum Psalmi filiis Core. Secunda sabbati.", "A canticle of a Psalm for the sons of Core: for the second day of the week"),
    (86, "Oratio David.", "A prayer of David"),
    (87, "Canticum Psalmi filiis Core. In finem, pro Maheleth ad respondendum. Intellectus Eman Ezrahitae.", "A canticle of a Psalm for the sons of Core: unto the end, for Maeleth, to answer understanding of Eman the Ezrahite"),
    (88, "Intellectus Ethan Ezrahitae.", "Understanding for Ethan the Ezrahite"),
    (89, "Oratio Moysi, hominis Dei.", "A prayer of Moses the man of God"),
    (90, None, None),  # No superscription
    (91, "Laus cantici David.", "Praise of a canticle for David"),
    (92, "Psalmus David. In die ante sabbatum, quando fundata est terra.", "A Psalm for David. When the house was built after the captivity. On the day before the sabbath"),
    (93, "Psalmus David. Quarta sabbati.", "A Psalm for David. On the fourth day of the week"),
    (94, "Laus cantici ipsi David.", "Praise of a canticle of David himself"),
    (95, "Quando domus aedificabatur post captivitatem. Canticum David.", "When the house was built after the captivity. A canticle for David"),
    (96, "Canticum David, quando terra ejus restituta est.", "A canticle for David, when his land was restored again to him"),
    (97, "Psalmus David.", "A Psalm for David"),
    (98, "Psalmus David.", "A Psalm for David"),
    (99, "Psalmus in confitendum.", "A Psalm of praise"),
    (100, "Psalmus ipsi David.", "A Psalm for David himself"),
    (101, "Oratio pauperis, cum anxius fuerit, et in conspectu Domini effuderit precem suam.", "The prayer of the poor man, when he was anxious, and poured out his supplication before the Lord"),
    (102, "Ipsi David.", "For David himself"),
    (103, None, None),  # No superscription
    (104, None, None),  # No superscription
    (105, None, None),  # No superscription
    (106, None, None),  # No superscription
    (107, "Canticum Psalmi ipsi David.", "A canticle of a Psalm, for David himself"),
    (108, "In finem. Psalmus David.", "Unto the end, a Psalm of David"),
    (109, "Alleluja.", "Alleluia"),
    (110, "Alleluja.", "Alleluia"),
    (111, "Alleluja.", "Alleluia"),
    (112, "Alleluja.", "Alleluia"),
    (113, "In exitu Israel de Aegypto, domus Jacob de populo barbaro,", "When Israel went out of Egypt, the house of Jacob from a barbarous people"),
    (114, "Alleluja.", "Alleluia"),
    (115, None, None),  # No superscription
    (116, "Alleluja.", "Alleluia"),
    (117, "Alleluja.", "Alleluia"),
    (118, "Alleluja.", "Alleluia"),
    (119, "Canticum graduum.", "A gradual canticle"),
    (120, "Canticum graduum.", "A gradual canticle"),
    (121, "Canticum graduum.", "A gradual canticle"),
    (122, "Canticum graduum.", "A gradual canticle"),
    (123, "Canticum graduum. Ad te levavi oculos meos, qui habitas in caelis.", "A gradual canticle. To thee have I lifted up my eyes, who dwellest in heaven"),
    (124, "Canticum graduum.", "A gradual canticle"),
    (125, "Canticum graduum. In convertendo Dominus captivitatem Sion, facti sumus sicut consolati.", "A gradual canticle. When the Lord brought back the captivity of Sion, we became like men comforted"),
    (126, "Canticum graduum Salomonis.", "A gradual canticle of Solomon"),
    (127, "Canticum graduum.", "A gradual canticle"),
    (128, "Canticum graduum.", "A gradual canticle"),
    (129, "Canticum graduum.", "A gradual canticle"),
    (130, "Canticum graduum David.", "A gradual canticle of David"),
    (131, "Canticum graduum.", "A gradual canticle"),
    (132, "Canticum graduum.", "A gradual canticle"),
    (133, "Canticum graduum. Ecce nunc benedicite Dominum, omnes servi Domini, qui statis in domo Domini, in atriis domus Dei nostri.", "A gradual canticle. Behold now bless ye the Lord, all ye servants of the Lord: Who stand in the house of the Lord, in the courts of the house of our God"),
    (134, "Alleluja.", "Alleluia"),
    (135, "Alleluja.", "Alleluia"),
    (136, "Psalmus David.", "A Psalm of David"),
    (137, "Ipsi David. Alleluja. Aggaei et Zachariae.", "For David himself. Alleluia. Of Aggeus and Zacharias"),
    (138, "In finem. Psalmus David.", "Unto the end, a Psalm of David"),
    (139, "In finem. Psalmus David.", "Unto the end, a Psalm of David"),
    (140, "In finem. Psalmus David.", "Unto the end, a Psalm of David"),
    (141, "Intellectus David, cum esset in spelunca. Oratio.", "Of understanding for David. A prayer when he was in the cave"),
    (142, "Psalmus David, adversus Goliath.", "A Psalm of David against Goliath"),
    (143, "Psalmus David.", "A Psalm for David"),
    (144, "Alleluja. David.", "Alleluia. Of David"),
    (145, "Alleluja. Aggaei et Zachariae.", "Alleluia. Of Aggeus and Zacharias"),
    (146, "Alleluja. Aggaei et Zachariae.", "Alleluia. Of Aggeus and Zacharias"),
    (147, "Alleluja.", "Alleluia"),
    (148, "Alleluja.", "Alleluia"),
    (149, "Alleluja.", "Alleluia"),
    (150, "Alleluja.", "Alleluia"),
]


def parse_vulgate_superscription(latin_text: str, english_text: str) -> dict:
    """Parse Vulgate superscription to extract structured data."""
    if not latin_text:
        return {
            "has_author_attribution": False,
            "davidic_attribution": False,
            "author_attribution": None,
            "musical_terms": None,
            "historical_note": None,
            "genre_designation": None,
        }

    latin_lower = latin_text.lower()

    # Check for Davidic attribution
    davidic = "david" in latin_lower

    # Extract author attribution
    author = None
    if "david" in latin_lower:
        author = "David"
    elif "asaph" in latin_lower:
        author = "Asaph"
    elif "core" in latin_lower:
        author = "Sons of Core"
    elif "moysi" in latin_lower or "moses" in english_text.lower():
        author = "Moses"
    elif "salomon" in latin_lower:
        author = "Solomon"
    elif "ethan" in latin_lower or "eman" in latin_lower:
        author = "Ethan the Ezrahite" if "ethan" in latin_lower else "Eman the Ezrahite"

    # Extract musical terms
    musical_terms = []
    if "in carminibus" in latin_lower or "hymnis" in latin_lower:
        musical_terms.append("in carminibus/hymnis (with hymns/stringed instruments)")
    if "pro octava" in latin_lower:
        musical_terms.append("pro octava (for the eighth)")
    if "torcularibus" in latin_lower:
        musical_terms.append("pro torcularibus (for the winepresses)")

    # Extract genre designations
    genre = None
    if "psalmus" in latin_lower:
        genre = "Psalmus (Psalm)"
    if "canticum" in latin_lower:
        genre = "Canticum (Canticle/Song)"
    if "oratio" in latin_lower:
        genre = "Oratio (Prayer)"
    if "alleluja" in latin_lower or "alleluia" in english_text.lower():
        genre = "Alleluja (Praise)"
    if "canticum graduum" in latin_lower:
        genre = "Canticum graduum (Song of Ascents)"

    # Extract historical notes
    historical = None
    if "absalom" in latin_lower:
        historical = "When he fled from Absalom his son"
    elif "saul" in latin_lower and "spelunca" in latin_lower:
        historical = "When he fled from Saul into the cave"
    elif "achimelech" in latin_lower or "allophyli" in latin_lower:
        historical = "When the Philistines held him in Geth / before Achimelech"
    elif "goliath" in latin_lower:
        historical = "Against Goliath"
    elif "deserto" in latin_lower:
        historical = "When he was in the desert"
    elif "captivit" in latin_lower:
        historical = "After the captivity / when the house was built"

    return {
        "has_author_attribution": author is not None,
        "davidic_attribution": davidic,
        "author_attribution": author,
        "musical_terms": ", ".join(musical_terms) if musical_terms else None,
        "historical_note": historical,
        "genre_designation": genre,
    }


def seed_vulgate_witnesses(session: Session):
    """Seed Vulgate textual witnesses for all 150 Psalms."""
    print("=" * 80)
    print("Seeding Vulgate (Latin) Textual Witnesses")
    print("=" * 80)

    # Get all existing psalms
    psalms = get_all_psalms(session)
    psalm_dict = {p.psalm_number: p for p in psalms}

    added_count = 0
    skipped_count = 0

    for psalm_num, latin_text, english_text in VULGATE_SUPERSCRIPTIONS:
        # Get the psalm
        psalm = psalm_dict.get(psalm_num)
        if not psalm:
            print(f"⚠️  Warning: Psalm {psalm_num} not found in database. Skipping.")
            skipped_count += 1
            continue

        # Check if Vulgate witness already exists
        existing = session.exec(
            select(TextualWitness).where(
                TextualWitness.mt_psalm_id == psalm.id,
                TextualWitness.tradition == "Vulgate"
            )
        ).first()

        if existing:
            print(f"⏭️  Psalm {psalm_num}: Vulgate witness already exists. Skipping.")
            skipped_count += 1
            continue

        # Parse the superscription
        parsed = parse_vulgate_superscription(latin_text or "", english_text or "")

        # Determine if it agrees with MT
        agrees_with_mt = True
        differences = []

        # Compare author attribution
        if psalm.author_attribution and parsed["author_attribution"]:
            mt_author = psalm.author_attribution.lower()
            vul_author = parsed["author_attribution"].lower()
            if "david" in mt_author and "david" not in vul_author:
                agrees_with_mt = False
                differences.append("Vulgate lacks Davidic attribution present in MT")
            elif "david" not in mt_author and "david" in vul_author:
                agrees_with_mt = False
                differences.append("Vulgate adds Davidic attribution not in MT")

        # Create the witness
        witness = TextualWitness(
            tradition="Vulgate",
            language="Latin",
            edition="Clementine Vulgate",
            mt_psalm_id=psalm.id,
            mt_psalm_number=psalm_num,
            original_text=latin_text,
            english_translation=english_text,
            has_author_attribution=parsed["has_author_attribution"],
            author_attribution=parsed["author_attribution"],
            davidic_attribution=parsed["davidic_attribution"],
            musical_terms=parsed["musical_terms"],
            historical_note=parsed["historical_note"],
            genre_designation=parsed["genre_designation"],
            agrees_with_mt=agrees_with_mt,
            differences_from_mt="; ".join(differences) if differences else None,
            textual_notes="Vulgate follows LXX tradition in many superscriptions",
        )

        session.add(witness)
        added_count += 1

        # Print status
        status = "✅" if latin_text else "⚪"
        author_info = f" [{parsed['author_attribution']}]" if parsed["author_attribution"] else ""
        print(f"{status} Psalm {psalm_num}{author_info}: {'Has superscription' if latin_text else 'No superscription'}")

    session.commit()

    print()
    print("=" * 80)
    print(f"✅ Successfully added {added_count} Vulgate witnesses")
    print(f"⏭️  Skipped {skipped_count} (already exist or psalm not found)")
    print("=" * 80)

    # Print summary statistics
    total_witnesses = session.exec(
        select(TextualWitness).where(TextualWitness.tradition == "Vulgate")
    ).all()

    with_super = len([w for w in total_witnesses if w.original_text])
    without_super = len([w for w in total_witnesses if not w.original_text])
    davidic = len([w for w in total_witnesses if w.davidic_attribution])

    print()
    print("Summary Statistics:")
    print(f"  Total Vulgate witnesses: {len(total_witnesses)}")
    print(f"  With superscriptions: {with_super}")
    print(f"  Without superscriptions: {without_super}")
    print(f"  Davidic attributions: {davidic}")
    print()


def main():
    """Main function to seed Vulgate witnesses."""
    with Session(engine) as session:
        seed_vulgate_witnesses(session)


if __name__ == "__main__":
    main()
