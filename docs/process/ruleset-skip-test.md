# Ruleset skip-behavior test

Temporary file — safe to delete after Issue #970 test is complete.

Purpose: docs-only commit to verify GitHub Ruleset "skipped = pass" behavior
for `playwright-e2e` on `release/m14`. No frontend or backend files changed;
CI path filter will skip `playwright-e2e`. Test passes if the PR is mergeable.
