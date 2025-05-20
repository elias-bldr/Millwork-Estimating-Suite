<!-- docs/reference/pascal-scripts.md -->
# Pascal Script Snippets

```pascal
procedure Main;
var
  itm: IItem;
begin
  itm := ItemManager.NewItem('Material');
  itm.Name := '1x4 Casing';
  itm.SetProperty('SKU', 'C1X4-PRM');
  itm.SetProperty('Cost Each', 1.15);
end;

Main;

Function                |   Purpose
NewItem(Type)	        |   Creates item of given millwork type
NavigateToLinkedPage()	|   Opens detail page (UI)