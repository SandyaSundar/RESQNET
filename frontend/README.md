# RESQNET Frontend

React and Vite interface for the RESQNET FastAPI simulation API.

## Local development

From this directory, copy `.env.example` to `.env`, run `npm ci`, then `npm run dev`. Leave `VITE_BACKEND_URL` blank locally so Vite proxies `/api` to `http://127.0.0.1:8000`.

## Vercel production

Keep the existing Vercel project Root Directory set to `frontend`. The submitted app URL is `https://resqnet-eight-psi.vercel.app`. Set the Vercel Production environment variable `VITE_BACKEND_URL` to the deployed backend's public origin, with no trailing slash. The actual backend origin is not in this repository; obtain it from the hosting provider before deploying. Vercel's rewrite supports frontend routes; API requests go directly to the backend origin.