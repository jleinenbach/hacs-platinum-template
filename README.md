# HACS Platinum Integration Template

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.1+-blue.svg)](https://www.home-assistant.io/)
[![HACS](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://hacs.xyz/)
[![Quality Scale](https://img.shields.io/badge/Quality%20Scale-Platinum-gold.svg)](https://developers.home-assistant.io/docs/core/integration-quality-scale/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A template for creating Home Assistant custom integrations targeting **Platinum Quality Scale** standards.

## 🚀 Features

- **Platinum Quality Scale** compliance from the start
- **Strict Type Checking** with Pyright + mypy --strict
- **Modern Python** (3.13+) with `asyncio.timeout`
- **AI-Optimized** with CLAUDE.md/AGENTS.md for AI assistants
- **Quality Tracking** via `quality_scale.yaml`
- **Comprehensive CI** with all required checks

## 📋 Prerequisites

- Home Assistant 2026.1.0+
- Python 3.13+
- HACS for installation

## 🔧 Development Setup

```bash
# Install dev dependencies
pip install -r requirements_dev.txt

# Install pre-commit hooks
pre-commit install

# Run all checks
./script/check
```

## ✅ Quality Assurance

| Check | Tool | Requirement |
|-------|------|-------------|
| Format | `ruff format` | MANDATORY |
| Lint | `ruff check --fix` | MANDATORY |
| Type Check | `pyright` | MANDATORY |
| Type Check | `mypy --strict` | MANDATORY |
| Tests | `pytest --cov` | >95% coverage |
| HACS | `hacs/action` | MANDATORY |
| Hassfest | `hassfest` | MANDATORY |

## 📁 Project Structure

```
├── CLAUDE.md                    # AI agent instructions
├── AGENTS.md                    # Alias for CLAUDE.md
├── pyproject.toml               # Ruff, Pyright, mypy, pytest config
├── .pre-commit-config.yaml      # Pre-commit hooks
│
├── .github/workflows/
│   └── ci.yml                   # Full CI pipeline
│
├── custom_components/your_domain/
│   ├── quality_scale.yaml       # ⚠️ Track compliance here!
│   ├── py.typed                 # Platinum: strict-typing
│   └── ...
│
├── script/
│   ├── check                    # Run all checks
│   ├── lint                     # ruff format + check --fix
│   └── type-check               # pyright + mypy --strict
│
└── tests/
    └── ...
```

## 🎯 Quality Scale Tracking

The `quality_scale.yaml` file tracks compliance with all 53 rules:

```yaml
rules:
  async-dependency:
    status: done  # Change from 'todo' when implemented
    comment: "All API calls use async aiohttp"
```

**AI agents MUST update this file when implementing features!**

## 📖 Documentation

- [CLAUDE.md](CLAUDE.md) - AI agent instructions
- [quality_scale.yaml](custom_components/your_domain/quality_scale.yaml) - Compliance tracking
- [HA Quality Scale](https://developers.home-assistant.io/docs/core/integration-quality-scale/)

## License

MIT License
