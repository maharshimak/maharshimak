# Portfolio and MAK'MA Pages deployment audit

**Date:** 2026-11-06. **Mode:** read-only. No deployment, rollback, promotion, workflow dispatch, environment change, or settings change was performed.

## Verified production endpoints

| Target | Live URL | Deployment evidence | Current serving status | Finding |
| --- | --- | --- | --- | --- |
| Tech Portfolio (Vercel) | https://maharshipatel-tech-portfolio.vercel.app/ | Vercel `dpl_HjjEiwMYyiFvyWqUVeaGiZPznwHk`, production READY, source `maharshimak/maharshi-tech-portfolio` branch `personalize`, commit `d508eeed12aee42401b859eddaf2fae60a55a6ca` | HTTP 200, HSTS present | Nov 4 restart-branding fix is the currently aliased production deployment. CSP response header was not observed. |
| Original portfolio (Vercel) | https://maharshipatel-portfolio.vercel.app/ | Vercel `dpl_J1zPaNrCgfKNpb9DybjQ4s3TeWdh`, production READY, deployed Sep 30 | HTTP 200, HSTS present | Older deployment. A CSP exists, but uses `unsafe-inline` / `unsafe-eval`. Do not assume newer source security patches are published. |
| MAK'MA Labs Projects (GitHub Pages) | https://maharshimak.github.io/makma-ai-os/projects/ | Latest GitHub Pages deployment `7036029686`, successful Oct 13 from `c533f1a6952e183b51321cf5290a5969d8e8ebb8` | HTTP 200, HSTS present | Live Pages is older than GitHub `main` `427ba5774f8e011cd17e2beb394981192f50377f` merged Nov 3. |

## Vercel additional checks

- Confirmed current Tech Portfolio production alias points at the Nov 4 `d508eeed` commit; Vercel build state is READY.
- Original portfolio Vercel project has no newer deployment in the available project deployment list after Sep 30.
- Vercel runtime-error queries for both portfolio projects returned **no runtime errors over the past seven days**. This does **not** measure client-side JS exceptions, accessibility, visual correctness, or third-party scripts.
- Tech Portfolio lacks an observed `Content-Security-Policy` header. Add one only after testing image/3D/worker/font and translation integrations on a branch; do not directly change production headers as part of this audit.
- Original portfolio's CSP is permissive for script execution; harden only with a reviewed Next.js compatibility plan and preview verification.

## MAK'MA GitHub Pages release gate

The current AI OS #25 workflow run `41853239202` completed verification successfully, but `deploy` and `live-e2e` jobs were **skipped** by design. Hence the Nov 3/4 code is **not** demonstrated on the public Pages route. The verification result must not be described as a production deployment.

Proposed owner-controlled release sequence, **not executed**:

1. Review and individually approve security PRs, their dependencies, CI, and the cross-repository `makma.v1` contract.
2. Require clean exact-head Python CI, security history scan, cross-system integration, and Pages artifact verification. Verify media and accessibility where relevant.
3. Verify the GitHub Pages environment protection and publishing token/permissions before any dispatch.
4. Only after a new explicit release authorization, dispatch the approved `main` Pages workflow, verify deployment SHA, then perform live E2E and visual/mobile/accessibility checks.
5. Confirm which experience is actually visible at `/projects/`; separate cinematic draft PR #23 remains unmerged and should not be silently promoted.

## Scope and limitations

- HTTP HEAD/response-header smoke checks were executed; **no new full interactive cross-browser walkthrough** was performed in this audit.
- This report does not assert that every link, video, animation, localized string, or user journey is bug-free.
- Vercel's older `makma-studio-site` project exists as a separate historical hosting record. It is **not** a release instruction for the user, who prefers GitHub Pages for Studio.
- Do not publish or change the private portfolio or Studio repositories, branch protections, domains, environment variables, or deployment targets without separate owner approval.
