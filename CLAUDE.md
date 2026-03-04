# CLAUDE.md

## Overview

NYU-HQ is a project documentation site for the NYU project at Ennead Architects. It consists of a static HTML site (deployed via Vercel and GitHub Pages) and a Python utility that uploads local HTML reports to the GitHub repository.

## Repository Structure

```
NYU-HQ/
  docs/                  # Static site served by Vercel / GitHub Pages
    index.html           # Main page
    diagram.html         # Project diagram
  sender/                # Python utility to push reports to GitHub
    send_report.py       # Uploads HTML reports + assets via GitHub API
    build.bat            # Builds sender into standalone executable
    create_build_version.py  # Version stamping for builds
```

## Development

### Static Site

The `docs/` directory is served directly -- no build step required.

To preview locally, open `docs/index.html` in a browser or use any static file server.

### Report Sender

```bash
cd sender
python send_report.py    # Send latest HTML report to GitHub repo
```

Requires a `config.json` file in the sender directory with:
- `github_token` -- GitHub personal access token
- `repo_owner` -- GitHub org/user
- `repo_name` -- Repository name

No external Python dependencies required (uses only standard library).

## Deployment

- **Static site**: Deployed to Vercel (`outputDirectory: docs`, no build step) and GitHub Pages
- **Sender**: Runs locally on Windows; can be compiled to `.exe` via `build.bat`

## Key Configuration

```
# sender/config.json (not committed)
github_token              # GitHub personal access token
repo_owner                # GitHub organization or user
repo_name                 # Target repository name
```
