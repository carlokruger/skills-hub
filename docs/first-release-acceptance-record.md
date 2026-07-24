# First-release acceptance record

Status: **passed — Carlo explicitly confirmed the VM test on 2026-07-24**

This record is completed for an untagged public candidate. Do not create a v1 tag or release until every field is redacted as needed, completed, and Carlo explicitly confirms the VM run.

| Evidence | Record |
| --- | --- |
| Candidate commit SHA | `f55b99a4d5f8552eb4330176460e1abe436d67d6` |
| Downloaded GitHub ZIP SHA-256 | `0cc2f8836a93ae681f88de62897d086f007e51756b2d49320fa9cb64236720d1` |
| Reference acceptance profile | `carlo-baseline` |
| VM environment | Fresh macOS/zsh VM; passed (Carlo-confirmed) |
| Bootstrap command and summary | `./scripts/bootstrap --profile carlo-baseline`; passed (Carlo-confirmed) |
| Pinned Source verification | Passed for all nine manifest Sources (Carlo-confirmed) |
| Installed-link audit | Passed for the `carlo-baseline` selection (Carlo-confirmed) |
| Tracked-files, credential, and ignored-Source boundary scan | Passed locally and in a fresh public clone; no forbidden tracked paths |
| Carlo's explicit confirmation | Confirmed: “test passes” on 2026-07-24 |

The public-first boundary exception applied to this candidate: the tracked-file, credential, and ignored-Source assertions ran after push and passed. A future failed scan, bootstrap, restore, profile application, link audit, or VM run requires a remediated candidate and a new record.
