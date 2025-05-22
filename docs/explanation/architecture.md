<!-- docs/explanation/architecture.md -->
# Architecture Overview

``` mermaid
flowchart TD
  A[Inventory Excel Worksheet With Data From PDWiz] --> B["Separate Tables For Millwork Inventory, Manufacture Labor, Install Labor & External Items"];
  B --> F[Assembly Builder References Excel Tables For SKU #s];
  F --> G["Export Assemblies As PlanSwift Scripts (.psscript files)"];
  G --> H["Use #quot;Create Tools#quot; Millwork Plugin To Create Assemblies Via PlanSwift Scripts (.psscript files)"];
  
  B --> C[Import Each Excel Table's Data Into Microsoft Access Database Tables]
  C --> D[Import Microsoft Access Database Tables Into PlanSwift Lists];
  D --> E[Select From Dropdown List Properties When Creating Items];

  E --> I;
  H --> I[Use Proper Assembly Structure To Create Items & Complete Takeoffs];
  I --> J[Use Job Margin Values, Takeoff Measurements & Item Cost Data To Generate A Variety Of PlanSwift Reports];
  J --> K[Use PlanSwift Reports To Create Quotes]
```