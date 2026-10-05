# subwatch-personal

A small, **personal, read-only** tool that watches a few finance subreddits and builds a private stock-ticker watchlist.

It **never posts, comments, votes, messages or moderates**.

## What it does
Every ~5 minutes it:
1. Reads the newest public posts and comments in:
   r/pennystocks, r/Shortsqueeze, r/10xPennyStocks, r/100xpennystock, r/marketrodeo, r/TheRaceTo10Million
   (`GET /r/{sub}/new`, `GET /r/{sub}/comments`).
2. Extracts mentioned stock tickers (e.g. `$ABCD`).
3. Looks up each author's public account age and karma (`GET /user/{name}/about`), cached for 7 days.
4. Counts a ticker only when several established accounts discuss it. Tickers pushed mainly by brand-new or single-topic accounts are treated as likely spam and ignored.

Example: 8 established accounts mention `$ABCD` within a few hours → it goes on the private watchlist. Only 3 week-old accounts posting nothing but `$ABCD` → it is flagged and ignored.

## API usage
- OAuth app-only (client credentials), read-only scopes.
- ~5–10 requests per minute, well under Reddit's 100 QPM limit. Honours `X-Ratelimit-*` headers.
- Descriptive User-Agent: `linux:subwatch-personal:0.1 (by /u/pawariton)`.

## Data handling
- Stored privately for a single user. Never shared, published or sold.
- Not used to train AI/ML models.
- Deleted after 90 days; content deleted on Reddit is removed when detected.

## Why not Devvit
Devvit apps are installed by a subreddit's moderators and run inside that subreddit. This tool only needs read-only access to public posts across several subreddits the author does not moderate, combined with the author's own off-platform data.

## Files
- `subwatch_readonly.py`: the read-only API client (token, subreddit listings, author lookup). Credentials are read from a local `.env.reddit` file, which is never committed.
