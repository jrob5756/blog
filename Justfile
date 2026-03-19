# Default recipe: list available commands
default:
    @just --list

# Start dev server with drafts
dev:
    hugo server -D

# Start dev server (published content only)
serve:
    hugo server

# Build the site
build:
    hugo --minify

# Build including drafts
build-drafts:
    hugo --minify -D

# Create a new blog post (usage: just post my-post-title)
post title:
    hugo new content blog/$(date +%Y-%m-%d)-{{title}}.md

# Local path to the news repo
news_repo := "~/src/news"

# Sync all news reports
sync-news:
    python3 scripts/sync-news.py {{news_repo}}/reports content/news/

# Sync only today's news report
sync-news-today:
    python3 scripts/sync-news.py {{news_repo}}/reports content/news/ --today

# Sync a specific date's report (usage: just sync-news-date 2026-03-15)
sync-news-date date:
    python3 scripts/sync-news.py {{news_repo}}/reports content/news/ --date {{date}}

# Sync reports from a date onward (usage: just sync-news-since 2026-03-01)
sync-news-since date:
    python3 scripts/sync-news.py {{news_repo}}/reports content/news/ --since {{date}}

# Clean build output
clean:
    rm -rf public/ resources/_gen/

# Check for broken links in build output
check: build
    hugo --printPathWarnings 2>&1 | grep -i warn || echo "No warnings found"
