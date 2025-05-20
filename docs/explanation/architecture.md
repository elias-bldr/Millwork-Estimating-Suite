<!-- docs/explanation/architecture.md -->
# Architecture Overview

``` mermaid
flowchart TD
  A[Inventory Excel] --> B[Assembly Builder];
  B --> C[.psscript];
  C --> D(["<img src='/assets/video/createjob.webp'>"]);
  D -->|Imports Lists| E[PlanSwift DB];
  D -->|Generates Reports| F[PDF Quote];
```

Assembly Builder: stateless; reads Excel, writes script.

Plugin: static bundle; ships lists & layouts.

PlanSwift: runtime environment + reporting.

yaml
Copy
Edit

---