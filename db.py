# db.py
import pandas as pd
import settings

# If your sheets are named differently, just adjust the sheet_name=...
INVENTORY_SHEET   = "Millwork Inventory Costs"
LABOR_SHEET       = "Millwork Labor Costs"
EXTERNAL_ITEMS_SHEET = "External Items Costs"
INSTALL_SHEET = "Install Labor Costs"

def load_inventory():
    """
    Returns a DataFrame indexed by SKU # with columns like Description, Cost Each, OrgID, etc.
    """
    df = pd.read_excel(
        settings.EXCEL_PATH,
        sheet_name=INVENTORY_SHEET,
        dtype={"SKU #": str}
    )
    return df.set_index("SKU #")

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
