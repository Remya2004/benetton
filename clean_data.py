import pandas as pd
import os
import sys

# ─────────────────────────────────────────
# FILE NAMES
# ─────────────────────────────────────────
FILE_SS25   = "data_ss25.xlsb"
FILE_SS2324 = "data_ss2324.xlsb"
OUTPUT_CSV  = "data_cleaned.csv"

def log(msg):
    print(f">> {msg}")

# ─────────────────────────────────────────
# FIT TYPE EXTRACTION
# Built from actual style names in your data
# ─────────────────────────────────────────
def extract_fit_type(des, cat):
    d = str(des).upper().strip()
    c = str(cat).upper().strip()

    # ── JACKET ───────────────────────────
    if c == "JACKET":
        if any(x in d for x in ["FRONT OPEN","F/O","OPEN FRONT","ZIPPER","ZIP THROUGH","ZIP UP"]):
            return "Front Open"
        if any(x in d for x in ["FRONT CLOSED","F/C","CLOSED FRONT","PULLOVER"]):
            return "Front Closed"
        if any(x in d for x in ["HOODIE","HOODED"]):
            return "Hooded"
        if "BOMBER" in d:
            return "Bomber"
        if "DENIM" in d:
            return "Denim Jacket"
        if any(x in d for x in ["PADDED","QUILTED","PUFFER"]):
            return "Padded / Puffer"
        return "Jacket - Other"

    # ── DENIM / BOTTOMS ──────────────────
    if c in ["DENIM","WOVEN BOTTOM","KNIT BOTTOM","TRICOT"]:
        if any(x in d for x in ["SHORTS","SHORT"]):
            return "Shorts"
        if any(x in d for x in ["SLIM FIT","SLIM-FIT"]) and "STRAIGHT" not in d:
            return "Slim Fit"
        if any(x in d for x in ["STRAIGHT FIT","STRAIGHT-FIT","STRAIGHT"]):
            return "Straight Fit"
        if any(x in d for x in ["REGULAR FIT","REGULAR-FIT","REGULAR"]):
            return "Regular Fit"
        if any(x in d for x in ["BOOT CUT","BOOTCUT","BOOT-CUT"]):
            return "Boot Cut"
        if any(x in d for x in ["FLARE","WIDE LEG","WIDE-LEG"]):
            return "Flare / Wide Leg"
        if any(x in d for x in ["CARGO","UTILITY POCKET"]):
            return "Cargo"
        if any(x in d for x in ["JOGGER","PULL ON","ELASTICATED","DRAWCORD"]):
            return "Jogger / Pull On"
        if any(x in d for x in ["SLOUCHY","RELAXED","RLXD","LOOSE"]):
            return "Relaxed Fit"
        return "Regular Fit"

    # ── TEE ──────────────────────────────
    if c == "TEE":
        if any(x in d for x in ["BOXY","OVSD","OVERSIZED","RLXD","RELAXED"]):
            return "Boxy / Oversized"
        if any(x in d for x in ["CROPPED","CROP"]):
            return "Cropped"
        if any(x in d for x in ["LONGLINE","LONG LINE","LONG-LINE"]):
            return "Longline"
        if "RAGLAN" in d:
            return "Raglan"
        if "HENLEY" in d:
            return "Henley"
        if any(x in d for x in ["STRIPER","STRIPE","STRIPPER"]):
            return "Striped Tee"
        return "Regular Tee"

    # ── POLO ─────────────────────────────
    if c == "POLO":
        if any(x in d for x in ["RESORT COLLAR","RESORT POLO","CUBAN COLLAR","RESORT"]):
            return "Resort / Open Collar"
        if any(x in d for x in ["PIQUE","PIQUÉ"]):
            return "Pique Polo"
        if any(x in d for x in ["OTTOMAN","JACQUARD","TEXTURED"]):
            return "Textured Polo"
        if "RUGBY" in d:
            return "Rugby Polo"
        if any(x in d for x in ["STRIPE","STRIPER"]):
            return "Striped Polo"
        if any(x in d for x in ["V-NECK","V NECK"]):
            return "V-Neck Polo"
        return "Solid Polo"

    # ── SHIRT / WOVEN TOP ─────────────────
    if c in ["SHIRT","WOVEN TOP"]:
        if any(x in d for x in ["RESORT SHIRT","RESORT COLLAR","CUBAN"]):
            return "Resort Shirt"
        if "HOODED" in d:
            return "Hooded Shirt"
        if any(x in d for x in ["CHECK","PLAID"]):
            return "Check Shirt"
        if any(x in d for x in ["STRIPE","STRIPER"]):
            return "Striped Shirt"
        if any(x in d for x in ["AOP","PRINT","FLORAL","TROPICAL"]):
            return "Printed Shirt"
        if "SEERSUCKER" in d:
            return "Seersucker Shirt"
        if any(x in d for x in ["SCHIFFLI","POINTELLE","CROCHET","LACE"]):
            return "Embellished Shirt"
        return "Solid / Casual Shirt"

    # ── SWEATSHIRT ────────────────────────
    if c == "SWEATSHIRT":
        if any(x in d for x in ["HOODIE","HOODED"]):
            return "Hoodie"
        if any(x in d for x in ["CREW NECK","CREWNECK","ROUND NECK"]):
            return "Crew Neck"
        if any(x in d for x in ["ZIP","ZIPPER","FRONT OPEN"]):
            return "Zip-Up"
        if any(x in d for x in ["OVERSIZED","OVSD","BOXY","RLXD"]):
            return "Oversized"
        return "Regular Sweatshirt"

    # ── DRESS ─────────────────────────────
    if c == "DRESS":
        if any(x in d for x in ["MIDI","MAXI"]):
            return "Midi / Maxi Dress"
        if any(x in d for x in ["TIERED","LAYERED","FLARED"]):
            return "Tiered / Flared Dress"
        if any(x in d for x in ["SHIRT DRESS","POLO DRESS"]):
            return "Shirt / Polo Dress"
        if any(x in d for x in ["PERMA PLEAT","PLEATED"]):
            return "Pleated Dress"
        if any(x in d for x in ["SHIFT","STRAIGHT"]):
            return "Shift Dress"
        if "SMOCKED" in d:
            return "Smocked Dress"
        return "Casual Dress"

    # ── ACCESSORIES ──────────────────────
    if c == "ACCESSORIES":
        if any(x in d for x in ["SLIDE","SANDAL"]):
            return "Slides / Sandals"
        if any(x in d for x in ["SNEAKER","TRAINER"]):
            return "Sneakers"
        if any(x in d for x in ["CAP","HAT","BUCKET"]):
            return "Caps / Hats"
        if any(x in d for x in ["BAG","BACKPACK","TOTE"]):
            return "Bags"
        return "Accessories - Other"

    return "Other"


# ─────────────────────────────────────────
# LOAD HELPER
# ─────────────────────────────────────────
def load_xlsb(filepath, season_label=None):
    log(f"Reading {filepath} ...")
    df = pd.read_excel(filepath, engine="pyxlsb", header=1)
    df.columns = [str(c).strip().upper() for c in df.columns]

    RENAME = {
        "REALIZED SALE-CR":   "REALIZED SALE- CR",
        "REALIZED SALE - CR": "REALIZED SALE- CR",
        "MRP/UNIT":           "MRP/ UNIT",
        " NET RECD":          "NET RECD",
        "STR":                "STR %",
        "STR%":               "STR %",
    }
    df.rename(columns=RENAME, inplace=True)

    if season_label:
        df["SEASON"] = season_label
    if "ORIGIN" not in df.columns:
        df["ORIGIN"] = "Retail - Domestic"
    if "FORMAT" not in df.columns:
        df["FORMAT"] = "UNKNOWN"

    log(f"  Loaded: {df.shape}")
    return df


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def clean_data():
    log("Starting Data Engine...")
    frames = []

    if os.path.exists(FILE_SS25):
        frames.append(load_xlsb(FILE_SS25, season_label="SS25"))
    else:
        log(f"WARNING: {FILE_SS25} not found")

    if os.path.exists(FILE_SS2324):
        frames.append(load_xlsb(FILE_SS2324))
    else:
        log(f"WARNING: {FILE_SS2324} not found")

    if not frames:
        print("ERROR: No files found.")
        sys.exit(1)

    df = pd.concat(frames, ignore_index=True)
    log(f"Combined: {df.shape}")

    # ── KEEP COLUMNS ─────────────────────
    NEEDED = [
        "SEASON","REGION","CAT","DES","GENDER",
        "ORDER QUANTITY","NET RECD","SOLD QTY",
        "REALIZED SALE- CR","MRP/ UNIT",
        "ORIGIN","FORMAT","STORE"
    ]
    NEEDED = [c for c in NEEDED if c in df.columns]
    df = df[NEEDED].copy()

    # ── GENDER FILTER ────────────────────
    df["GENDER"] = df["GENDER"].astype(str).str.strip().str.upper()
    before = len(df)
    df = df[df["GENDER"].isin(["BOYS","GIRLS"])].copy()
    log(f"Gender filter: {before:,} → {len(df):,} rows")

    # ── NUMERIC ──────────────────────────
    for col in ["ORDER QUANTITY","NET RECD","SOLD QTY",
                "REALIZED SALE- CR","MRP/ UNIT"]:
        if col in df.columns:
            df[col] = (
                df[col].astype(str)
                .str.replace(r"[₹,\s]","",regex=True)
                .str.replace(r"[^0-9.\-]","",regex=True)
            )
            df[col] = pd.to_numeric(df[col],errors="coerce").fillna(0)

    # ── STRINGS ──────────────────────────
    for col in ["SEASON","REGION","CAT","DES","GENDER",
                "ORIGIN","FORMAT","STORE"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()

    # ── ORIGIN MAP ───────────────────────
    ORIGIN_MAP = {
        "RTMC01":"Retail - Domestic","RTMC02":"Retail - Domestic",
        "WS01":"Wholesale","WS02":"Wholesale",
        "01C":"Import","DOMESTIC (ILP)":"Retail - Domestic",
        "IMPORTS":"Import",
    }
    df["ORIGIN"] = df["ORIGIN"].map(ORIGIN_MAP).fillna(df["ORIGIN"])

    # ── REMOVE JUNK ──────────────────────
    df = df[df["REGION"].astype(str).str.strip() != ""].copy()
    df = df[~df["REGION"].str.upper().str.contains(
        "TOTAL|GRAND|NAN|NONE",na=True)].copy()

    # ── STR % ────────────────────────────
    df["STR %"] = 0.0
    mask = df["NET RECD"] > 0
    df.loc[mask,"STR %"] = (
        df.loc[mask,"SOLD QTY"] / df.loc[mask,"NET RECD"] * 100
    ).clip(upper=100.0).round(1)

    # ── FIT TYPE ─────────────────────────
    log("Extracting FIT_TYPE from style names...")
    df["FIT_TYPE"] = df.apply(
        lambda r: extract_fit_type(r["DES"], r["CAT"]), axis=1
    )
    coverage = (df["FIT_TYPE"] != "Other").sum() / len(df) * 100
    log(f"FIT_TYPE coverage: {coverage:.1f}% of styles classified")

    # ── CORE FLAG ────────────────────────
    median_qty = df["ORDER QUANTITY"].median()
    df["CORE_FLAG"] = df.apply(
        lambda r: "Core" if (
            r["ORDER QUANTITY"] >= median_qty and r["STR %"] >= 50
        ) else "Fashion",
        axis=1
    )

    # ── PRICE BAND ───────────────────────
    def price_band(mrp):
        if mrp <= 799:    return "Value (<=799)"
        elif mrp <= 1299: return "Mid (800-1299)"
        elif mrp <= 1999: return "Premium (1300-1999)"
        else:             return "Luxury (2000+)"

    df["PRICE BAND"] = df["MRP/ UNIT"].apply(price_band)

    # ── SAVE ─────────────────────────────
    df.to_csv(OUTPUT_CSV, index=False)

    print("\n" + "="*50)
    print(f"SUCCESS — {OUTPUT_CSV} with {len(df):,} rows")
    print("="*50)
    print("\nRows by Season:")
    print(df["SEASON"].value_counts().to_string())
    print("\nRows by Region:")
    print(df["REGION"].value_counts().to_string())
    print("\nRows by Gender:")
    print(df["GENDER"].value_counts().to_string())
    print(f"\nFIT_TYPE coverage: {coverage:.1f}%")
    print("\nFit Types per Category:")
    print(df.groupby(["CAT","FIT_TYPE"]).size().reset_index(
        name="rows").sort_values(["CAT","rows"],
        ascending=[True,False]).to_string())
    print("="*50+"\n")

if __name__ == "__main__":
    clean_data()
