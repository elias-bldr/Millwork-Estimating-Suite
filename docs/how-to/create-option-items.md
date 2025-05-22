<!-- docs/how-to/create-option-items.md -->

## Use-case

You need to include an external item in an Assembly.

## Add External Items To PlanSwift List Database

=== "Demo"
    ![type:video](../assets/video/addingoptionstolist.mp4){: .mx-auto preload="metadata" .no-glb }


=== "Flowchart"
    ``` mermaid
    flowchart TD
      A[Navigate To Lists Tab] --> B[Find Millwork Databases List Item];
      B --> C[Access External Items Costs Table];
      C --> D[Use Green + Button To Create A New Entry];
      D --> E[Enter SKU #, Description & Date Data For Your New Entry];
      E --> F[Click Check Mark To Save Your Changes];
      F --> G["Create Your #quot;Other#quot; Type Option Item"];
    ```

## Add "Other" (Option) Items To Takeoff Assembly Item

=== "Demo"
    ![type:video](../assets/video/creatingoptionitems.mp4){: .mx-auto preload="metadata" .no-glb }

=== "Flowchart"
    ``` mermaid
    flowchart TD
      A[Create Your Desired Assembly Structure] -- IF NEEDED --> B[Credit Material Via The Material Form];
      A --> C;
      B --> C[Add The External #quot;Other#quot; Type Item To The Assembly];
      C --> D[Verify Qty Per Count & Cost/Pricing Values Are Correct In Estimating Tab];
    ```

## Display Options Data With PlanSwift Reports

=== "Demo"
    ![type:video](../assets/video/optionsreportdata.mp4){: .mx-auto preload="metadata" .no-glb }

=== "Flowchart"
    ``` mermaid
    flowchart TD
      A[Navigate To The Reports Tab] --> B[Select The Millwork Option/Credit By Folder Report];
      B --> C[Review Data Displayed On The Report];
    ```