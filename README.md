# Scraper Engine

Given how hard it is to scrape and use scrapers. I have decided to build an
engine that allows people to scrape using only YAML recepies. I will see where
this goes.

## Tech Stack
- **Python** - Main development language
- **Django Ninja** - Fast API framework for the web API
- **Prefect** - Workflow orchestration for managing scraping flows
- **Docker** - Containerized execution environment
- **Playwright/Puppeteer** - Browser automation (to be decided)
- **Hetzner** - Cloud infrastructure provider
- **Coolify** - Deployment platform

My plan is to build this in 4 stages:
1. MVP Core: Run a scraper inside Docker from a YAML file. It will only run
requests scraping. A simple way to prove the whole process in a simple manner.
2. Playwright or Puppetteer in Typescript & Hybrid Execution: Add JS rendering
and multi step workflow for more complex and real world use scraping cases.
3. Production Service: Make this whole project observable, deployable and stable.
4. Robust Platform: Make it scalable, multi-client, automatable and testable.


I will be using Claude to help me.
