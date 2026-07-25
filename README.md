# Saturday Mat — Yoga with Jenny

A single-page website for Jenny's Saturday morning yoga class in Oceanside, CA.

## Project Structure

```
saturday-mat/
├── index.html              # Main site (all styles + scripts inline)
├── manifest.json           # PWA manifest for "Add to Home Screen"
├── service-worker.js       # Offline cache for static assets
├── images/
│   ├── hero.jpg            # Hero photo (the outdoor yoga pose you sent)
│   └── studio-tour.mp4     # ← ADD YOUR STUDIO VIDEO HERE
└── icons/
    ├── icon-192.png        # PWA icon (placeholder — replace with Jenny's logo)
    └── icon-512.png        # PWA icon (placeholder — replace with Jenny's logo)
```

## Before Going Live

Search for `REPLACE:` in `index.html` to find everything that needs updating:

1. **API_DOMAIN** — Ask Devin for the backend URL, then replace `https://api.saturdaymat.com`
2. **Email** — Replace `hello@saturdaymat.com` with Jenny's real email (2 places)
3. **Instagram** — Replace `@saturdaymatyoga` with the real handle
4. **Class style** — Set it (Vinyasa, Slow flow, etc.)
5. **Price** — Set the drop-in rate
6. **Cancellation policy** — Fill in Jenny's policy
7. **Studio video** — Drop the MP4 file at `images/studio-tour.mp4`
8. **Icons** — Replace the placeholder PNGs with real ones (192x192 and 512x512)

## PWA

The site supports "Add to Home Screen" on iOS and Android. The service worker caches the main HTML and hero image so the site loads even without internet.

## GitHub Pages

To deploy:
1. Push this folder to a GitHub repo
2. Settings → Pages → Source: main branch, root folder
3. Once we have a custom domain, add a `CNAME` file with the domain name
