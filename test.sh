#! /bin/bash

# assert-equal(test case name, expected value, actual value)
# Assert that both values are equal.
assert-equal() {
  if [[ $3 != "$2" ]]; then
    printf "\e[41mTest failed: %s, expected %s, got %s\e[0m\n\n" "$1" "$2" "$3"
  else
    printf "\e[42mTest successful: %s, expected %s, got %s\e[0m\n\n" "$1" "$2" "$3"
  fi
}

# assert-contains(test case name, value, searching string)
# Assert that the searching string contains a value.
function assert-contains() {
  if [[ $3 != *$2* ]]; then
    printf "\e[41mTest failed: %s, expected %s in output, got:\n%s\e[0m\n\n" "$1" "$2" "$3"
  else
    printf "\e[42mTest successful: %s, expected %s to be in string\e[0m\n\n" "$1" "$2"
  fi
}

# assert-success(test case name)
# Assert that the last command had an exit code of 0
function assert-success() {
  if [[ $? -ne 0 ]]; then
    printf "\e[41mTest failed: %s, expected exit code 0, got %s\e[0m\n\n" "$1" "$?"
  else
    printf "\e[42mTest successful: %s, expected exit code 0\e[0m\n\n" "$1"
  fi
}

source .venv/bin/activate

git init test
cd test || exit 1

# 1. No changes; expected: 0.0.0, no changes
touch test.1
git add .
git commit -m 'chore: test'
output=$(python3 ../src/app.py)
assert-success "No changes"
assert-contains "No changes" "next_version=0.0.0" "$output"
assert-contains "No changes" "has_changes=False" "$output"

# 2. Fix, expected: 0.0.1, changes
touch test.2
git add .
git commit -m 'fix: test'
output=$(python3 ../src/app.py --create-tag true)
assert-success "Fix"
assert-contains "Fix" "next_version=0.0.1" "$output"
assert-contains "Fix" "has_changes=True" "$output"
assert-equal "Fix: Check git tag" "v0.0.1" "$(git describe --tags)"

# 3. Feature, expected: 0.1.0, changes
touch test.3
git add .
git commit -m 'feat: test'
output=$(python3 ../src/app.py --create-tag true)
assert-success "Feature"
assert-contains "Feature" "next_version=0.1.0" "$output"
assert-contains "Feature" "has_changes=True" "$output"
assert-equal "Feature: Check git tag" "v0.1.0" "$(git describe --tags)"

# 4. Breaking Feature, expected: 1.0.0, changes
touch test.4
git add .
git commit -m 'feat!: test'
output=$(python3 ../src/app.py --create-tag true)
assert-success "Breaking Feature"
assert-contains "Breaking Feature" "next_version=1.0.0" "$output"
assert-contains "Breaking Feature" "has_changes=True" "$output"
assert-equal "Breaking Feature: Check git tag" "v1.0.0" "$(git describe --tags)"

# 5. Hotfix, expected: 1.0.0-h.1, changes
touch test.5
git add .
git commit -m 'fix: test'
output=$(python3 ../src/app.py --create-tag true --suffix h --only-increase-suffix true)
assert-success "Hotfix 1"
assert-contains "Hotfix 1" "Version is 1.0.0-h.1" "$output"
assert-contains "Hotfix 1" "has_changes=True" "$output"
assert-equal "Hotfix 1: Check git tag" "v1.0.0-h.1" "$(git describe --tags)"

# 6. Hotfix, expected: 1.0.0-h.2, changes
touch test.6
git add .
git commit -m 'fix: test'
output=$(python3 ../src/app.py --create-tag true --suffix h --only-increase-suffix true)
assert-success "Hotfix 2"
assert-contains "Hotfix 2" "Version is 1.0.0-h.2" "$output"
assert-contains "Hotfix 2" "has_changes=True" "$output"
assert-equal "Hotfix 2: Check git tag" "v1.0.0-h.2" "$(git describe --tags)"

# 7. Feature, expected: 1.1.0, changes
touch test.7
git add .
git commit -m 'feat: test'
output=$(python3 ../src/app.py --create-tag true)
assert-success "Feature 2"
assert-contains "Feature 2" "next_version=1.1.0" "$output"
assert-contains "Feature 2" "has_changes=True" "$output"
assert-equal "Feature 2: Check git tag" "v1.1.0" "$(git describe --tags)"

printf "\e[43mPress any key to exit...\e[0m\n"
read -n 1 -r
cd ..
rm -drf test

deactivate
