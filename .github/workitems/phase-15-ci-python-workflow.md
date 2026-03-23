# Work Item WI-015: Phase 15 - Python CI Workflow

## Status
- [ ] Not started
- [ ] In progress
- [ ] Blocked
- [ ] Done

## Goal

Set up GitHub Actions CI workflow for automated testing and validation on every push/PR.

## Scope

### 1. Workflow Triggers

- Push to main/develop branches
- Pull requests to main

### 2. CI Steps

1. Checkout code
2. Setup Python 3.12
3. Install dependencies
4. Run linting (flake8)
5. Run tests (pytest)
6. Generate coverage report

### 3. Matrix Testing (Optional)

- Python 3.11, 3.12
- Ubuntu latest

## Workflow File

```yaml
# .github/workflows/python-ci.yml
name: Python CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          cd src/backend
          pip install -r requirements.txt
          pip install pytest pytest-cov flake8
      - name: Lint
        run: |
          cd src/backend
          flake8 . --max-line-length=120
      - name: Test
        run: |
          cd src/backend
          pytest --cov=. --cov-report=term-missing
```

## Acceptance Criteria

- CI runs on every push/PR
- Linting errors fail the build
- Test failures fail the build
- Coverage report generated

## Files Created

- `.github/workflows/python-ci.yml`

## Success Criteria

- Green badge on repository
- All PRs validated before merge
- Coverage visible in PR comments
