#!/bin/zsh
set -euo pipefail

workspace=$(mktemp -d "${TMPDIR:-/tmp}/skills-hub-test.XXXXXX")
workspace=${workspace:A}
trap 'rm -rf "$workspace"' EXIT
hub=$workspace/hub
origin=$workspace/origin
author=$workspace/author
mkdir -p "$hub/scripts" "$hub/profiles" "$hub/skills/local-skill" "$workspace/home/.agents"
cp scripts/bootstrap "$hub/scripts/bootstrap"
chmod +x "$hub/scripts/bootstrap"

git init --bare "$origin" >/dev/null
git init "$author" >/dev/null
git -C "$author" config user.name Test
git -C "$author" config user.email test@example.invalid
mkdir -p "$author/external-skill"
print -r -- 'external test skill' > "$author/external-skill/SKILL.md"
print -r -- 'MIT test license' > "$author/LICENSE"
git -C "$author" add LICENSE external-skill/SKILL.md
git -C "$author" commit -m source >/dev/null
git -C "$author" branch -M main
git -C "$author" remote add origin "$origin"
git -C "$author" push -u origin main >/dev/null
pin=$(git -C "$author" rev-parse HEAD)

print -r -- 'local test skill' > "$hub/skills/local-skill/SKILL.md"
print -r -- '{"schema_version":1,"sources":{"testsource":{"url":"'"$origin"'","revision":"'"$pin"'","license":"MIT","license_path":"LICENSE","skills":{"external":"external-skill"}}}}' > "$hub/sources.json"
print -r -- '{"schema_version":1,"skills":["local-skill","external"],"destinations":["agents"]}' > "$hub/profiles/test.json"

AGENTS_HOME="$workspace/home/.agents" "$hub/scripts/bootstrap" --profile test --no-input > "$workspace/first.out"
grep -Fq 'COMPLETE profile=test sources=1 created=2 retained=0 reconciled=0 conflicts=0 skipped=0' "$workspace/first.out"
[[ $(readlink "$workspace/home/.agents/skills/local-skill") == "$hub/skills/local-skill" ]]
[[ $(readlink "$workspace/home/.agents/skills/external") == "$hub/sources/testsource/external-skill" ]]
[[ $(git -C "$hub/sources/testsource" rev-parse HEAD) == "$pin" ]]

AGENTS_HOME="$workspace/home/.agents" "$hub/scripts/bootstrap" --profile test --no-input > "$workspace/second.out"
grep -Fq 'COMPLETE profile=test sources=1 created=0 retained=2 reconciled=0 conflicts=0 skipped=0' "$workspace/second.out"

print -r -- '{"schema_version":1,"skills":["local-skill"],"destinations":["agents"]}' > "$hub/profiles/test.json"
AGENTS_HOME="$workspace/home/.agents" "$hub/scripts/bootstrap" --profile test --no-input > "$workspace/third.out"
grep -Fq 'COMPLETE profile=test sources=1 created=0 retained=1 reconciled=1 conflicts=0 skipped=0' "$workspace/third.out"
[[ ! -e "$workspace/home/.agents/skills/external" ]]

print 'bootstrap contract passed'
