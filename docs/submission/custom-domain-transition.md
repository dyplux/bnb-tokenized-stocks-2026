# `rwa.dyplux.com` transition plan

**Prepared:** 2026-10-05 UTC. **State:** plan only. No DNS, Pages project, repository Pages setting or live URL was changed. The existing judge URL remains `https://dyplux.github.io/bnb-tokenized-stocks-2026/`.

## Constraint and choice

The repository currently publishes `/docs` from `main` through GitHub Pages, with no custom domain configured. A branch-published GitHub Pages custom domain changes that site's domain configuration. To keep the existing project URL as an independent fallback while the new host is checked, publish the same static `/docs` directory to a **separate Cloudflare Pages project** and attach `rwa.dyplux.com` there. Do not add `docs/CNAME` or set a custom domain on the GitHub Pages repository.

Cloudflare supports a static HTML site with a chosen output directory and a project `*.pages.dev` URL. Its [custom-domain process](https://developers.cloudflare.com/pages/configuration/custom-domains/) requires associating the domain with the Pages project; for a zone already managed in Cloudflare it can create the CNAME during setup. The current GitHub Pages configuration stays untouched. [Cloudflare's static HTML guide](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/) describes a build with no framework and an output directory. [GitHub's Pages domain guide](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages) describes its separate custom-domain behavior.

## Execution order, after specific deployment approval

1. Confirm the GitHub Pages fallback, its MP4 and both observed JSON receipts load without authentication. Record HTTP status and receipt hashes. Check that `rwa.dyplux.com` has no conflicting DNS record immediately before setup. A 5 October read-only DNS check found no A or CNAME response, but that can change.
2. Create one Cloudflare Pages project linked to `dyplux/bnb-tokenized-stocks-2026`, production branch `main`, repository root as working directory, no framework, and `docs` as output directory. Use no build command if the dashboard permits it, or the documented no-op command `exit 0`. Do not inject Binance credentials or wallet keys. The public site is a static evidence packet.
3. Inspect the temporary `https://<project>.pages.dev/` before attaching the domain: page HTML, CSS, JavaScript, video, both observed receipts, their hashes, and the local judge-run link. Confirm the deployed commit matches the approved repository commit. Correct relative links only if this check finds a reproducible problem.
4. Add `rwa.dyplux.com` under that Cloudflare Pages project's **Custom domains**. Confirm the generated CNAME targets the project's `*.pages.dev` hostname. Wait for the domain to become active and for HTTPS to serve a valid certificate. Test `/`, `/media/execution-safety-judge-demo.mp4` and both `/judge/*.json` paths from a signed-out client. Verify the observed receipt hashes and no mixed-content or redirect loop.
5. Only after the HTTPS checks pass, offer the new URL in submission materials. Keep the GitHub Pages URL as a visible fallback link and monitor both through judging. Do not redirect the GitHub Pages URL or change its repository setting.

## Rollback and stop conditions

If the Pages project, CNAME or TLS check fails, leave the submission and video links on GitHub Pages. Remove the Cloudflare custom-domain association and its generated DNS record if a rollback is needed; the GitHub Pages project is unaffected. Do not cut over on a merely resolving DNS name or a certificate-warning page. The current GitHub Pages deployment is independently accessible even if the new host never launches.

**Current operational gate:** the 5 October GitHub Pages build for commit `2a10047` was cancelled before any build step during a reported GitHub Actions degradation. The old published page still returns HTTP 200. Confirm a successful final build or use the verified Cloudflare mirror before relying on a newer page revision.
