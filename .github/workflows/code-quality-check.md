---
description: |
  This workflow performs AI-powered code quality analysis on pull requests.
  It reviews changed files for potential bugs, security issues, performance
  problems, and adherence to best practices, then posts a detailed review
  comment on the PR.

on:
  pull_request:
    types: [opened, synchronize, reopened]
  workflow_dispatch:

permissions:
  contents: read
  pull-requests: read
  issues: read

network: defaults

tools:
  github:

safe-outputs:
  add-comment:
  add-labels:
    allowed: [code-quality, automated-review]
---

# Code Quality Check

Perform an AI-powered code quality review on the pull request.

## What to Analyze

For each changed file in the pull request, check for:

- **Bugs & Logic Errors** - Off-by-one errors, null/undefined references, race conditions, incorrect control flow
- **Security Issues** - Injection vulnerabilities (SQL, XSS, command), hardcoded secrets, insecure dependencies, improper input validation
- **Performance** - Unnecessary loops, expensive operations inside loops, memory leaks, missing pagination
- **Code Style & Best Practices** - Naming conventions, dead code, overly complex functions, missing error handling
- **Type Safety** - Incorrect type usage, unsafe casts, missing null checks

## What to Ignore

- Formatting and whitespace-only changes
- Auto-generated files (lock files, build artifacts)
- Test fixture data

## Review Output

Post a single review comment on the pull request with:

1. **Summary** - A brief overview of the code quality findings
2. **Critical Issues** - Must-fix problems (bugs, security vulnerabilities)
3. **Warnings** - Recommended improvements (performance, best practices)
4. **Suggestions** - Optional enhancements for better code quality
5. **Verdict** - An overall assessment: Approve, Request Changes, or Comment

## Style

- Be constructive and specific - reference exact lines and suggest fixes
- Prioritize findings by severity (critical > warning > suggestion)
- Keep feedback actionable - explain *why* something is an issue and *how* to fix it
- If the code looks good, say so briefly and approve

## Process

1. Fetch the pull request diff and list of changed files
2. Read the full content of each changed file for context
3. Analyze each file against the quality criteria above
4. Compile findings into a structured review
5. Submit the review as a PR comment using the GitHub API
