# Architecture Diagrams

This directory contains Mermaid diagram source files (`.mmd`) and their PNG exports (`.png`) for the AI Video Violence Detection System.

## 📁 Diagram Files

| Diagram | Source File | PNG Export | Used In | Path Reference |
|---------|-------------|------------|---------|----------------|
| High-Level Architecture | `system-architecture-simple.mmd` | `system-architecture-simple.png` | `README.md` | `docs/diagrams/...` |
| Detailed Architecture | `system-architecture.mmd` | `system-architecture.png` | `README.md` | `docs/diagrams/...` |
| N-Tier System | `system-architecture-requirements.mmd` | `system-architecture-requirements.png` | `docs/02_requirements.md` | `diagrams/...` |
| N-Tier Implementation | `system-architecture-simple.mmd` | `system-architecture-simple.png` | `docs/05_technical.md` | `diagrams/...` |
| Target Architecture | `system-architecture-simple.mmd` | `system-architecture-simple.png` | `docs/06_architecture_plan.md` | `diagrams/...` |
| Database ERD | `database-erd.mmd` | `database-erd.png` | `docs/11_database_schema.md` | `diagrams/...` |

## 🔄 Workflow

### Editing Diagrams

1. **Edit the source file**: Modify the `.mmd` file (this is the single source of truth)
2. **Export to PNG**: Use one of the methods below
3. **Commit both files**: Commit both `.mmd` and `.png` files together

### Export Methods

#### Option 1: Mermaid CLI (Recommended - Automated)

```powershell
# Install Mermaid CLI (one-time)
npm install -g @mermaid-js/mermaid-cli

# Export single file with config
mmdc -i system-architecture.mmd -o system-architecture.png `
     -w 1920 -b white -c mermaid-config.json -s 2

# Export all files (from repository root)
Get-ChildItem docs\diagrams\*.mmd | ForEach-Object {
    $pngPath = $_.FullName -replace '\.mmd$', '.png'
    mmdc -i $_.FullName -o $pngPath `
         -w 1920 -b white `
         -c docs\diagrams\mermaid-config.json `
         -s 2
}
```

#### Option 2: Mermaid Live Editor (Manual)

1. Visit: https://mermaid.live/
2. Open the `.mmd` file and copy its content
3. Paste into the editor
4. Click "PNG" export button
5. Save to this directory with matching name

#### Option 3: VS Code Extension

1. Install: "Markdown Preview Mermaid Support"
2. Open `.mmd` file in VS Code
3. Preview the diagram
4. Right-click → Export as PNG
5. Save to this directory

## 📋 Best Practices

- **Single Source of Truth**: Always edit `.mmd` files, never edit PNGs directly
- **Consistent Naming**: PNG filename must match `.mmd` filename (e.g., `diagram.mmd` → `diagram.png`)
- **Commit Both**: Always commit both `.mmd` and `.png` files together
- **High Resolution**: Export at 1920px width or higher for professional quality
- **White Background**: Use white background for consistency (or transparent for dark mode)
- **Use Config File**: Always use `mermaid-config.json` for consistent styling

## 🔗 Path References in Markdown

**IMPORTANT:** Path references differ by file location:

- **From `README.md` (root):** Use `docs/diagrams/diagram.png`
- **From `docs/*.md` files:** Use `diagrams/diagram.png`

**Example in README.md:**
```markdown
![Diagram](docs/diagrams/system-architecture.png)
```

**Example in docs/02_requirements.md:**
```markdown
![Diagram](diagrams/system-architecture-requirements.png)
```

## 📝 Configuration

The `mermaid-config.json` file ensures consistent styling across all exports:
- Theme: default
- Colors: Project-specific color scheme
- Layout: Optimized for readability
- Scale: 2x for retina displays

## 📝 Notes

- PNG files are binary and tracked in git (see `.gitattributes`)
- ASCII fallbacks are maintained in markdown files for accessibility (wrapped in `<details>` tags)
- All diagrams use consistent color scheme matching project theme
- Total PNG size: ~180-780 KB (acceptable for repository)
