# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a scraper engine that allows users to define web scraping workflows using YAML configuration files (recipes). The project is designed to be built in 4 stages:

1. **MVP Core**: Docker-based scraper that runs simple HTTP requests from YAML files
2. **Playwright/Puppeteer Integration**: Add JavaScript rendering and multi-step workflows
3. **Production Service**: Make the system observable, deployable and stable
4. **Robust Platform**: Scale to multi-client, automatable and testable system

## Architecture

The project uses a Python-based stack with the following key components:

- **Python**: Main development language
- **Django**: Web framework with Django Ninja for fast API development
- **Prefect**: Workflow orchestration for managing scraping flows
- **Docker**: Containerized execution environment for scrapers
- **YAML-based configuration**: Scraping workflows defined in YAML "recipes"
- **Playwright/Puppeteer**: Browser automation (to be decided later)
- **Hetzner**: Cloud infrastructure provider
- **Coolify**: Deployment platform for containerized applications
- **Multi-stage approach**: Incremental development from simple HTTP to complex browser automation

## Project Structure

```
/Users/pepe/code/scraper/
├── engine/                 # Django application root
│   ├── engine/            # Main Django project settings
│   │   ├── settings.py    # Django configuration
│   │   ├── urls.py        # URL routing
│   │   └── ...
│   ├── scraper/           # Core scraping models and logic
│   │   ├── models.py      # Project, Job, Run, Results models
│   │   └── ...
│   ├── users/             # User management
│   │   ├── models.py      # User model
│   │   └── ...
│   └── manage.py          # Django management script
├── scrapers/              # Scraper implementations
│   ├── core/              # Core scraping functionality
│   ├── browser/           # Browser-based scrapers
│   └── runners/           # Execution runners
├── recipes/               # YAML recipe configurations
├── deploy/                # Deployment configurations
└── tests/                 # Test files
```

## Django Models

### Users App (`engine/users/models.py`)
- **User**: Basic user model (currently minimal implementation)

### Scraper App (`engine/scraper/models.py`)
- **Project**: Container for organizing scraping jobs
  - UUID primary key
  - Name and owner (FK to User)
  - Creation timestamp

- **Job**: Individual scraping job definition
  - UUID primary key
  - Associated with Project
  - Stores raw YAML recipe and parsed JSON
  - Tracks creation, updates, last run time
  - Active/inactive status

- **Run**: Execution instance of a Job
  - UUID primary key
  - Status tracking (queued, running, success, failure)
  - Prefect integration (state and flow run ID)
  - Execution logs and timing

- **Results**: Output data from Run execution
  - UUID primary key
  - JSON payload and artifacts storage
  - Linked to specific Run

## Development Setup

This project uses Python with the following stack:
- Django with Django Ninja for API development
- Prefect for workflow orchestration
- Docker for containerized execution
- Standard Python tooling (pip/poetry for dependencies, pytest for testing)

The .gitignore is configured for Python development environments.

## Key Concepts

- **Scraper Recipes**: YAML configuration files that define scraping workflows
- **Docker Execution**: Isolated execution environment for scraping operations
- **Hybrid Execution**: Planned support for both simple HTTP requests and browser automation
- **Multi-step Workflows**: Support for complex scraping scenarios with multiple steps
- **Project Organization**: Jobs are organized under Projects owned by Users
- **Run Tracking**: Each job execution creates a Run record with full status and result tracking

## Current Status

The project has Django applications set up with core models defined for managing scraping workflows. The database schema supports the full lifecycle from recipe definition to execution results.