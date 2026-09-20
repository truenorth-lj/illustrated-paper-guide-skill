# Illustrated Paper Guide Skills

[![skills.sh](https://img.shields.io/badge/skills.sh-install-blue)](https://www.skills.sh/truenorth-lj/illustrated-paper-guide-skill/illustrated-paper-guide)
[![ClawHub](https://img.shields.io/badge/ClawHub-install-purple)](https://clawhub.ai/illustrated-paper-guide/skills/illustrated-paper-guide)
[![License: MIT-0](https://img.shields.io/badge/License-MIT--0-green)](LICENSE)

A small, portable skill suite for turning academic papers into illustrated,
checkpoint-based study guides.

The repository contains two related but independently useful skills:

| Skill | Responsibility |
| --- | --- |
| `illustrated-paper-guide` | Compares top-down reading paths, reviews source coverage, and builds or improves a durable paper-reading guide with checkpoints, figure explanations, limitations, and Q&A write-back. |
| `teaching-diagram-maker` | Creates and visually verifies editable teaching diagrams for mechanisms, comparisons, timelines, pathways, and causal chains. |

`illustrated-paper-guide` uses `teaching-diagram-maker` whenever a custom
teaching diagram would materially improve understanding. Both are bundled in
this repository so they can be installed together.

## Install

```bash
# Install both skills interactively
npx skills add truenorth-lj/illustrated-paper-guide-skill

# Or select one skill
npx skills add truenorth-lj/illustrated-paper-guide-skill --skill illustrated-paper-guide
npx skills add truenorth-lj/illustrated-paper-guide-skill --skill teaching-diagram-maker
```

For a manual installation, copy both directories under `skills/` into the
skills directory used by your agent host. For example:

```bash
cp -R skills/illustrated-paper-guide ~/.agents/skills/
cp -R skills/teaching-diagram-maker ~/.agents/skills/
```

For OpenClaw, the skills are also available separately through ClawHub:

```bash
clawhub install illustrated-paper-guide
clawhub install teaching-diagram-maker
```

Verified registry pages:

| Skill | skills.sh | ClawHub |
| --- | --- | --- |
| `illustrated-paper-guide` | [View on skills.sh](https://www.skills.sh/truenorth-lj/illustrated-paper-guide-skill/illustrated-paper-guide) | [View on ClawHub](https://clawhub.ai/illustrated-paper-guide/skills/illustrated-paper-guide) |
| `teaching-diagram-maker` | [View on skills.sh](https://www.skills.sh/truenorth-lj/illustrated-paper-guide-skill/teaching-diagram-maker) | [View on ClawHub](https://clawhub.ai/illustrated-paper-guide/skills/teaching-diagram-maker) |

## Usage

Example requests for `illustrated-paper-guide`:

- “Turn this PDF into a study guide I can finish in checkpoints.”
- “Compare several reading plans and give me the fastest route that still covers every major claim.”
- “Explain every panel in Figure 3 and show how it supports the claim.”
- “Add a big-picture section and a linked reading checklist to these notes.”
- “Write my follow-up explanation back into the relevant section.”

Example requests for `teaching-diagram-maker`:

- “Draw an editable diagram of this signaling pathway.”
- “Compare these three models in one teaching figure.”
- “Fix the clipping and unreadable labels in this SVG.”

## Method

The suite follows six principles:

1. Give the reader the problem, method, and conclusion before details.
2. Compare genuinely different candidate reading routes for a new full guide,
   then synthesize and review one shallow-to-deep route.
3. Optimize early understanding by reordering rather than silently omitting
   source material.
4. Separate source evidence, interpretation, and open questions.
5. Explain figures from visible evidence instead of jumping to conclusions.
6. Preserve new understanding in the note, not only in chat history.

Route competition is adaptive: focused follow-ups stay single-reader; a
typical new guide uses two route readers; complex reviews or dense theory add a
dedicated source reviewer. A third route is reserved for explicit three-way
comparison requests. The guide headings stabilize before the learner checklist
is generated, while a separate coverage ledger lets a source reviewer detect
omissions without making the checklist unwieldy.

The paper skill creates the learning structure. The diagram skill owns diagram
craft and visual verification. This boundary keeps both skills focused while
allowing them to compose cleanly.

## Repository Structure

```text
AGENTS.md
README.md
LICENSE
skills/
├── illustrated-paper-guide/
│   ├── SKILL.md
│   ├── meta.json
│   ├── agents/openai.yaml
│   └── references/
│       ├── figure-reading-rubric.md
│       ├── paper-guide-template.md
│       └── reading-path-competition.md
└── teaching-diagram-maker/
    ├── SKILL.md
    ├── meta.json
    └── agents/openai.yaml
scripts/
└── validate_package.py
```

No papers, publisher figures, private notes, or source-project files are
included. Users remain responsible for the licenses and permissions governing
the papers and images they process.

## Validation

```bash
./scripts/validate_package.py
```

The validator checks frontmatter, metadata, required files, bundled dependency
references, accidental private paths, obvious unfinished markers, and bundled
binary paper assets.

## Security and Privacy

The published repository is built from a clean release snapshot. It contains
no paper files, publisher images, private notes, credentials, contact details,
absolute user paths, or source-project history. The package validator checks
for common privacy regressions and the repository is scanned for secrets before
release.

## License

MIT-0 (MIT No Attribution). See [LICENSE](LICENSE).
