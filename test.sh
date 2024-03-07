#! /bin/bash
# Arg1: Test case name, Arg 2: Expected; Arg 3: Actual
function assert-equal() {
  if [[ $3 != "$2" ]]; then
    printf "\e[41mTest failed: %s, expected %s, got %s\e[0m\n\n" "$1" "$2" "$3"
  else
    printf "\e[42mTest successful: %s, expected %s\e[0m\n\n" "$1" "$2"
  fi
}

# Arg1: Test case name, Arg 2: Expected; Arg 3: Output to search in
function assert-contains() {
  if [[ $3 != *$2* ]]; then
    printf "\e[41mTest failed: %s, expected %s in output, got:\n%s\e[0m\n\n" "$1" "$2" "$3"
  else
    printf "\e[42mTest successful: %s, expected %s\e[0m\n\n" "$1" "$2"
  fi
}

function assert-success() {
  if [[ $? -ne 0 ]]; then
    printf "\e[41mTest failed: %s, expected exit code 0, got %s\e[0m\n\n" "$1" "$?"
  else
    printf "\e[42mTest successful: %s, expected exit code 0\e[0m\n\n" "$1"
  fi
}

source .test.env
source .venv/bin/activate

git clone "$TEST_REPOSITORY_URL" test
cd test || exit 1

# 1. No changes; expected: 0.0.0, no changes
touch test.1
git add .
git commit -m 'chore: test'
output=$(python3 ../src/app.py)
assert-success "No changes"
assert-contains "No changes" "0.0.0" "$output"
assert-contains "No changes" "No changes" "$output"

# 2. Fix, expected: 0.0.1, changes
touch test.2
git add .
git commit -m 'fix: test'
output=$(python3 ../src/app.py --create-tag true)
assert-success "Fix"
assert-contains "Fix" "0.0.1" "$output"
assert-contains "Fix" "Changes detected" "$output"
assert-equal "Fix: Check git tag" "0.0.1" "$(git describe --tags)"

# 3. Feature, expected: 0.1.0, changes
touch test.3
git add .
git commit -m 'feat: test'
output=$(python3 ../src/app.py --create-tag true)
assert-success "Feature"
assert-contains "Feature" "0.1.0" "$output"
assert-contains "Feature" "Changes detected" "$output"
assert-equal "Feature: Check git tag" "0.1.0" "$(git describe --tags)"

# 4. Breaking Feature, expected: 1.0.0, changes
touch test.4
git add .
git commit -m 'feat!: test'
output=$(python3 ../src/app.py --create-tag true)
assert-success "Breaking Feature"
assert-contains "Breaking Feature" "1.0.0" "$output"
assert-contains "Breaking Feature" "Changes detected" "$output"
assert-equal "Breaking Feature: Check git tag" "1.0.0" "$(git describe --tags)"

# 5. Hotfix, expected: 1.0.0-h.1, changes
touch test.5
git add .
git commit -m 'fix: test'
output=$(python3 ../src/app.py --create-tag true --suffix h --only-increase-suffix true)
assert-success "Hotfix 1"
assert-contains "Hotfix 1" "1.0.0-h.1" "$output"
assert-contains "Hotfix 1" "Changes detected" "$output"
assert-equal "Hotfix 1: Check git tag" "1.0.0-h.1" "$(git describe --tags)"

# 6. Hotfix, expected: 1.0.0-h.2, changes
touch test.6
git add .
git commit -m 'fix: test'
output=$(python3 ../src/app.py --create-tag true --suffix h --only-increase-suffix true)
assert-success "Hotfix 2"
assert-contains "Hotfix 2" "1.0.0-h.2" "$output"
assert-contains "Hotfix 2" "Changes detected" "$output"
assert-equal "Hotfix 2: Check git tag" "1.0.0-h.2" "$(git describe --tags)"

printf "\e[43mPress any key to exit...\e[0m\n"
read -n 1 -r
cd ..
rm -drf test

deactivate
