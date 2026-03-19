# jasonrobert.dev

Personal blog and website built with [Hugo](https://gohugo.io/) and the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, deployed to [Cloudflare Pages](https://pages.cloudflare.com/).

## Local Development

```bash
# Install Hugo (macOS)
brew install hugo

# Clone with submodules
git clone --recurse-submodules https://github.com/jrob5756/blog.git
cd blog

# Start dev server (includes drafts)
hugo server -D
```

Open [http://localhost:1313](http://localhost:1313) in your browser.

## Content Structure

| Section | Path | Description |
|---------|------|-------------|
| Home | `content/_index.md` | Profile landing page |
| About | `content/about/index.md` | Professional profile |
| Blog | `content/blog/` | Long-form articles and technical posts |
| News | `content/news/` | Daily AI/tech news summaries (auto-synced) |
| Search | `content/search.md` | Full-text search page |

## Writing a New Post

```bash
hugo new content blog/YYYY-MM-DD-post-title.md
```

Edit the generated file, set `draft: false` when ready to publish.

## News Sync

News reports are synced from the [news](https://github.com/jrob5756/news) repo via GitHub Actions. The sync script transforms `reports/YYYY/MM/DD.md` into Hugo content with proper front matter.

To run manually:

```bash
python3 scripts/sync-news.py /path/to/news/reports content/news/
```

## Deployment

Cloudflare Pages builds automatically on push to `main`:

| Setting | Value |
|---------|-------|
| Build command | `hugo --minify` |
| Output directory | `public` |
| Environment variable | `HUGO_VERSION=0.158.0` |

## License

Content is copyright Jason Robert. The site source code is available for reference.
