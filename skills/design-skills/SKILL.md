---
name: design-skills
description: Curated registry and implementation engine for 67 UI/UX design systems (Bento, Shadcn, Claude, Neubrutalism, Glassmorphism, Material, etc.). Selects, inspects, and applies tokens, typography, colors, layouts, and accessibility constraints to any frontend.
---

# Design Skills System (67 UI/UX Design Systems)

This skill serves as your comprehensive design system consultant and implementation engine, powered by 67 curated design specifications imported from `awesome-design-skills` (TypeUI).

## Core Capabilities

1. **Aesthetic Matching & Recommendation**: Recommend the ideal visual design style based on project goals, audience, and mood.
2. **Token Inspection & Grounding**: Read and apply exact design tokens (hex palettes, typography scales, font pairings, spacing, radiuses) from `registry/<name>/DESIGN.md`.
3. **Frontend Implementation**: Translate tokens and component rules directly into production code (Tailwind CSS config, CSS variables, React/Vue/Svelte/HTML components).
4. **Accessibility & Quality Gates**: Enforce WCAG 2.2 AA standards, visible focus states, interactive states (hover/active/disabled), and high-contrast typography.

---

## Design System Taxonomy (67 Styles by Category)

### 1. Modern, Minimal & Clean
- **`bento`**: Modular grid layout with card blocks, soft spacing, and clear hierarchy (`#FAD4C0`, `#80A1C1`, `#FFF5E6`).
- **`shadcn`**: Minimalist utility-first design inspired by shadcn/ui with dark/light monochrome tokens (`#000000`, `#111111`, `#FFFFFF`).
- **`clean`**: Simplicity-focused layout with high whitespace, Roboto/Poppins, and minimal visual noise.
- **`minimal`**: Essentialist design with strict typography and whitespace discipline.
- **`sleek`**: Polished, modern high-tech interface with refined edges and subtle contrast.
- **`spacious`**: Breathing room, large padding/margins, and open layout grids.
- **`square`**: Sharp 0px corners, precise geometric borders, and technical grid aesthetics.
- **`modern`**: Contemporary web design baseline with balanced visual weight.

### 2. AI, Editorial & Publishing
- **`claude`**: Research-journal aesthetic on warm ivory stone (`#141413`, `#FAF9F6`), Anthropic Sans/Serif, zero shadows, flat buttons.
- **`codex`**: Blank-canvas edge-to-edge interface with stark monochrome contrast and pure typographic weight.
- **`agentic`**: Conversational AI-first interface with minimal chrome, clear delegated task flows, and warm accents (`#FF5701`).
- **`editorial`**: Magazine-grade serif layout (Gelasio/Ubuntu Mono), structured editorial columns, and reading focus.
- **`storytelling`**: Narrative-driven page progression, interactive chaptering, and rich typography.
- **`impeccable`**: Graphic editorial poster style with warm amber and burnt orange tones (`#CC8800`, `#C55221`).
- **`basic`**: Print-inspired visual language for books, annual reports, and publications.

### 3. Trendy, Glass & 3D Aesthetics
- **`glassmorphism`**: Frosted glass effects, translucent layers, backdrop blur, and luminous borders (`#1856FF`, `#3A344E`).
- **`claymorphism`**: Playful, puffy 3D shapes mimicking soft clay with gentle shadows and rounded corners.
- **`neumorphism`**: Soft extruded shapes with dual inner/outer shadows creating physical surface tactile depth.
- **`gradient`**: Vivid color transitions and smooth multidimensional mesh backgrounds (`#990FFA`, `#E60076`).
- **`neon`**: Cyberpunk glowing edges, dark canvases, and high-saturation neon strokes.
- **`futuristic`**: Sci-fi typography (Audiowide), tech accents, and forward-looking layouts.
- **`cosmic`**: Space/sci-fi dark mode with starfield depths and luminous accents.

### 4. Retro, Brutalist & Nostalgic
- **`brutalism`**: Raw, unadorned architectural anti-design with stark black lines, functional minimalism, and unpolished layouts.
- **`neobrutalism`**: High-energy brutalism with saturated block colors, thick black borders (2-4px), hard drop shadows (no blur), and quirky badges.
- **`skeumorphism`**: Realistic tactile textures, beveled edges, realistic lighting, and real-world metaphor controls.
- **`retro`**: Vintage 70s/80s computing aesthetics, warm analog vibes, and classic display fonts.
- **`vintage`**: Aged paper textures, antique typography, and heritage color schemes.
- **`dithered`**: Retro dot-pattern shading simulating monochrome/limited-palette displays.
- **`riso`**: Risograph print aesthetic with misaligned screens, vivid ink overlays, and grain.
- **`matrix`**: Hacker green phosphor terminal glow on pure obsidian canvas.
- **`pacman` / `tetris` / `sega`**: Arcade and 8/16-bit retro gaming motifs with pixel borders and primary color blocks.

### 5. Enterprise, Cloud & Data-Dense
- **`enterprise`**: Dark cloud platform aesthetic (GitHub/Vercel/Heroku vibe) with modular panels, status pills, and high information density (`#0C5CAB`).
- **`ant`**: Enterprise data-dense design system (Ant Design inspired) with Plus Jakarta Sans, compact tables, and robust forms (`#1677FF`).
- **`corporate`**: Polished enterprise brand presence with structured corporate blues and neutral grays.
- **`professional`**: Balanced B2B layout prioritizing trust, credibility, and clear visual hierarchy.
- **`material`**: Google Material Design elevation system, ripple states, and floating action surfaces.
- **`roku`**: TV/app ecosystem grid navigation with high-visibility remote/keyboard focus targets.
- **`levels`**: High-conversion landing page framework focusing on speed, trust badges, and friction removal.

### 6. Warm, Artistic & Expressive
- **`cafe`**: Warm earthy tones (`#5D4432`, `#E9E3DD`, `#F9F7F5`), cozy typography (Poppins), and soft organic hospitality vibes.
- **`terracotta`**: Mediterranean earthen clay, warm terracotta oranges, and sun-baked neutrals.
- **`doodle` / `sketch`**: Hand-drawn lines, sketch borders, notebook backgrounds, and playful character.
- **`paper`**: Textured stationery, card stock cards, deckled edges, and physical stationery feel.
- **`artistic`**: High-contrast, expressive typography (Limelight) for creative portfolios and exhibitions.
- **`vibrant` / `colorful` / `expressive`**: High-energy, saturated creative palettes celebrating personality and motion.

---

## Implementation Workflow

When asked to design a component, landing page, app, or UI system:

### Step 1: Select or Confirm Design Style
- If the user specifies a style (e.g., *"build a bento dashboard"* or *"use claude style"*), locate that style in `registry/<name>/`.
- If the user gives general requirements (e.g., *"make an enterprise monitoring dashboard"* or *"create a warm coffee shop app"*), recommend 2-3 fitting styles from the taxonomy above.

### Step 2: Read Exact Tokens
Inspect the style's `DESIGN.md` and `SKILL.md` under `registry/<name>/`:
- **Colors**: `primary`, `secondary`, `surface`, `text`, `neutral`, `success`, `warning`, `danger`
- **Typography**: Display font, body font, monospace font, font scale, font weights
- **Radiuses & Borders**: `rounded-sm`, `rounded-md`, border thickness
- **Spacing scale**: 4/8/12/16/24/32

### Step 3: Author Implementation Code
Apply the tokens into code:
1. Define tokens as CSS Custom Properties or Tailwind theme config:
```css
:root {
  --color-primary: #...;
  --color-surface: #...;
  --color-text: #...;
  --radius-sm: 4px;
  --radius-md: 8px;
}
```
2. Build UI components matching the brand aesthetic:
   - Match corner curvature, border styles, and drop shadows strictly to the specification.
   - Implement explicit interaction states: `:hover`, `:focus-visible`, `:active`, and `:disabled`.
   - Never use low-contrast text on colored surfaces; maintain WCAG AA minimum 4.5:1.

---

## Management & CLI Helper

A management script is bundled in `scripts/manage_skills.py`:

```bash
# List all 67 available design systems
python .agents/skills/design-skills/scripts/manage_skills.py list

# View exact tokens and design rationale for any style
python .agents/skills/design-skills/scripts/manage_skills.py info <style_name>

# Promote a specific style to a standalone top-level skill in .agents/skills/
python .agents/skills/design-skills/scripts/manage_skills.py promote <style_name>

# Remove a promoted style from top-level skills
python .agents/skills/design-skills/scripts/manage_skills.py demote <style_name>
```
