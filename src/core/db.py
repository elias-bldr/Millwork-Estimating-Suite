# db.py
import pandas as pd
from . import settings

# If your sheets are named differently, just adjust the sheet_name=...
INVENTORY_SHEET   = "Millwork Inventory Costs"
LABOR_SHEET       = "Millwork Labor Costs"
EXTERNAL_ITEMS_SHEET = "External Items Costs"
INSTALL_SHEET = "Install Labor Costs"

def _load_and_normalize(sheet_name: str) -> pd.DataFrame:
    # 1) read the sheet
    df = pd.read_excel(
        settings.EXCEL_PATH,
        sheet_name=sheet_name,
        dtype={"SKU #": str}
    ).set_index("SKU #")

    # 3) divide by 100 if UOM contains "CLF"
    clf = df["C_UOM"].str.contains("CLF", na=False)
    df.loc[clf, "Cost Each"] = df.loc[clf, "Cost Each"] / 100

    # 4) divide by 1000 if UOM contains "MBF" or "MSF"
    mbf_msf = df["C_UOM"].str.contains("MBF|MSF", na=False)
    df.loc[mbf_msf, "Cost Each"] = df.loc[mbf_msf, "Cost Each"] / 1000

    return df

def load_inventory() -> pd.DataFrame:
    return _load_and_normalize(INVENTORY_SHEET)

def load_labor():
    """
    Returns a DataFrame indexed by SKU # with columns like Description, Cost Each, OrgID, etc.
    """
    df = pd.read_excel(
        settings.EXCEL_PATH,
        sheet_name=LABOR_SHEET,
        dtype={"SKU #": str}
    )
    return df.set_index("SKU #")

def load_install():
    """
    Returns a DataFrame indexed by SKU # with columns like Description, Cost Each, OrgID, etc.
    """
    df = pd.read_excel(
        settings.EXCEL_PATH,
        sheet_name=INSTALL_SHEET,
        dtype={"SKU #": str}
    )
    return df.set_index("SKU #")

def load_external():
    """
    Returns a DataFrame indexed by SKU # with columns like Description, Cost Each, OrgID, etc.
    """
    df = pd.read_excel(
        settings.EXCEL_PATH,
        sheet_name=EXTERNAL_ITEMS_SHEET,
        dtype={"SKU #": str}
    )
    return df.set_index("SKU #")
