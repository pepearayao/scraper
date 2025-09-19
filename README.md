# Scraper Engine

A powerful web scraping engine that allows users to define scraping workflows using YAML configuration files (recipes). The engine handles everything from simple HTTP requests to complex browser automation scenarios.

## Project Structure

```
scraper/
├── engine/                 # Django application
│   ├── engine/            # Main Django project configuration
│   ├── scraper/           # Core scraping models and logic
│   └── users/             # User management
├── scrapers/              # Scraper implementations
│   ├── core/              # Core scraping functionality
│   ├── browser/           # Browser-based scrapers
│   └── runners/           # Execution runners
├── recipes/               # YAML recipe configurations
├── deploy/                # Deployment configurations
└── tests/                 # Test files
```

## Tech Stack

- **Python** - Main development language
- **Django** - Web framework with Django Ninja for fast API development
- **Prefect** - Workflow orchestration for managing scraping flows
- **Docker** - Containerized execution environment
- **YAML** - Configuration format for scraping recipes
- **Playwright/Puppeteer** - Browser automation (to be decided)
- **Hetzner** - Cloud infrastructure provider
- **Coolify** - Deployment platform

## Core Models

The Django application includes these key models:

- **User**: Basic user authentication and management
- **Project**: Container for organizing scraping jobs by user
- **Job**: Individual scraping job definitions with YAML recipes
- **Run**: Execution instances tracking status and Prefect integration
- **Results**: Output data storage with JSON payload and artifacts

## Development Roadmap

Building this in 4 stages:

1. **MVP Core**: Docker-based scraper that runs simple HTTP requests from YAML files
2. **Browser Integration**: Add Playwright/Puppeteer for JavaScript rendering and multi-step workflows
3. **Production Service**: Make the system observable, deployable and stable
4. **Robust Platform**: Scale to multi-client, automatable and testable system

## Current Status

✅ Project structure established
✅ Django applications created
✅ Core models defined
🔄 API development in progress
⏳ Docker integration pending
⏳ YAML recipe parsing pending
