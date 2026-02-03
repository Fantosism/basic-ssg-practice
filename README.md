# Basic SSG Practice

I built this static site generator from scratch to understand how SSGs work under the hood.

## What it does

- Converts Markdown files to HTML pages
- Applies a single HTML template to all pages
- Copies static assets (CSS, images) to the output directory
- Supports configurable base paths for deployment to subdirectories (like GitHub Pages)

## What it's missing

This is a learning project, not a production tool. It lacks:

- Hot reloading / dev server
- Asset optimization and bundling
- Syntax highlighting for code blocks
- RSS feeds, sitemaps, SEO tags
- Layouts and partials
- Data files and collections
- Plugins and extensibility
- Build caching and incremental builds

If you need a real static site generator, use [Astro](https://astro.build/) or [Hugo](https://gohugo.io/).
