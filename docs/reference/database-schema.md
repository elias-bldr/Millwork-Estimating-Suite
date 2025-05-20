<!-- docs/reference/database-schema.md -->
# Database Schema

*(Excerpt – open the `.mdb` in Access for full view)*

``` sql
  CREATE TABLE Inventory (
    SKU            TEXT PRIMARY KEY,
    Description    TEXT,
    Cost_Each      CURRENCY,
    UOM            TEXT,
    Updated        DATETIME
  );

CREATE TABLE AssemblyDefs (
  AssemblyID AUTOINCREMENT PRIMARY KEY,
  Name        TEXT,
  ParentSKU   TEXT,
  QtyFormula  TEXT
);

!!! note
    Assembly Builder queries via pyodbc; DSN-less connection string:
    Driver={Microsoft Access Driver (*.mdb, *.accdb)};
    DBQ=C:\Users\<you>\Documents\PlanSwift Data\Lists\MillworkInventory.mdb;
