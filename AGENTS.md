# Illustrated Paper Guide Skill Suite

This repository is a public, portable two-skill package.

## Skills

- `skills/illustrated-paper-guide/`: paper-reading guide structure and figure interpretation.
- `skills/teaching-diagram-maker/`: editable teaching-diagram creation and visual QA.

The first skill may invoke the second. Keep their responsibilities separate:
the paper skill decides when and where a diagram is needed; the diagram skill
owns how it is created and verified.

## Repository Rules

- Treat this `AGENTS.md` as the single source of truth for repository-level
  agent instructions. Do not add a duplicate `CLAUDE.md`.
- Keep both skills self-contained and usable outside the source workspace.
- Do not add private repository names, absolute user paths, personal notes,
  unpublished conversations, paper PDFs, or publisher-owned figure files.
- Use generic examples rather than references to private source documents.
- Keep source evidence, interpretation, and open questions distinguishable.
- Preserve the copyright-safety guidance when editing figure workflows.
- Run `./scripts/validate_package.py` after changes.
- Commit messages use `<type>: <summary>`.

## Release Layout

This is a monorepo. Each directory under `skills/` is independently installable
and contains its own `SKILL.md`, metadata, and OpenAI interface metadata.
