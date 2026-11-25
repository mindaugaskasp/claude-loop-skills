#!/usr/bin/env bash
# Home-made review for seedbox. Prints one line per problem:
#   path:line: [label] message
# and exits 1 when there is at least one.
set -u

cd "$(dirname "$0")/.."

files=$(find bin lib -type f \( -name '*.rb' -o -path 'bin/*' \) | sort)
found=0

report() {
  echo "$1"
  found=1
}

for f in $files; do
  # 1. Debugger calls left in.
  while IFS=: read -r n _; do
    [ -n "$n" ] && report "$f:$n: [debugger-left-in] remove the debugger call"
  done < <(grep -nE '^\s*(binding\.(irb|pry)|debugger)\b' "$f")

  # 2. TODO or FIXME without a name in brackets, like TODO(ieva).
  while IFS=: read -r n _; do
    [ -n "$n" ] && report "$f:$n: [todo-without-name] write TODO(name) so we know whom to ask"
  done < <(grep -nE '\b(TODO|FIXME)\b' "$f" | grep -vE '\b(TODO|FIXME)\([a-z]+\)')

  # 3. Tabs for indentation.
  while IFS=: read -r n _; do
    [ -n "$n" ] && report "$f:$n: [tab-indent] indent with two spaces, not tabs"
  done < <(grep -nP '^\t+' "$f")

  # 4. Lines longer than 120 characters.
  while IFS=: read -r n _; do
    [ -n "$n" ] && report "$f:$n: [long-line] line is longer than 120 characters"
  done < <(grep -nE '^.{121,}$' "$f")

  # 5. The frozen string comment at the top of every Ruby file.
  case "$f" in
    *.rb)
      if [ "$(head -n 1 "$f")" != "# frozen_string_literal: true" ]; then
        report "$f:1: [missing-frozen-string-literal] first line must be '# frozen_string_literal: true'"
      fi
      ;;
  esac
done

if [ "$found" -eq 1 ]; then
  exit 1
fi
echo "review: nothing found"
