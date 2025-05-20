<!-- docs/explanation/data-flow.md -->
# Data Flow

1. **Inventory update** → Excel sheet.  
2. Assembly Builder reads → recalculates assembly JSON.  
3. Pascal script inserts/updates items in PlanSwift DB.  
4. Reports query `[Takeoff]` quantities + costs.

!!! info
    Costs live only in PlanSwift after step 3; reports stay accurate even if sheet changes later.
