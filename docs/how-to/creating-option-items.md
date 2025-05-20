## Use-case

You need to include an external item in an Assembly.

## Add External Items To PlanSwift List Database

=== "Demo"
    ![type:video](../assets/video/addingoptionstolist.mp4){: .mx-auto preload="metadata" .no-glb }


=== "Flowchart"
    ``` mermaid
    flowchart TD
      A[Create & Name Folder] --> B[Create & Name Assembly Item];
      B --> C[Set Qty Per Count];
      C --> D["Add Child Item (Material, Part or Labor) to Assembly Item"];
      D -- Optional --> E[Use Helpful Name Formula];
      D --> F;
      E --> F[Search & Select SKU Inventory Item From Selected Item Dropdown];
      F --> G[Confirm Parent/Child Assembly Structure];
      G -- Optional --> H[Drag & Drop Assembly Into Template For Later Use];
    ```

## Add "Other" (Option) Items To Takeoff Assembly Item

=== "Demo"
    ![type:video](../assets/video/creatingoptionitems.mp4){: .mx-auto preload="metadata" .no-glb }

=== "Flowchart"
    ``` mermaid
    flowchart TD
      A[Create & Name Folder] --> B[Create & Name Assembly Item];
      B --> C[Set Qty Per Count];
      C --> D["Add Child Item (Material, Part or Labor) to Assembly Item"];
      D -- Optional --> E[Use Helpful Name Formula];
      D --> F;
      E --> F[Search & Select SKU Inventory Item From Selected Item Dropdown];
      F --> G[Confirm Parent/Child Assembly Structure];
      G -- Optional --> H[Drag & Drop Assembly Into Template For Later Use];
    ```

## Display Options Data With PlanSwift Reports

=== "Demo"
    ![type:video](../assets/video/optionsreportdata.mp4){: .mx-auto preload="metadata" .no-glb }

=== "Flowchart"
    ``` mermaid
    flowchart TD
      A[Create & Name Folder] --> B[Create & Name Assembly Item];
      B --> C[Set Qty Per Count];
      C --> D["Add Child Item (Material, Part or Labor) to Assembly Item"];
      D -- Optional --> E[Use Helpful Name Formula];
      D --> F;
      E --> F[Search & Select SKU Inventory Item From Selected Item Dropdown];
      F --> G[Confirm Parent/Child Assembly Structure];
      G -- Optional --> H[Drag & Drop Assembly Into Template For Later Use];
    ```