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
- **Django Ninja**: Fast API framework for the web API layer
- **Prefect**: Workflow orchestration for managing scraping flows
- **Docker**: Containerized execution environment for scrapers
- **YAML-based configuration**: Scraping workflows defined in YAML "recipes"
- **Playwright/Puppeteer**: Browser automation (to be decided later)
- **Hetzner**: Cloud infrastructure provider
- **Coolify**: Deployment platform for containerized applications
- **Multi-stage approach**: Incremental development from simple HTTP to complex browser automation

## Development Setup

This project uses Python with the following stack:
- Django Ninja for API development
- Prefect for workflow orchestration
- Docker for containerized execution
- Standard Python tooling (pip/poetry for dependencies, pytest for testing)

The .gitignore is configured for Python development environments.

## Key Concepts

- **Scraper Recipes**: YAML configuration files that define scraping workflows
- **Docker Execution**: Isolated execution environment for scraping operations
- **Hybrid Execution**: Planned support for both simple HTTP requests and browser automation
- **Multi-step Workflows**: Support for complex scraping scenarios with multiple steps

## Current Status

The project is in initial setup phase with basic git repository structure established.