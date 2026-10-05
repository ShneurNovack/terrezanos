# Terrezano's Ristorante

Tribute website for Terrezano's, the fake Italian restaurant from Saturday Night Live's "Italian Restaurant" sketch (Season 43 premiere, September 30, 2017, hosted by Ryan Gosling).

Static multi-page site served as a Cloudflare Worker with static assets. Live at https://terrezanos.shneur.workers.dev

## Edit and build

All page content lives in `build.py`; shared CSS and JS live in `src/`.

```
python3 build.py      # regenerates ./public
npx wrangler dev      # preview locally
```

Pushing to `main` deploys automatically through Cloudflare Workers Builds.

Not affiliated with NBC, Saturday Night Live or Pizza Hut.
