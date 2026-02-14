# AI Agent Guidelines (General Python Projects)

## 1. Scope & Intent

This repository contains a **Python 3.12 project** intended to be:

* Hobbyist or exploratory
* Maintainable and evolvable
* Compatible with:

  * Clean / Hexagonal / Layered architectures
  * Data-science or research workflows
  * Script-heavy or library-style projects

This document defines **non-negotiable rules** for AI agents and human contributors.

> When in doubt, prioritize **clarity, reversibility, and explicit intent**.

---

## 2. Critical Agent Rules (Highest Priority)

These rules override all others.

### 🚫 Git & File Safety

1. **NEVER commit or push unless explicitly ordered**
2. **NEVER delete files** without explicit permission

   * Exception: temporary files created during the agent session
3. **ALWAYS run pre-commit before any commit**

   ```bash
   uv run pre-commit run --all-files
   ```
4. **NEVER bypass linting rules**

   * Do not modify `.pre-commit-config.yaml`
   * Rule suppression requires **explicit user approval** and inline justification

If a rule blocks progress, **stop and ask**.

---

## 3. Command Execution Policy

### Dependency & Command Management

All commands **must** be executed via `uv`.

```bash
# Install dependencies. Do not add them directly to pyproject.toml
uv add <dependency_name>

# Remove dependencies
uv remove <dependency_name>

# Sync dependencies
uv sync

# Quality & checks
uv run ruff check
uv run black
uv run bandit
uv run pre-commit run --all-files
```

🚫 Never invoke `pip`, `ruff`, `black`, `pytest`, or other tools directly.

This guarantees:

* Reproducibility
* Consistent environments
* Agent determinism

---

## 4. Python 3.12 Coding Standards

### Typing (Mandatory)

* All functions must be fully typed
* Prefer modern syntax exclusively

```python
# Good
def transform(data: dict[str, Any]) -> dict[str, Any]: ...

# Bad
def transform(data): ...
```

#### Allowed typing features

* `|` union syntax
* PEP 695 type aliases
* Generics (`TypeVar`, `Generic`)
* `kw_only=True` dataclasses

---

### Dataclasses & Data Models

* Prefer dataclasses over raw dicts
* Use `kw_only=True` for clarity
* Data containers may optionally implement `__getitem__` if dict-like access is required

```python
@dataclass(kw_only=True)
class Record:
    id: int
    name: str
```

⚠️ Raw dictionaries are acceptable **only** in:

* Exploratory notebooks
* Temporary data-science pipelines
* Explicitly documented exceptions

---

### Docstrings (Mandatory for Public Code)

* Use **Google docstring format**
* Required for:

  * Public functions
  * Classes
  * Modules with business or research logic

**Structure:**

1. Short summary (no period)
2. Blank line
3. Args
4. Returns / Yields
5. Raises (if applicable)
6. Optional extended explanation

---

### Modern Python Practices

* Use `match/case` for complex branching
* Prefer f-strings (including debug syntax)
* Prefer comprehensions for simple transforms
* Use context managers for all resources

---

## 5. Architecture & Design Principles

This project may follow **any** of the following styles:

* Clean / Hexagonal Architecture
* Layered / Modular Architecture
* Script-based or exploratory workflows
* Data-science pipelines

Regardless of style:

* Separate **I/O** from **logic**
* Avoid hidden side effects
* Prefer pure functions where possible
* Keep boundaries explicit (even if lightweight)

---

## 6. Persistence & Data Handling (If Applicable)

If the project uses databases or persistent storage:

* No inline SQL
* No string-interpolated queries
* Prefer parameterized queries
* Keep persistence logic isolated

If no database is present, this section may be ignored.

---

## 7. Error Handling & Logging

* No silent failures
* Exceptions must either:

  * Be handled meaningfully
  * Or re-raised with context
* Log intent, not noise

```text
GOOD: "Failed to parse record X due to missing field Y"
BAD: "Error occurred"
```

Retries must be:

* Explicit
* Bounded
* Logged

---

## 8. Security Baselines

* No secrets in code
* No credentials committed
* Environment variables only
* Avoid unsafe deserialization
* Assume untrusted input by default

---

## 9. Git Workflow Rules

### Branching

* Feature branches: `feature/description`
* Fix branches: `fix/description`
* Never commit directly to `main` or `develop`
* Never use:

  * `git reset --hard`
  * Force-push
    unless explicitly ordered

Always confirm:

```bash
git branch
```

before staging or committing.

---

### Commit Format

Use **Conventional Commits**:

```text
feat: add data ingestion step
fix: correct type mismatch in parser
docs: clarify agent rules
```

---

### Push Checklist (Only If Ordered)

1. Run pre-commit
2. Review `git diff`
3. Update README if scope or behavior changed
4. Push

---

## 10. Testing Expectations

Testing depth depends on project type:

* **Application / library** → unit tests expected
* **Data science / research** → smoke tests or validation scripts acceptable
* **Exploratory scripts** → tests optional but encouraged

All tests must be:

* Deterministic
* Explicitly scoped
* Runnable via `uv run`

---

## 11. Agent Self-Audit Checklist

Before stopping work:

* [ ] Python 3.12 syntax only
* [ ] Full typing coverage (unless explicitly exempted)
* [ ] Google-style docstrings for public code
* [ ] `uv run` used everywhere
* [ ] Errors handled and logged
* [ ] Tests updated or justified
* [ ] No commits or deletions without permission

---

## 12. Final Notes for AI Agents

This repository values:

* **Correctness over speed**
* **Clarity over cleverness**
* **Reversibility over optimization**

If urgency, ambiguity, or uncertainty arises:

> **Stop, explain, and request instructions.**

This is always the correct action
