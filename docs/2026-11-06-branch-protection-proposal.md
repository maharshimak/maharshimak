# Core MAK'MA GitHub default-branch protection proposal

**Snapshot:** 2026-11-06, read-only inspection. **Status:** proposal only; zero repository settings changed.

This proposal covers the ten public core repositories. Do not change repository visibility, history, branch settings, deployment configuration or publishing environments without the owner's separate authorization. Private repos are deliberately out of scope.

## Verified targets

| Repository | Default branch | Observed SHA | Protected? | Candidate existing CI job names |
| --- | --- | --- | --- | --- |
| [maharshimak](https://github.com/maharshimak/maharshimak) | `main` | `f1ae23216657` | **No** | `validate-profile`, `gitleaks`, `reachable-history-scan` |
| [makma-ai-os](https://github.com/maharshimak/makma-ai-os) | `main` | `427ba5774f8e` | **No** | `quality`, `gitleaks`, `integration`, `verify` |
| [agentic-rag-engine](https://github.com/maharshimak/agentic-rag-engine) | `main` | `4eb25f6d91dd` | **No** | `quality`, `gitleaks` |
| [multimodal-ai-studio](https://github.com/maharshimak/multimodal-ai-studio) | `main` | `56cb15eb40e3` | **No** | `quality`, `gitleaks` |
| [knowledge-twin](https://github.com/maharshimak/knowledge-twin) | `main` | `ef18b11342bf` | **No** | `quality`, `gitleaks` |
| [clinical-document-intelligence](https://github.com/maharshimak/clinical-document-intelligence) | `main` | `ae9ab50407c2` | **No** | `quality`, `gitleaks` |
| [secure-data-copilot](https://github.com/maharshimak/secure-data-copilot) | `main` | `46be63dae698` | **No** | `quality`, `gitleaks` |
| [llm-eval-observability](https://github.com/maharshimak/llm-eval-observability) | `main` | `72535c7513d2` | **No** | `quality`, `gitleaks` |
| [mlops-control-plane](https://github.com/maharshimak/mlops-control-plane) | `main` | `1d8c6dad79fa` | **No** | `quality`, `gitleaks` |
| [mlops-production-pipeline](https://github.com/maharshimak/mlops-production-pipeline) | `main` | `0631b10a83cf` | **No** | `quality`, `gitleaks` |

The candidate names above come from current workflow job identifiers, **not** from ruleset settings. Before requiring any job, inspect the exact check name exposed by a real PR and confirm that it reliably runs on `pull_request`. Do **not** add a nonexistent, scheduled-only or intentionally skipped job as a required check.

## Proposed ruleset: `core-main-review-gate`

Use one repository-specific ruleset for each public `main`; configure in GitHub Settings > Rules > Rulesets. Apply to `main` only (not feature, experimental or draft branches).

1. Require a pull request for updates to `main`. Maintain draft PRs for experimental work.
2. Block force-push and branch deletion, including accidental admin operations if supported.
3. Require successful, current, relevant CI checks at the exact reviewed head. Start with `quality` and `gitleaks` for the eight specialist repos; for AI OS evaluate `integration` and the Pages `verify` job as well; for the profile use `validate-profile`, `gitleaks` and `reachable-history-scan` after the scanner fix.
4. Require conversation resolution before merging if the account plan supports it.
5. Require an independent human review **only if a qualified non-author reviewer exists**. A one-person repository owner cannot approve their own PR; indiscriminately requiring one approval would create a merge deadlock. Preserve the owner's explicit merge decision and add a collaborator/reviewer deliberately before enabling mandatory approval count.
6. Minimize bypass actors and document any emergency owner-only bypass. Prefer no bypass for force-push/deletion. Recheck team/account plan feature support before activation.
7. Do not allow push-time auto-deployment of MAK'MA Pages merely because CI succeeds. The already-reviewed workflow requires an explicit main-branch `workflow_dispatch`; keep publishing separate from normal verification.
8. Apply protections one repository at a time, beginning with a non-critical public specialist repo, validating real draft-PR behavior and rollback of **settings only after a separate authorization**. Do not batch-enable untested rulesets.

## Check-name considerations

- Every specialist uses Python CI (`quality`) and Security history scan (`gitleaks`). Multimodal's `real-ffmpeg` can become required only after confirming availability and dependable PR execution.
- AI OS also has Cross-system integration (`integration`) and Pages verification (`verify`). Its `deploy` and `live-e2e` jobs are intentionally skipped for ordinary PRs and **must not** be required merge checks.
- The profile's scheduled security audit was failing on synthetic test fixtures until draft [#68](https://github.com/maharshimak/maharshimak/pull/68). Do not activate its history-scan requirement until the fix is reviewed/merged and CI on `main` is green.
- Prevent stale required-check names when Dependabot upgrades GitHub Actions. Validate each required check by its GitHub UI display name.
- Enforce no production release from a draft PR; any merge and any publishing require distinct explicit owner approvals.

## Activation checklist — owner gated

- [ ] Owner confirms the ten repository targets and the exact ruleset design.
- [ ] Confirm the account supports each enforcement feature; keep private repositories private.
- [ ] Confirm one real PR produces every proposed required check.
- [ ] Review branch bypass actors, administrator restrictions, and solo-maintainer review lockout.
- [ ] Activate one canary ruleset and prove PR checks/rejection behavior.
- [ ] Reassess before enabling the other nine.
- [ ] Record final ruleset IDs and an export of settings after separately approved activation.

**No ruleset, branch protection, repository visibility, or deployment setting was changed by this proposal.**
