"""
LXX-MT Psalm Numbering Alignment Utilities

The Septuagint (LXX) and Masoretic Text (MT) use different numbering systems.
This module provides utilities for converting between them.

Key differences:
- MT Psalms 9-10 → LXX Psalm 9 (combined)
- MT Psalms 11-113 → LXX Psalms 10-112 (offset by -1)
- MT Psalms 114-115 → LXX Psalm 113 (combined)
- MT Psalm 116 → LXX Psalms 114-115 (split)
- MT Psalms 117-146 → LXX Psalms 116-145 (offset by -1)
- MT Psalm 147 → LXX Psalms 146-147 (split)
- LXX Psalm 151 has no MT equivalent (apocryphal)
"""

from typing import List, Dict, Tuple


# Complete MT → LXX alignment mapping
MT_TO_LXX_MAP: Dict[int, str] = {
    # Psalms 1-8: Exact match
    1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8",

    # Psalms 9-10: Combined in LXX as Psalm 9
    9: "9", 10: "9",

    # Psalms 11-113: LXX = MT - 1
    11: "10", 12: "11", 13: "12", 14: "13", 15: "14", 16: "15", 17: "16",
    18: "17", 19: "18", 20: "19", 21: "20", 22: "21", 23: "22", 24: "23",
    25: "24", 26: "25", 27: "26", 28: "27", 29: "28", 30: "29", 31: "30",
    32: "31", 33: "32", 34: "33", 35: "34", 36: "35", 37: "36", 38: "37",
    39: "38", 40: "39", 41: "40", 42: "41", 43: "42", 44: "43", 45: "44",
    46: "45", 47: "46", 48: "47", 49: "48", 50: "49", 51: "50", 52: "51",
    53: "52", 54: "53", 55: "54", 56: "55", 57: "56", 58: "57", 59: "58",
    60: "59", 61: "60", 62: "61", 63: "62", 64: "63", 65: "64", 66: "65",
    67: "66", 68: "67", 69: "68", 70: "69", 71: "70", 72: "71", 73: "72",
    74: "73", 75: "74", 76: "75", 77: "76", 78: "77", 79: "78", 80: "79",
    81: "80", 82: "81", 83: "82", 84: "83", 85: "84", 86: "85", 87: "86",
    88: "87", 89: "88", 90: "89", 91: "90", 92: "91", 93: "92", 94: "93",
    95: "94", 96: "95", 97: "96", 98: "97", 99: "98", 100: "99", 101: "100",
    102: "101", 103: "102", 104: "103", 105: "104", 106: "105", 107: "106",
    108: "107", 109: "108", 110: "109", 111: "110", 112: "111", 113: "112",

    # Psalms 114-115: Combined in LXX as Psalm 113
    114: "113", 115: "113",

    # Psalm 116: Split in LXX as Psalms 114-115
    116: "114/115",

    # Psalms 117-146: LXX = MT - 1
    117: "116", 118: "117", 119: "118", 120: "119", 121: "120", 122: "121",
    123: "122", 124: "123", 125: "124", 126: "125", 127: "126", 128: "127",
    129: "128", 130: "129", 131: "130", 132: "131", 133: "132", 134: "133",
    135: "134", 136: "135", 137: "136", 138: "137", 139: "138", 140: "139",
    141: "140", 142: "141", 143: "142", 144: "143", 145: "144", 146: "145",

    # Psalm 147: Split in LXX as Psalms 146-147
    147: "146/147",

    # Psalms 148-150: Exact match
    148: "148", 149: "149", 150: "150",
}


# Reverse mapping: LXX → MT (note: some LXX numbers map to multiple MT)
LXX_TO_MT_MAP: Dict[str, List[int]] = {
    "1": [1], "2": [2], "3": [3], "4": [4], "5": [5], "6": [6], "7": [7], "8": [8],
    "9": [9, 10],  # LXX 9 combines MT 9-10
    "10": [11], "11": [12], "12": [13], "13": [14], "14": [15], "15": [16], "16": [17],
    "17": [18], "18": [19], "19": [20], "20": [21], "21": [22], "22": [23], "23": [24],
    "24": [25], "25": [26], "26": [27], "27": [28], "28": [29], "29": [30], "30": [31],
    "31": [32], "32": [33], "33": [34], "34": [35], "35": [36], "36": [37], "37": [38],
    "38": [39], "39": [40], "40": [41], "41": [42], "42": [43], "43": [44], "44": [45],
    "45": [46], "46": [47], "47": [48], "48": [49], "49": [50], "50": [51], "51": [52],
    "52": [53], "53": [54], "54": [55], "55": [56], "56": [57], "57": [58], "58": [59],
    "59": [60], "60": [61], "61": [62], "62": [63], "63": [64], "64": [65], "65": [66],
    "66": [67], "67": [68], "68": [69], "69": [70], "70": [71], "71": [72], "72": [73],
    "73": [74], "74": [75], "75": [76], "76": [77], "77": [78], "78": [79], "79": [80],
    "80": [81], "81": [82], "82": [83], "83": [84], "84": [85], "85": [86], "86": [87],
    "87": [88], "88": [89], "89": [90], "90": [91], "91": [92], "92": [93], "93": [94],
    "94": [95], "95": [96], "96": [97], "97": [98], "98": [99], "99": [100], "100": [101],
    "101": [102], "102": [103], "103": [104], "104": [105], "105": [106], "106": [107],
    "107": [108], "108": [109], "109": [110], "110": [111], "111": [112], "112": [113],
    "113": [114, 115],  # LXX 113 combines MT 114-115
    "114": [116], "115": [116],  # Both parts of split MT 116
    "114/115": [116],  # Compound form
    "116": [117], "117": [118], "118": [119], "119": [120], "120": [121], "121": [122],
    "122": [123], "123": [124], "124": [125], "125": [126], "126": [127], "127": [128],
    "128": [129], "129": [130], "130": [131], "131": [132], "132": [133], "133": [134],
    "134": [135], "135": [136], "136": [137], "137": [138], "138": [139], "139": [140],
    "140": [141], "141": [142], "142": [143], "143": [144], "144": [145], "145": [146],
    "146": [147], "147": [147],  # Both parts of split MT 147
    "146/147": [147],  # Compound form
    "148": [148], "149": [149], "150": [150],
    "151": [],  # LXX only, no MT equivalent
}


# Alignment type lookup
ALIGNMENT_TYPES: Dict[int, str] = {}

# Exact matches (1-8, 148-150)
for i in list(range(1, 9)) + list(range(148, 151)):
    ALIGNMENT_TYPES[i] = "exact"

# Combined psalms
for i in [9, 10, 114, 115]:
    ALIGNMENT_TYPES[i] = "combined"

# Split psalms
for i in [116, 147]:
    ALIGNMENT_TYPES[i] = "split"

# Offset psalms (all others)
for i in range(11, 114):
    ALIGNMENT_TYPES[i] = "offset"
for i in range(117, 147):
    ALIGNMENT_TYPES[i] = "offset"


def mt_to_lxx(mt_number: int) -> str:
    """
    Convert MT psalm number to LXX psalm number.

    Args:
        mt_number: Masoretic Text psalm number (1-150)

    Returns:
        LXX psalm number as string (can be compound like "114/115")

    Example:
        >>> mt_to_lxx(23)
        "22"
        >>> mt_to_lxx(116)
        "114/115"
    """
    return MT_TO_LXX_MAP.get(mt_number, str(mt_number))


def lxx_to_mt(lxx_number: str) -> List[int]:
    """
    Convert LXX psalm number to MT psalm number(s).

    Args:
        lxx_number: Septuagint psalm number as string

    Returns:
        List of MT psalm numbers (usually one, but can be two for combined)

    Example:
        >>> lxx_to_mt("22")
        [23]
        >>> lxx_to_mt("9")
        [9, 10]
    """
    return LXX_TO_MT_MAP.get(lxx_number, [])


def get_alignment_type(mt_number: int) -> str:
    """
    Get the alignment type for a given MT psalm number.

    Args:
        mt_number: Masoretic Text psalm number (1-150)

    Returns:
        Alignment type: "exact", "combined", "split", or "offset"

    Example:
        >>> get_alignment_type(23)
        "offset"
        >>> get_alignment_type(116)
        "split"
    """
    return ALIGNMENT_TYPES.get(mt_number, "unknown")


def format_dual_number(mt_number: int) -> str:
    """
    Format psalm number showing both MT and LXX.

    Args:
        mt_number: Masoretic Text psalm number

    Returns:
        Formatted string like "Psalm 23 (LXX 22)"

    Example:
        >>> format_dual_number(23)
        "Psalm 23 (LXX 22)"
    """
    lxx_num = mt_to_lxx(mt_number)
    return f"Psalm {mt_number} (LXX {lxx_num})"


def get_alignment_note(mt_number: int) -> str:
    """
    Get a human-readable note explaining the alignment.

    Args:
        mt_number: Masoretic Text psalm number

    Returns:
        Explanatory note about the alignment
    """
    alignment_type = get_alignment_type(mt_number)
    lxx_num = mt_to_lxx(mt_number)

    if alignment_type == "exact":
        return f"MT and LXX have the same numbering"
    elif alignment_type == "offset":
        return f"LXX is one number behind MT"
    elif alignment_type == "combined":
        if mt_number in [9, 10]:
            return f"MT Psalms 9-10 are combined as LXX Psalm 9"
        else:  # 114, 115
            return f"MT Psalms 114-115 are combined as LXX Psalm 113"
    elif alignment_type == "split":
        if mt_number == 116:
            return f"MT Psalm 116 is split into LXX Psalms 114-115"
        else:  # 147
            return f"MT Psalm 147 is split into LXX Psalms 146-147"

    return ""


def get_all_alignments() -> List[Tuple[int, str, str, str]]:
    """
    Get complete alignment table for all 150 MT psalms.

    Returns:
        List of tuples: (mt_number, lxx_number, alignment_type, notes)
    """
    alignments = []
    for mt_num in range(1, 151):
        lxx_num = mt_to_lxx(mt_num)
        alignment_type = get_alignment_type(mt_num)
        notes = get_alignment_note(mt_num)
        alignments.append((mt_num, lxx_num, alignment_type, notes))

    return alignments
