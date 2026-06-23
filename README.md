# Arc Activity Tracker

Arc Activity Tracker is a full-stack wallet analytics dashboard for the Arc Testnet. It turns raw wallet activity into readable scores, risk signals, protocol insights, watchlist trends, and portfolio-ready reports.

The project is built for hackathon demos, ecosystem analytics, and wallet intelligence experiments. It combines a FastAPI backend, Arc RPC and ArcScan data, SQLite score history, and a Streamlit frontend.

## Features

- Wallet summary analytics with balance, score, badge, grade, risk, protocol count, activity counters, timeline, strengths, weaknesses, and recommendations.
- Wallet intelligence insights that suggest actions such as UnitFlow swaps, UnitFlow liquidity, PredictMarket usage, and broader Arc ecosystem interactions.
- Watchlist manager with score change tracking, previous score, current score, delta, and increase/decrease indicators.
- Dashboard with visual score cards for Wallet Health, Sybil Risk, Activity Level, and Protocol Count.
- System analytics for ecosystem health, wallet growth, grade distribution, protocol ranking, risk distribution, and supported protocols.
- Wallet comparison page for score, balance, transactions, transfers, protocol overlap, and risk comparison.
- Leaderboard for top tracked wallets.
- Historical score and balance charts using saved score snapshots.
- PDF wallet report generation support.
- Arc protocol detection for UnitFlow, PredictMarket, XyloVault, and XyloStablePool.

## Screenshots

Add screenshots or GIFs here before submitting to GitHub or a hackathon gallery.

Recommended captures:

| Page | Suggested Screenshot |
| --- | --- |
| Dashboard | `screenshots/dashboard.png` |
| Wallet Analytics | `screenshots/wallet-analytics.png` |
| Watchlist | `screenshots/watchlist.png` |
| Comparison | `screenshots/comparison.png` |
| System Analytics | `screenshots/system-analytics.png` |
| Leaderboard | `screenshots/leaderboard.png` |

Example Markdown:

```md
![Dashboard](screenshots/dashboard.png)
![Wallet Analytics](screenshots/wallet-analytics.png)
```

## API Endpoints

The backend is served by FastAPI under the `/wallets` prefix.

### Network And Ecosystem

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/wallets/status` | Check Arc RPC connectivity and latest block. |
| `GET` | `/wallets/analytics` | Return ecosystem totals such as wallets, snapshots, average score, and average balance. |
| `GET` | `/wallets/ecosystem-trend` | Return wallet, snapshot, and average score growth values. |
| `GET` | `/wallets/health-score` | Return ecosystem health score. |
| `GET` | `/wallets/top-protocols` | Return supported Arc protocols. |
| `GET` | `/wallets/protocol-ranking` | Rank protocols by tracked usage. |
| `GET` | `/wallets/risk-distribution` | Return low, medium, and high risk distribution. |
| `GET` | `/wallets/grade-distribution` | Return grade counts across latest tracked snapshots. |

### Wallet Intelligence

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/wallets/{address}/summary` | Return full wallet summary, score, risk, activity, protocols, timeline, strengths, weaknesses, and recommendations. |
| `GET` | `/wallets/{address}` | Return wallet balance. |
| `GET` | `/wallets/{address}/details` | Return ArcScan address details. |
| `GET` | `/wallets/{address}/activity` | Return transaction and token transfer counters. |
| `GET` | `/wallets/{address}/transactions` | Return recent wallet transactions from ArcScan. |
| `GET` | `/wallets/{address}/protocols` | Return detected protocol list and protocol count. |
| `GET` | `/wallets/{address}/timeline` | Return recent protocol/action timeline. |
| `GET` | `/wallets/{wallet}/history` | Return saved score history snapshots for a wallet. |

### Watchlist And Rankings

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/wallets/watchlist` | Return saved watchlist addresses. |
| `GET` | `/wallets/watchlist-status` | Return current score, previous score, delta, and direction for each watchlisted wallet. |
| `POST` | `/wallets/watchlist/{address}` | Add a wallet to the watchlist. |
| `DELETE` | `/wallets/watchlist/{address}` | Remove a wallet from the watchlist. |
| `GET` | `/wallets/leaderboard` | Return ranked wallets from the watchlist. |
| `GET` | `/wallets/ranking` | Return latest score ranking from score history. |
| `GET` | `/wallets/top-wallets` | Return top score history rows. |

## Architecture

```text
Arc Activity Tracker
+-- frontend/
|   +-- App.py
|   +-- pages/
|       +-- Dashboard.py
|       +-- Analytics.py
|       +-- System_Analytics.py
|       +-- Comparison.py
|       +-- History.py
|       +-- Leaderboard.py
|       +-- Watchlist.py
+-- backend/
|   +-- main.py
|   +-- api/
|   |   +-- wallets.py
|   +-- models/
|   |   +-- database.py
|   |   +-- wallet.py
|   |   +-- score_history.py
|   +-- services/
|       +-- arc_rpc.py
|       +-- arcscan.py
|       +-- score.py
|       +-- risk.py
|       +-- grade.py
|       +-- ecosystem.py
|       +-- wallet_intelligence.py
|       +-- protocol_analytics.py
|       +-- leaderboard.py
|       +-- timeline.py
|       +-- watchlist.py
+-- data/
|   +-- watchlist.json
+-- activity_tracker.db
+-- requirements.txt
```

### Data Flow

1. The Streamlit frontend requests wallet or ecosystem data from FastAPI.
2. FastAPI calls Arc Testnet RPC and ArcScan API services.
3. Backend services calculate score, grade, risk, protocol usage, activity timeline, and wallet intelligence insights.
4. Wallet summary requests save score snapshots into SQLite.
5. Watchlist status compares the two most recent score snapshots to show score movement.
6. Streamlit renders metrics, score cards, charts, tables, and wallet reports.

### Tech Stack

- Frontend: Streamlit, Pandas
- Backend: FastAPI, Uvicorn
- Database: SQLite, SQLAlchemy
- Blockchain access: Web3.py, Arc Testnet RPC
- Explorer data: ArcScan API
- Reporting: ReportLab

## Installation

### 1. Clone The Repository

```bash
git clone https://github.com/your-username/arc-activity-tracker.git
cd arc-activity-tracker
```

### 2. Create A Virtual Environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start The Backend

```bash
uvicorn backend.main:app --reload
```

FastAPI will run at:

```text
http://127.0.0.1:8000
```

Interactive API docs:

```text
http://127.0.0.1:8000/docs
```

### 5. Start The Frontend

In a second terminal:

```bash
streamlit run frontend/App.py
```

Streamlit will usually run at:

```text
http://localhost:8501
```

## Usage

### Analyze A Wallet

1. Open the Streamlit app.
2. Enter an Arc wallet address.
3. View balance, score, badge, grade, risk, protocol activity, timeline, and wallet recommendations.

### Track Watchlist Score Changes

1. Go to the Watchlist page.
2. Add one or more wallet addresses.
3. Visit wallet summaries over time to create score snapshots.
4. Open Watchlist again to see current score, previous score, delta, and movement indicator.

### Explore Ecosystem Analytics

Use the Dashboard and System Analytics pages to inspect:

- Wallet Health
- Sybil Risk
- Activity Level
- Protocol Count
- Grade distribution
- Risk distribution
- Protocol ranking
- Leaderboard trends

### Compare Wallets

Use the Comparison page to compare two wallets across:

- Score
- Balance
- Transactions
- Token transfers
- Protocol count
- Protocol overlap
- Risk

## Scoring Model

The current scoring model is intentionally transparent for hackathon review:

```text
score = transactions_count // 10
      + token_transfers_count // 20
      + protocol_count * 100
```

Badges:

| Score | Badge |
| --- | --- |
| `500+` | Legend |
| `300+` | Master |
| `150+` | Explorer |
| `<150` | Newbie |

Risk is derived from low transaction activity and missing protocol activity.

## Roadmap

- Add screenshot assets and demo GIFs for each page.
- Add authentication for private watchlists.
- Add scheduled background jobs to refresh watchlist scores automatically.
- Expand protocol detection with contract address mappings and decoded event logs.
- Add richer Sybil heuristics such as wallet age, repeated funding source, burst activity, and protocol diversity decay.
- Add CSV export for wallet history, leaderboard, and watchlist status.
- Add test coverage for scoring, risk, protocol detection, wallet intelligence, and API response shapes.
- Add Docker and docker-compose setup for one-command local launch.
- Add hosted demo deployment.
- Add configurable RPC, explorer, and database settings through environment variables.

## Hackathon Notes

Arc Activity Tracker is designed to show how wallet analytics can help users understand their on-chain reputation and discover ecosystem actions. It is useful for:

- New user onboarding
- Ecosystem growth dashboards
- Protocol engagement tracking
- Wallet reputation experiments
- Sybil and activity quality research

The project favors explainable scoring and visible recommendations so judges, developers, and users can understand how each wallet profile is produced.

## License

Add your preferred license before publishing.
