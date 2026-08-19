<!-- Thanks for contributing to komodo-config! Please fill in the sections below. -->

## What does this PR change?

<!-- Brief summary of the stacks / variables added, removed, or modified. -->

## Which environment does this affect?

- [ ] Prod (`stacks/<name>.toml`)
- [ ] Dev  (`stacks/<name>-dev.toml`)
- [ ] Both
- [ ] Neither — meta change (CI, README, sync.toml, etc.)

## Validation checklist

- [ ] `validate-toml` CI check passed
- [ ] TOML parses locally (`python -c "import tomli; tomli.load(open('stacks/your-file.toml','rb'))"`)
- [ ] If adding a new stack, the referenced compose file exists in the app repo
- [ ] If adding a new stack, `server` field matches a Komodo Periphery server that exists
- [ ] If changing env vars, `variables.toml` is updated (or a new Komodo Variable is added)
- [ ] No secrets committed (only `[[VAR]]` interpolation references)

## Related app-repo PR (if any)

<!-- If this PR is paired with a compose change in broomej/servarr or another
     app repo, link it here so reviewers can see both halves. -->

- broomej/servarr#____

## Rollback plan

- Revert this PR
- Komodo will re-sync on next push and restore the previous resource definitions
