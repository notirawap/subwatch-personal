# subwatch-personal

A personal, **read-only** research tool for a few finance subreddits.

It **never posts, comments, votes, messages or moderates**.

## What it does
Every few minutes it reads new public posts and comments in:
r/pennystocks, r/Shortsqueeze, r/10xPennyStocks, r/100xpennystock, r/marketrodeo, r/TheRaceTo10Million.

It summarises which stocks are being discussed and uses public account age/karma to discount likely spam accounts. Results are for the author's private use only.

## API usage
- OAuth app-only (client credentials), read-only.
- ~5–10 requests per minute, well under Reddit's limits; honours rate-limit headers.
- User-Agent: `linux:subwatch-personal:0.1 (by /u/Squidget_Pawarit)`.

## Data handling
- Private, single user. Never shared, published or sold.
- Not used to train AI/ML models.
- Deleted after 90 days; content deleted on Reddit is removed when detected.

## Why not Devvit
Devvit apps are installed by a subreddit's moderators and run inside it. This tool only needs read-only access to public posts across several subreddits the author does not moderate.
