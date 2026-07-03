# Chess.com Performance Analytics Dashboard
An analytics dashboard of my chess career.

The dashboard is an automated, full stack data pipeline that extracts raw historical game metadata from the public Chess.com API, applies mathematical cleaning using Python/Pandas, and renders an interactive statistical dashboard using React and Recharts.

**[Live Interactive Demo Link Coming Here]**

---

##  Architecture & Tech Stack
* **Data Layer (ETL):** Python 3, Pandas, Requests API Client
* **Presentation Layer:** React (Vite/Esbuild), Recharts (Data Visualizations)
* **Automation/DevOps:** GitHub Actions (Cron schedule workflow execution)

## Key Insights Uncovered
* **Automated Engineering:** Bypasses live server hosting costs by generating a build time static JSON state compiled via daily backend tasks.
* **Resilient Architecture:** Implemented robust handling for structural variations and missing game match variants (e.g., zero-game mathematical handling using Pandas Series evaluation matrices).
