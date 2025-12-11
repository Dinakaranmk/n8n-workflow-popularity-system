n8n Workflow Popularity System

This project collects information about popular n8n workflows from three different sources:
YouTube, the n8n Community Forum, and Google Trends.
The goal is to identify which workflows are getting the most attention and make that information available through a simple REST API.

The project was built as part of a technical assignment that required data collection, processing, automation, and API creation.

Overview

The system does the following:

Fetches workflow-related data from:

YouTube (views, likes, comments, engagement ratios)

n8n Forum (replies, likes, contributors, topic views)

Google Trends (search interest for workflow keywords)

Combines all the collected data into a single JSON file called workflows_final.json.

Serves the combined data through a Flask-based API so it can be viewed or used by other tools.

Includes a cron-ready setup using GitHub Actions, so the data can be updated daily or weekly without manual work.

Key Files
yt_fetch_and_save.py      - Fetches YouTube data
forum_fetcher.py          - Fetches n8n Forum data
trends_fetcher.py         - Fetches Google Trends data
merge_datasets.py         - Merges all collected data
serve_all_workflows.py    - Runs the Flask REST API
requirements.txt          - Project dependencies


Cron automation file:

.github/workflows/daily-update.yml

How to Run the Project Locally

Install the required Python packages:

pip install -r requirements.txt


Create a .env file in the project folder with:

YOUTUBE_API_KEY=your_api_key_here


Run the data fetch scripts:

py yt_fetch_and_save.py
py forum_fetcher.py
py trends_fetcher.py
py merge_datasets.py


Start the API:

py serve_all_workflows.py


Open the API in your browser:

http://127.0.0.1:5000/workflows

API Usage Examples

The API supports filtering and searching through URL parameters.

Examples:

Get all workflows
http://127.0.0.1:5000/workflows

Filter by platform
http://127.0.0.1:5000/workflows?platform=YouTube

Filter by country
http://127.0.0.1:5000/workflows?country=US

Search by keyword
http://127.0.0.1:5000/workflows?q=slack

Limit results
http://127.0.0.1:5000/workflows?limit=10

Cron Automation

A GitHub Actions workflow is included to enable automatic daily or weekly updates.

The file .github/workflows/daily-update.yml runs all fetchers, merges the data, and commits updated results back to the repository.
This allows the system to stay up-to-date without needing to run anything manually.

Technologies Used

Python

Flask

YouTube Data API

Discourse API (n8n Forum)

Google Trends (pytrends)

GitHub Actions (for automation)

Notes

This project was created for learning and demonstration purposes, to show how data from multiple platforms can be collected, combined, and served through an API in an automated manner.