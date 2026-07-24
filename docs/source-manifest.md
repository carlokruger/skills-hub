# Source manifest contract

`sources.json` is schema-versioned JSON read with macOS `plutil`. Its stable lowercase Source IDs determine checkout paths: `sources/<source-id>`. Entries may not provide arbitrary local checkout paths.

Each Source records a public clone URL, a full 40-character lowercase commit SHA, an SPDX license identifier, a source-relative license path, and a `skills` object. That object is the complete allowlist for third-party skill exposure: each key is a stable Hub skill ID and each value is a source-relative directory containing `SKILL.md`. An empty object means the Source is restored but exposes no skills to profiles.

Do not install a Source repository wholesale. A profile can select an authored `skills/<id>` directory or an explicitly mapped Source skill only. Ordinary bootstrap restores pins and never advances them.
