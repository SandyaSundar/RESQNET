# RESQNET Frontend

React and Vite client for the RESQNET simulation API.

## Local development

Copy `.env.example` to `.env` and leave `VITE_BACKEND_URL` blank. The browser uses same-origin `/api` requests and Vite proxies them to `http://127.0.0.1:8000` during development.

```powershell
npm ci
npm run dev
```

## Deployment

Keep the existing Vercel project rooted at `frontend`. Set its production environment variable `VITE_BACKEND_URL` to the Railway backend's public origin, with no trailing slash. The backend must allow `https://resqnet-eight-psi.vercel.app` in `CORS_ORIGINS`.

Failure injection is not implemented by the current backend. The UI reports it as unsupported and does not send a failure request.
