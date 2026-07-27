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
grep -Fq 'COMPLETE profile=test sources=0 created=0 retained=1 reconciled=1 conflicts=0 skipped=0' "$workspace/third.out"
[[ ! -e "$workspace/home/.agents/skills/external" ]]

# A profile made entirely of Hub-authored skills must not restore unrelated
# manifest Sources. This keeps unavailable historical source pins from blocking
# the public Carlo Baseline projection.
print -r -- '{"schema_version":1,"sources":{"unneeded":{"url":"https://example.invalid/unneeded.git","revision":"0000000000000000000000000000000000000000","license":"MIT","license_path":"LICENSE","skills":{}}}}' > "$hub/sources.json"
print -r -- '{"schema_version":1,"skills":["local-skill"],"destinations":["agents","claude","codex"]}' > "$hub/profiles/local-only.json"
local_home="$workspace/local-home"
AGENTS_HOME="$local_home/.agents" CLAUDE_HOME="$local_home/.claude" CODEX_HOME="$local_home/.codex" \
  "$hub/scripts/bootstrap" --profile local-only --no-input > "$workspace/local-only.out"
grep -Fq 'COMPLETE profile=local-only sources=0 created=3 retained=0 reconciled=0 conflicts=0 skipped=0' "$workspace/local-only.out"
[[ -L "$local_home/.agents/skills/local-skill" ]]
[[ $(readlink "$local_home/.claude/skills") == "$local_home/.agents/skills" ]]
[[ $(readlink "$local_home/.codex/skills") == "$local_home/.agents/skills" ]]

# The v1 per-harness layout is migrated only when every existing entry is
# recorded and still points to the Hub-owned target.
legacy_home="$workspace/legacy-home"
for root in .agents .claude .codex; do
  mkdir -p "$legacy_home/$root/skills"
  ln -s "$hub/skills/local-skill" "$legacy_home/$root/skills/local-skill"
done
for destination in agents claude codex; do
  print -r -- "local-skill"$'\t'"$hub/skills/local-skill" > "$hub/.hub-state/legacy-${destination}.tsv"
done
print -r -- '{"schema_version":1,"skills":["local-skill"],"destinations":["agents","claude","codex"]}' > "$hub/profiles/legacy.json"
AGENTS_HOME="$legacy_home/.agents" CLAUDE_HOME="$legacy_home/.claude" CODEX_HOME="$legacy_home/.codex" \
  "$hub/scripts/bootstrap" --profile legacy --no-input > "$workspace/legacy.out"
grep -Fq 'COMPLETE profile=legacy sources=0 created=2 retained=1 reconciled=2 conflicts=0 skipped=0' "$workspace/legacy.out"
[[ $(readlink "$legacy_home/.claude/skills") == "$legacy_home/.agents/skills" ]]
[[ $(readlink "$legacy_home/.codex/skills") == "$legacy_home/.agents/skills" ]]

# A foreign canonical symlink is never followed or altered.
foreign_home="$workspace/foreign-home"
mkdir -p "$foreign_home/outside" "$foreign_home/.agents"
print -r -- 'keep me' > "$foreign_home/outside/keep"
ln -s "$foreign_home/outside" "$foreign_home/.agents/skills"
if AGENTS_HOME="$foreign_home/.agents" CLAUDE_HOME="$foreign_home/.claude" CODEX_HOME="$foreign_home/.codex" \
  "$hub/scripts/bootstrap" --profile local-only --no-input > "$workspace/foreign.out" 2>&1; then
  print -u2 'foreign canonical symlink must not be accepted'
  exit 1
fi
grep -Fq 'CONFLICT local-only/agents: existing target left untouched' "$workspace/foreign.out"
grep -Fq 'keep me' "$foreign_home/outside/keep"

# A foreign harness directory is a conflict and its contents remain untouched.
foreign_destination_home="$workspace/foreign-destination-home"
mkdir -p "$foreign_destination_home/.claude/skills"
print -r -- 'keep me too' > "$foreign_destination_home/.claude/skills/keep"
if AGENTS_HOME="$foreign_destination_home/.agents" CLAUDE_HOME="$foreign_destination_home/.claude" CODEX_HOME="$foreign_destination_home/.codex" \
  "$hub/scripts/bootstrap" --profile local-only --no-input > "$workspace/foreign-destination.out" 2>&1; then
  print -u2 'foreign harness directory must not be replaced'
  exit 1
fi
grep -Fq 'CONFLICT local-only/claude: existing target left untouched' "$workspace/foreign-destination.out"
grep -Fq 'keep me too' "$foreign_destination_home/.claude/skills/keep"

print 'bootstrap contract passed'
