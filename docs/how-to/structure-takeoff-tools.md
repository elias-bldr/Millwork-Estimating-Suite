<!-- docs/how-to/structure-takeoff-tools.md -->
# How-to: Structure a Millwork Take-off

A consistent hierarchy speeds reporting and lets Segment-level filters work.

## Recommended hierarchy

```mermaid
graph TD
  Job --> Segment
  Segment --> Assembly
  Assembly -->|has many| Material
  Assembly --> Part
  Assembly --> Labor

| Level        | Naming rule      | Example                |
| ------------ | ---------------- | ---------------------- |
| **Job**      | `Project-Code`   | `24-AZ-347`            |
| **Segment**  | `Building-Floor` | `Bldg A – Floor 1`     |
| **Assembly** | `Room-Object`    | `BR 2 – Closet System` |

Tips
Create Segments for multi-building plans to isolate costs.

Use Properties → Filters on reports to include/exclude Segments.


---

```markdown
<!-- docs/how-to/select-list-items.md -->
# How-to: Select Items from List Databases

Four list tables install to `PlanSwift Data\Lists`:

| File | Table name | Contents |
|------|------------|----------|
| `MillworkInventory.mdb` | `Inventory` | SKU, Description, Cost |
| `MillworkLabor.mdb` | `LaborRates` | Task, Crew Rate |
| `MillworkParts.mdb` | `PartDefs` | Part SKUs |
| `MillworkAssemblies.mdb` | `AssemblyDefs` | Pre-built assemblies |

## Lookup procedure

1. Highlight an item field **SKU** ► click **[…]**.  
2. Filter by *Description contains* text.  
3. Press **Insert** → values populate *Cost* and *UOM*.

!!! tip
    Hold **Ctrl** while clicking to keep dialog open for rapid entry.

