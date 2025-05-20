<!-- docs/explanation/versioning-workflow.md -->
# Versioning & Release Workflow

| Artifact | Versioning rule | Example |
|----------|-----------------|---------|
| **Plugin (.pszip)** | SemVer, bump *minor* on inventory change, *major* on schema change | 2.1.0 |
| **Assembly Builder** | SemVer, bump *patch* for bugfix | 1.3.2 |
| **Inventory sheet** | Date-stamped filename | inventory_2025-05-16.xlsx |

Process:

1. Update inventory → commit sheet.  
2. Run CI to generate new assemblies & plugin build.  
3. Tag Git release.  
4. Publish on portal; update **Changelog**.

