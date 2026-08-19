# komodo-config

Centralized [Komodo](https://komo.do) Resource Sync declarations for all stacks managed by `broomej`.

This repo is the single source of truth for **what** Komodo deploys and **how** each stack is parameterized (env vars, file paths, branches). The actual `compose.yaml` files live in their respective app repos (e.g. [`broomej/servarr`](https://github.com/broomej/servarr)) — this repo just tells Komodo how to point at them.

## Layout

```
.
├── sync.toml                  # Top-level Resource Sync declaration (points back at this repo)
├── stacks/
│   ├── jellyfin.toml           # Prod stack: jellyfin (servarr / main)
│   └── jellyfin-dev.toml       # Dev stack: jellyfin-dev (servarr / dev branch)
└── .github/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
        └── validate-toml.yml   # CI: parse-checks every .toml in this repo
```

## Two-environment model

For every app we manage, we declare two Stack resources in TOML:

| Environment | Stack name       | Source repo           | Branch | Compose files                              | Project name    |
|-------------|------------------|-----------------------|--------|--------------------------------------------|-----------------|
| Prod        | `jellyfin`       | `broomej/servarr`     | `main` | `compose.yaml`                             | `jellyfin`      |
| Dev         | `jellyfin-dev`   | `broomej/servarr`     | `dev`  | `compose.yaml` + `compose.dev.yaml`        | `jellyfin-dev`  |

- The dev stack applies `compose.dev.yaml` **on top of** `compose.yaml` (Docker Compose override semantics).
- The dev override changes `container_name`, `ports`, `volumes` (separate config/cache, `${SERVARR_DATA}` mounted read-only), and keeps GPU access for testing NVIDIA runtime changes.
- Prod and dev have **separate project names**, so they get separate default networks, separate volumes, and never collide.

## Workflow (the whole point of this repo)

```
          ┌────────────────────────────────────────────────────────────┐
          │  1. Cut feature branch off `dev` in broomej/servarr        │
          │  2. Edit compose.yaml and/or compose.dev.yaml              │
          │  3. Open PR  →  GitHub Actions runs `docker compose config`│
          │  4. Merge PR into `dev`                                    │
          │  5. Komodo webhook fires → syncs this repo                 │
          │  6. Komodo redeploys the `jellyfin-dev` stack              │
          │  7. Manually verify dev at http://<tailnet>:8097           │
          │  8. Open PR  `dev → main`                                  │
          │  9. Branch protection requires PR review (self-merge ok)   │
          │ 10. Merge → Komodo redeploys `jellyfin` (prod)             │
          └────────────────────────────────────────────────────────────┘
```

The `main` branch of `broomej/servarr` has branch protection: **no direct pushes**, PRs only. The `dev` branch can take direct pushes if you want to move fast — Komodo will redeploy on every push.

## Adding a new app

1. Add the app's compose to the relevant app repo (e.g. `servarr/compose.yaml` gets a new service, or a new repo is created).
2. Add `stacks/<app>.toml` (prod) and `stacks/<app>-dev.toml` (dev) here, following the jellyfin pair as a template.
3. Add variables and secrets to Komodo's environment in the UI (never commit secrets here).
4. Commit and push. Komodo will pick up the new resources on next sync.

## Secrets

**Never commit secrets to this repo.** The `.env.example` file documents what Komodo needs; the real values live in:

- Komodo Core's environment (for `KOMODO_GITHUB_ACCOUNT` / token used to clone private repos), **or**
- Komodo Variables marked as `secret = true` (rendered as `[[VAR_NAME]]` in stack environment strings).

See `variables.toml` for the pattern.

## CI

`validate-toml.yml` runs on every PR against this repo. It parses every `.toml` file and fails on syntax errors before Komodo ever sees the file. Komodo itself will reject malformed TOML, but the CI gives you a faster feedback loop and a clear error in the PR check.

## Reference

- Komodo Resource Sync docs: https://komo.do/docs/sync-resources
- Stack config schema: https://docs.rs/komodo_client/latest/komodo_client/entities/stack/struct.StackConfig.html
- ResourceSync config schema: https://docs.rs/komodo_client/latest/komodo_client/entities/sync/struct.ResourceSyncConfig.html
