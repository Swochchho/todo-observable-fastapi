# 📋 FastAPI To-Do App with Prometheus & Grafana Monitoring

This is a simple yet modern to-do list application built with **FastAPI** and **SQLModel**, featuring real-time monitoring using **Prometheus** and **Grafana**. The frontend is styled with **Tailwind CSS** for a clean and responsive interface.

---

## 🚀 Features

- 🧾 Add, complete, and delete tasks
- 📈 Built-in Prometheus metrics for API observability
- 📊 Grafana dashboard support
- 🔥 Modern Tailwind-based frontend
- 🐳 Dockerized with `docker-compose`

---

## 🛠️ Tech Stack

- Backend: [FastAPI](https://fastapi.tiangolo.com/)
- ORM: [SQLModel](https://sqlmodel.tiangolo.com/)
- DB: SQLite (file-based)
- Monitoring: Prometheus + Grafana
- Metrics: `prometheus_client`
- Containerization: Docker + Docker Compose
- Frontend: HTML + TailwindCSS

---

## 📁 Project Structure
├── fastapi-app/
│ ├── main.py
│ ├── requirements.txt
│ └── static/
│ └── index.html
├── monitoring/
│ └── prometheus.yml
├── .gitignore
├── docker-compose.yml
├── LICENSE
└── README.md

---

## ⚙️ Getting Started

### Prerequisites

- Docker & Docker Compose installed

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/observability-todo.git
cd observability-todo
2. Start the app
bash
Copy
Edit
docker-compose up --build
FastAPI app: http://localhost:8000

Prometheus: http://localhost:9090

Grafana: http://localhost:3000

Default Grafana credentials:
User: admin
Pass: admin

📡 Prometheus Metrics
Metrics are exposed at:

bash
Copy
Edit
http://localhost:8000/metrics
Prometheus scrapes this endpoint based on monitoring/prometheus.yml.

Metrics include:

http_requests_total

http_request_duration_seconds

tasks_created_total

tasks_completed_total

📊 Grafana Setup
Login to Grafana: http://localhost:3000

Add Prometheus as a Data Source: http://prometheus:9090

Import a dashboard or create a new one

Visualize your API metrics 🚀

✅ Example API Routes
Method	Endpoint	Description
GET	/	Serve frontend UI
POST	/add	Add a new task
GET	/complete/{id}	Mark task as complete
GET	/delete/{id}	Delete a task
GET	/metrics	Prometheus metrics

📦 Install Python Locally (optional)
If you want to run it without Docker:

bash
Copy
Edit
cd fastapi-app
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
🧠 Future Ideas
PostgreSQL support

User authentication

Task due dates & reminders

Container health checks

🙌 Credits
Built with ❤️ by Your Name

