---
name: ts-docs-creator
description: Create or update Python project documentation using Diataxis. Use when asked to map content to Tutorial/How-to/Reference/Explanation, add YAML-frontmatter pages, generate API docs with Sphinx, publish with VitePress, enforce category-specific writing rules, and validate doc quality with a checklist.
---

# ts-docs-creator

Generate project-agnostic documentation for Python projects using Diataxis and a Sphinx-to-VitePress publishing workflow.

## Scope

- Apply this skill to Python projects.
- Keep instructions project-agnostic and reusable.
- Prefer public package interfaces and stable docs structure over project-specific assumptions.

## Bundled Resources

- `scripts/docs_pipeline.py`: Placeholder pipeline runner for Sphinx + VitePress commands.
- `assets/page-template.md`: Reusable page template for Tutorial and How-to drafting.
- `examples/tutorial-example.md`: Reference tutorial page showing expected structure and linking style.

## Required Pre-Read

- Read `docs/` to understand current information architecture and style.
- Read package source to identify public APIs and canonical naming.
- Read existing examples in `examples/` to link tutorials to runnable code.
- Read docs tool config (`pyproject.toml`, `conf.py`, `.vitepress/config.ts`) if present.

## Workflow

1. Classify each page request into exactly one Diataxis category.
2. Draft or update content using `assets/page-template.md` and category-specific writing rules.
3. Add `Developer Notes` for complex technique choices where needed.
4. Ensure Tutorial pages cross-reference relevant files in `examples/`.
5. Generate API docs with Sphinx into `docs/reference/api/` (use `scripts/docs_pipeline.py` as a command wrapper if helpful).
6. Configure and build VitePress with generated API docs included in nav/sidebar.
7. Run checklist validation before finalizing.

## Output Standards

### Diataxis Mapping

Assign every page to exactly one Diataxis category:

| Category | Orientation | Location | Title pattern |
| --- | --- | --- | --- |
| Tutorial | Learning | `docs/tutorial/` | Verb phrase |
| How-to Guide | Goal | `docs/how-to/` | `How to <action>` |
| Reference | Information | `docs/reference/` | Noun phrase |
| Explanation | Understanding | `docs/explanation/` | `About <concept>` or `<Concept> Explained` |

Recommended top-level sections:

| Section | Location | Content |
| --- | --- | --- |
| Home | `docs/index.md` | Overview, quick links, minimal example |
| Getting Started | `docs/getting-started/` | Installation, quick start, architecture |
| Development | `docs/development/` | Contributing, testing, release process |
| Changelog | `docs/changelog.md` | Version history |

### Directory Structure

Use this baseline layout:

```text
docs/
├── index.md
├── changelog.md
├── getting-started/
│   ├── installation.md
│   ├── quick-start.md
│   └── architecture.md
├── tutorial/
├── how-to/
├── explanation/
├── reference/
│   ├── index.md
│   ├── api/            # Sphinx-generated API docs
│   └── *.md            # hand-written reference pages
└── development/
    ├── contributing.md
    ├── testing.md
    └── release.md
```

### Page Template

Start each page with frontmatter and this skeleton:

```markdown
---
title: <Page Title>
description: <One-sentence summary for search and metadata>
---

# <Page Title>

<Opening paragraph: 2-3 sentences of context.>

## Prerequisites

- <Required knowledge/tools; skip for pure reference pages>

## <Main Content Sections>

...

## Next Steps

- [Related page](../category/page.md)
```

### Developer Notes

Add a `Developer Notes` section when a page includes complex implementation choices.

- Explain why a technique was chosen (trade-offs, constraints, alternatives considered).
- Document non-obvious aims (performance, compatibility, safety, or maintainability goals).
- Keep this section concise and technical; do not repeat tutorial steps.
- Place it near the end of the page, before `Next Steps` when present.

### Sphinx and VitePress Workflow

- Use Sphinx to auto-generate API markdown into `docs/reference/api/`.
- Treat generated API files as build artifacts; do not hand-edit generated content.
- Write conceptual and task-oriented pages manually under Diataxis directories.
- Publish the full docs site with VitePress, including generated API pages in navigation.
- Verify internal links from tutorials/how-to/reference pages to generated API pages.

### VitePress Configuration

Configure VitePress in `docs/.vitepress/config.ts` and keep navigation aligned with Diataxis directories.

```ts
import { defineConfig } from "vitepress";

export default defineConfig({
  title: "Project Docs",
  description: "Documentation site",
  srcDir: ".",
  outDir: ".vitepress/dist",
  cleanUrls: true,
  lastUpdated: true,
  themeConfig: {
    nav: [
      { text: "Guide", link: "/getting-started/quick-start" },
      { text: "Tutorial", link: "/tutorial/" },
      { text: "How-to", link: "/how-to/" },
      { text: "Reference", link: "/reference/" },
      { text: "Explanation", link: "/explanation/" },
    ],
    sidebar: {
      "/tutorial/": [
        {
          text: "Tutorial",
          items: [{ text: "Overview", link: "/tutorial/" }],
        },
      ],
      "/how-to/": [
        {
          text: "How-to",
          items: [{ text: "Overview", link: "/how-to/" }],
        },
      ],
      "/reference/": [
        {
          text: "Reference",
          items: [
            { text: "Overview", link: "/reference/" },
            { text: "API", link: "/reference/api/" },
          ],
        },
      ],
      "/explanation/": [
        {
          text: "Explanation",
          items: [{ text: "Overview", link: "/explanation/" }],
        },
      ],
    },
    search: {
      provider: "local",
    },
    socialLinks: [{ icon: "github", link: "https://github.com/org/repo" }],
  },
  sitemap: {
    hostname: "https://docs.example.com",
  },
});
```

Configuration rules:

- Keep `srcDir` rooted at the docs folder that contains markdown sources.
- Include `reference/api/` in sidebar so generated API pages are discoverable.
- Treat `reference/api/` as generated content and regenerate it during docs build.
- Keep `cleanUrls` and `lastUpdated` enabled unless project constraints require otherwise.
- Use relative internal links and avoid hard-coding local filesystem paths.
- Update `sitemap.hostname` and `socialLinks` to match the target project.

Build and publish pattern:

- Regenerate API docs with Sphinx first.
- Run VitePress build against the same docs tree.
- Publish output from `.vitepress/dist` (or configured output directory).
- Fail CI when link-checking or docs build fails.

### Category-Specific Writing Rules

#### Tutorials

- Use first-person plural voice.
- Present numbered, step-by-step flow.
- Include runnable examples and expected output for major steps.
- Cross-reference relevant files in `examples/` for each tutorial workflow step.
- Keep scope to one workflow.
- Defer deep theory to Explanation pages.
- End with a short outcome summary and next steps.

#### How-to Guides

- Start titles with `How to`.
- Use imperative voice.
- Assume reader competence.
- Show conditional branches explicitly.
- Keep concise while complete.

#### Reference

- Use neutral, factual tone.
- Prefer tables and definition lists over long prose.
- Document all public interfaces and parameters.
- Keep generated API docs separate from hand-written guides.

#### Explanation

- Focus on rationale, trade-offs, and conceptual models.
- Avoid procedural steps.
- Avoid duplicating reference parameter tables.

### Code Samples

For code in docs:

- Always specify a language fence (`python` by default for this skill).
- Keep snippets copy-paste runnable where possible.
- Use the project's unified wrapper/public facade when one exists.
- Avoid private internals and direct backend/vendor SDK imports unless explicitly documenting low-level behavior.
- Include type annotations.
- Follow project formatter/linter expectations.

Example:

```python
from package_name import Client


def main() -> None:
    client = Client.connect("endpoint")
    result = client.ping()
    print(result)


if __name__ == "__main__":
    main()
```

### Cross-Referencing

- Use relative links for internal docs.
- Link APIs to generated reference pages when available.
- In Tutorial pages, link examples to source files in `examples/` for direct runnable follow-up.
- Avoid absolute filesystem paths.
- Use lowercase hyphenated anchors.

### Terminology Policy

- Define a glossary for domain-specific terms.
- Use one canonical term per concept.
- Avoid synonyms that create ambiguity.
- Keep naming consistent across tutorials, how-to, reference, and explanation pages.

### Markdown Style

- Use ATX headings (`#`).
- Keep one blank line around headings and lists.
- Use `-` for unordered lists and `1.` for ordered lists.
- Align tables with a valid header separator.
- Soft-wrap prose near 80-100 columns.
- Remove trailing whitespace.
- Ensure final newline exists.
- Wrap inline code symbols in backticks.

## Quality Checklist

- [ ] Frontmatter includes `title` and `description`
- [ ] Page fits exactly one Diataxis category
- [ ] Title matches category naming convention
- [ ] Category-specific voice and structure rules are followed
- [ ] `Developer Notes` is included where complex technique decisions need explanation
- [ ] Sphinx-generated API docs are current and not hand-edited
- [ ] VitePress navigation includes generated API reference pages
- [ ] Tutorials cross-reference relevant files in `examples/`
- [ ] Code samples use the unified wrapper/public facade and are runnable
- [ ] Internal links are relative and valid
- [ ] Terminology is consistent with glossary
- [ ] Markdown formatting is clean (no trailing spaces, final newline)
- [ ] Tables render with proper header separators
