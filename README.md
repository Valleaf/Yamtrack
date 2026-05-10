# Yamtrack

![App Tests](https://github.com/FuzzyGrim/Yamtrack/actions/workflows/app-tests.yml/badge.svg)
![Docker Image](https://github.com/FuzzyGrim/Yamtrack/actions/workflows/docker-image.yml/badge.svg)
![CodeFactor](https://www.codefactor.io/repository/github/fuzzygrim/yamtrack/badge)
![Codecov](https://codecov.io/github/FuzzyGrim/Yamtrack/branch/dev/graph/badge.svg?token=PWUG660120)
![GitHub](https://img.shields.io/badge/license-AGPL--3.0-blue)

Yamtrack is a self hosted media tracker for movies, tv shows, anime, manga, video games, books, comics, and board games.

## 🚀 Demo

You can try the app at [yamtrack.fuzzygrim.com](https://yamtrack.fuzzygrim.com) using the username `demo` and password `demo`.

## ⚡ Quick Start

Get started with Docker in 5 minutes:

1. **Clone the repository**
   ```bash
   git clone https://github.com/FuzzyGrim/Yamtrack.git
   cd Yamtrack
   ```

2. **Create `.env` file** with required API keys (minimal configuration for testing)
   ```bash
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DOMAIN=localhost:8000
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_ENGINE=sqlite3
   ```
   See [Environment Variables wiki](https://github.com/FuzzyGrim/Yamtrack/wiki/Environment-Variables) for complete list.

3. **Start with Docker Compose**
   ```bash
   docker-compose up -d
   ```

4. **Open browser** and navigate to http://localhost:8000

5. **Create account** and start tracking your media!

For production deployment, see the [Installation](#-installing-with-docker) section below.

## ✨ Features

- 🎬 Track movies, tv shows, anime, manga, games, books, comics, and board games.
- 📺 Track each season of a tv show individually and episodes watched.
- ⭐ Save score, status, progress, repeats (rewatches, rereads...), start and end dates, or write a note.
- 📈 Keep a tracking history with each action with a media, such as when you added it, when you started it, when you started watching it again, etc.
- ✏️ Create custom media entries, for niche media that cannot be found by the supported APIs.
- 📂 Create personal lists to organize your media for any purpose, add other members to collaborate on your lists.
- 📅 Keep up with your upcoming media with a calendar, which can be subscribed to in external applications using a iCalendar (.ics) URL.
- 🔔 Receive notifications of upcoming releases via Apprise (supports Discord, Telegram, ntfy, Slack, email, and many more).
- 🐳 Easy deployment with Docker via docker-compose with SQLite or PostgreSQL.
- 👥 Multi-users functionality allowing individual accounts with personalized tracking.
- 🔑 Flexible authentication options including OIDC and 100+ social providers (Google, GitHub, Discord, etc.) via django-allauth.
- 🦀 Integration with [Jellyfin](https://jellyfin.org/), [Plex](https://plex.tv/) and [Emby](https://emby.media/) to automatically track new media watched.
- 📥 Import from [Trakt](https://trakt.tv/), [Simkl](https://simkl.com/), [MyAnimeList](https://myanimelist.net/), [AniList](https://anilist.co/) and [Kitsu](https://kitsu.app/) with support for periodic automatic imports.
- 📊 Export all your tracked media to a CSV file and import it back.

## 📱 Screenshots

| Homepage                                                                                       | Calendar                                                                                    |
| ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/homepage.png?v2" alt="Homepage" /> | <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/calendar.png" alt="calendar" /> |

| Media List Grid                                                                                    | Media List Table                                                                                     |
| -------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/medialist_grid.png" alt="List Grid" /> | <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/medialist_table.png" alt="List Table" /> |

| Media Details                                                                                         | Tracking                                                                                    |
| ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/media_details.png" alt="Media Details" /> | <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/tracking.png" alt="Tracking" /> |

| Season Details                                                                                          | Tracking Episodes                                                                                            |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/season_details.png" alt="Season Details" /> | <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/tracking_episode.png" alt="Tracking Episodes" /> |

| Lists                                                                                 | Statistics                                                                                      |
| ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/lists.png" alt="Lists" /> | <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/statistics.png" alt="Statistics" /> |

| Create Manual Entries                                                                                         | Import Data                                                                                       |
| ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/create_custom.png" alt="Create Manual Entries" /> | <img src="https://cdn.fuzzygrim.com/file/fuzzygrim/yamtrack/import_data.png" alt="Import Data" /> |

## 🏗️ Architecture

Yamtrack is built with a modern full-stack architecture:

**Technology Stack**:
- **Backend**: Django (Python web framework) with DRF for APIs
- **Frontend**: Django templates + HTMX for dynamic interactions
- **Database**: SQLite (default) or PostgreSQL
- **Cache**: Redis for sessions and async task queuing
- **Async Tasks**: Celery with Beat scheduler for periodic imports

**System Components**:

| Component | Purpose |
|-----------|---------|
| **`app/`** | Core media tracking: models (Movie, TV, Anime, etc.), views, business logic, search integration |
| **`integrations/`** | External service connections: OAuth flows, webhooks (Jellyfin/Plex/Emby), import pipeline |
| **`users/`** | Authentication, account management, notifications |
| **`events/`** | Calendar generation, recurring event scheduling, iCalendar (.ics) export |
| **`lists/`** | Custom lists, categories, collaboration features |

**Data Flow**:
1. **User Action** (track media, import data, schedule tasks)
2. **View** (validates input, handles auth)
3. **Business Logic** (models, helpers, external APIs)
4. **Database** (persistent storage + audit trail via simple-history)
5. **Background Tasks** (Celery for imports, notifications, calendar generation)

**Import Pipeline** (detailed in [`.github/IMPORT_PIPELINE.md`](.github/IMPORT_PIPELINE.md)):
```
User Import → Celery Task → Importer Class → Helpers → Bulk DB Operations
```

**Extending Yamtrack**:
- Add new media sources: Extend providers in `app/providers/`
- Add new integrations: Implement Importer class (see [`.github/IMPORTER_DEVELOPMENT.md`](.github/IMPORTER_DEVELOPMENT.md))
- Add new features: Create Django app in `src/` following existing patterns

## 🐳 Installing with Docker

Copy the default `docker-compose.yml` file from the repository and set the environment variables. This would use a SQlite database, which is enough for most use cases.

To start the containers run:

```bash
docker-compose up -d
```

Alternatively, if you need a PostgreSQL database, you can use the `docker-compose.postgres.yml` file.

### 🌊 Reverse Proxy Setup

When using a reverse proxy, set the `URLS` environment variable to the URL you are using for the app. This allows Yamtrack to trust the proxy origin and generate correct public URLs for OAuth redirects and webhook integrations.

```bash
services:
  yamtrack:
    ...
    environment:
      - URLS=https://yamtrack.mydomain.com
    ...
```

Note that the setting must include the correct protocol (`https` or `http`), and must not include the application `/` context path. Multiple origins can be specified by separating them with a comma (`,`).

### ⚙️ Environment variables

For detailed information on environment variables, please refer to the [Environment Variables wiki page](https://github.com/FuzzyGrim/Yamtrack/wiki/Environment-Variables).

## 💻 Local development

Clone the repository and change directory to it.

```bash
git clone https://github.com/FuzzyGrim/Yamtrack.git
cd Yamtrack
```

Install Redis or spin up a bare redis container:

```bash
docker run -d --name redis -p 6379:6379 --restart unless-stopped redis:8-alpine
```

Create a `.env` file in the root directory and add the following variables.

```bash
TMDB_API=API_KEY
MAL_API=API_KEY
IGDB_ID=IGDB_ID
IGDB_SECRET=IGDB_SECRET
STEAM_API_KEY=STEAM_API_SECRET
BGG_API_TOKEN=BGG_API_TOKEN
SECRET=SECRET
DEBUG=True
```

Then run the following commands.

```bash
python -m pip install -U -r requirements-dev.txt
pre-commit install
cd src
python manage.py migrate
python manage.py runserver & celery -A config worker --beat --scheduler django --loglevel DEBUG & tailwindcss -i ./static/css/input.css -o ./static/css/tailwind.css --watch
```

Go to: http://localhost:8000

## 💪 Support the Project

There are many ways you can support Yamtrack's development:

### ⭐ Star the Project

The simplest way to show your support is to star the repository on GitHub. It helps increase visibility and shows appreciation for the work.

### 🐛 Bug Reports

Found a bug? Open an [issue](https://github.com/FuzzyGrim/Yamtrack/issues) on GitHub with detailed steps to reproduce it. Quality bug reports are incredibly valuable for improving stability.

### 💡 Feature Suggestions

Have ideas for new features? Share them through [GitHub issues](https://github.com/FuzzyGrim/Yamtrack/issues). Your feedback helps shape the future of Yamtrack.

### 🧪 Contributing

Pull requests are welcome! Whether it's fixing typos, improving documentation, or adding new features, your contributions help make Yamtrack better for everyone.

### ☕ Donate

If you'd like to support the project financially:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/fuzzygrim)
