# Commit `2a10047` workflow incident

**Checked:** 2026-10-05 22:00 UTC after both retries completed. **Commit:** `2a100478dbcefe366953878104b9be136936d404`.

| Workflow | Run | First attempt | Current retry |
|---|---|---|---|
| [Python tests](https://github.com/dyplux/bnb-tokenized-stocks-2026/actions/runs/37368620035) | `37368620035` | Job `test` was cancelled at 20:30:39 UTC before a runner or step was assigned. The job API has `runner_name=""` and `steps=[]`; there is no failed test line or step log. | Attempt 2 also ended `cancelled`, with `runner_name=""` and `steps=[]`. No Python test ran on GitHub. |
| [Pages build and deployment](https://github.com/dyplux/bnb-tokenized-stocks-2026/actions/runs/37368619406) | `37368619406` | Job `build` was cancelled at 20:30:40 UTC before a runner or step was assigned. The `deploy` job was skipped; the report job was also cancelled. No build step log exists. | Attempt 2 also cancelled `build` and `report-build-status` before runner assignment; `deploy` was skipped. No Pages build ran. |

[GitHub Status](https://www.githubstatus.com/) reported `Actions: major_outage` at 20:51 UTC, with an active incident under investigation. A later 5 October read showed Actions operational and Pages degraded. That is consistent with the pre-runner cancellations but doesn't prove a specific internal cause. The older Pages run `37360300696` belongs to `1576d647` and wasn't rerun.

The repository's exact CI command, `python3 -m unittest discover -s tests -q`, passed locally on 5 October: **133 tests, 0 failures**. A fresh shallow clone of the public repository at `2a10047` passed the same 133 tests on the SSD. These are local results, not a successful GitHub Actions run. The old public judge page, both observed receipt JSON files and the MP4 returned signed-out HTTP 200, and each downloaded body matched the corresponding local `/docs` file SHA-256. A successful Pages deployment of `2a10047` remains unconfirmed. The public static page content itself didn't change in that commit; the new Monday findings and claim set are repository documents.

**Next check:** obtain a successful runner-backed Python run and Pages deployment for the exact final submission SHA, then check the page, video and receipt URLs without authentication and compare their hashes. The second attempts don't provide code-failure evidence. Keep the existing judge URL in submission materials throughout.
