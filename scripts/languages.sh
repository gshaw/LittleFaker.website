#!/usr/bin/env bash
# Fails when a page or a template string is missing a language. English is
# content/<page>.md and i18n/en.toml; the others are content/<page>.<lang>.md and
# i18n/<lang>.toml, for each [languages.<lang>] in hugo.toml.
set -euo pipefail
cd "$(dirname "$0")/.."

langs=$(sed -nE 's/^\[languages\.([a-z-]+)\]$/\1/p' hugo.toml | grep -vx en)
pages=$(find content -name '*.md' | grep -vE '\.[a-z-]+\.md$' | sort)
missing=0
checked=0
for page in $pages; do
  for lang in $langs; do
    checked=$((checked + 1))
    [[ -f ${page%.md}.$lang.md ]] || { echo "Missing: ${page%.md}.$lang.md" >&2; missing=$((missing + 1)); }
  done
done
en_keys=$(sed -nE 's/^([A-Za-z]+) =.*/\1/p' i18n/en.toml | sort)
for lang in $langs; do
  checked=$((checked + 1))
  keys=$(sed -nE 's/^([A-Za-z]+) =.*/\1/p' "i18n/$lang.toml" 2>/dev/null | sort)
  [[ $keys == "$en_keys" ]] || { echo "i18n/$lang.toml doesn't have the same keys as i18n/en.toml" >&2; missing=$((missing + 1)); }
done
((missing == 0)) || exit 1
echo "$(echo "$pages" | wc -l | tr -d ' ') pages and the template strings are in $(echo "$langs" | wc -l | tr -d ' ') more languages ($checked files checked)"
