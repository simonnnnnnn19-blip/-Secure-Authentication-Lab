# Secure Authentication Lab

A small, local Flask authentication service that demonstrates defensive
controls, each one proven by automated tests.

## Features

| Requirement | Implementation | Where |
|---|---|---|
| Password hashing | scrypt, per-password random salt (Werkzeug) | `app/store.py` |
| Server-side input validation | Username allow-list regex, password length/complexity, type checks | `app/validation.py` |
| Secure cookies | `HttpOnly`, `Secure`, `SameSite=Strict`, `Max-Age` | `app/auth.py` |
| Logout | Server-side session destroyed + cookie cleared | `app/auth.py`, `app/sessions.py` |
| Session expiry | Server-enforced lifetime (default 15 min) | `app/sessions.py` |
| Rate limiting | 5 failed logins per 5 min per (IP, username), then HTTP 429 | `app/rate_limit.py` |
| Generic errors | One identical message for every login failure | `app/auth.py` |

Extras: timing equalization for unknown usernames, security headers,
no debug mode, no hardcoded secrets.

## Setup

```bash
git clone <your-repo-url>
cd secure-auth-lab
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                 # then edit SECRET_KEY
```

## Run the tests

```bash
python -m unittest -v
```

Saved output from a passing run: [`docs/test-output.txt`](docs/test-output.txt) (29 tests, all OK).

## Run the app

```bash
python run.py        # http://127.0.0.1:5000
```

Try it with curl:

```bash
# Register
curl -X POST localhost:5000/register -H "Content-Type: application/json" \
     -d '{"username":"alice_01","password":"CorrectHorse42"}'

# Login (saves the cookie)
curl -i -c jar.txt -X POST localhost:5000/login -H "Content-Type: application/json" \
     -d '{"username":"alice_01","password":"CorrectHorse42"}'

# Protected page
curl -b jar.txt localhost:5000/profile

# Logout
curl -b jar.txt -X POST localhost:5000/logout -H "Content-Type: application/json" -d '{}'
```

Note: over plain `http://localhost`, browsers/curl will not send `Secure`
cookies back. Keep `COOKIE_SECURE=false` for local demos only; set it to
`true` behind HTTPS. The tests run with `Secure` enabled.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | `/register` | Create an account (validated) |
| POST | `/login` | Start a session (rate limited) |
| POST | `/logout` | End the session |
| GET | `/profile` | Protected; needs a valid session |

## Documentation

See [`docs/SECURITY_NOTE.md`](docs/SECURITY_NOTE.md) for design decisions and limitations.

## Project layout

```
app/        service code (auth, sessions, rate limiting, validation, storage)
tests/      automated tests (unittest)
docs/       test output + security note
run.py      local entry point
```
