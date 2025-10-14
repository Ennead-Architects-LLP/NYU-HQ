# NYU-HQ

Welcome to NYU-HQ! This repository hosts a GitHub Pages site using Jekyll.

## GitHub Pages Setup

This site uses the `docs` folder method for GitHub Pages:

1. The site content is in the `/docs` folder
2. GitHub Pages serves from this folder
3. Jekyll automatically builds the site

## Local Development

To run the site locally:

```bash
cd docs
bundle install
bundle exec jekyll serve
```

Then visit `http://localhost:4000/NYU-HQ/`

## Configuration

- Site configuration: `docs/_config.yml`
- Main page: `docs/index.md`
- Theme: Cayman (GitHub Pages default themes)

## Deployment

The site is automatically deployed when you push to the `main` branch. Make sure to:

1. Enable GitHub Pages in repository settings
2. Set source to "main branch /docs folder"

## License

[Add your license here]

