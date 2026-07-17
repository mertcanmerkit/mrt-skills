# Registry Contract

The registry ("playground") is the canonical index of the user's AI project network.

## Required Fields

Every registered project should have:

- project name
- role
- private GitHub URL
- local path
- read-first files
- usage/dispatch notes
- status
- last updated date

For design or Google Stitch-aware projects, include the durable design-control files in read-first entries when they exist:

- `source_of_truth/DESIGN.md`
- `source_of_truth/stitch-map.md`
- project-specific Stitch status docs such as `docs/12_stitch_status.md`

Usage notes for Stitch-aware projects must say that agents should use the recorded Stitch project/screen IDs and must not infer the current design from canvas position, generation order, or a vague "latest" label.

Usage notes must also preserve the model-selection rule: use the highest available usable Google Stitch model by default, practically Pro. Use Flash only when the user explicitly says to use Flash for Google Stitch. Do not infer Flash from project labels such as MVP, prototype, quick draft, early version, cheap, or low importance.

## Registry Files

- `docs/10_registered_projects.md`: human-readable registry.
- `docs/06_ai_system_registry.md`: canonical specialist system registry; reusable specialist projects can be appended here.
- `source_of_truth/registered_projects.json`: machine-readable registry.

## Privacy

Only private GitHub links should be added unless the user explicitly says public.
