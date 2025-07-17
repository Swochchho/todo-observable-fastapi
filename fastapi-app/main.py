from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, Session, SQLModel, create_engine, select
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from pydantic import BaseModel
from typing import List
import time

app = FastAPI(title="Todo API", version="1.0.0")

# CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["endpoint"]
)

TASKS_CREATED = Counter("tasks_created_total", "Total tasks created")
TASKS_COMPLETED = Counter("tasks_completed_total", "Total tasks completed")

# SQLite database
DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(DATABASE_URL, echo=True)

class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    completed: bool = False

# Pydantic models for API
class TodoCreate(BaseModel):
    title: str
    completed: bool = False

class TodoUpdate(BaseModel):
    title: str
    completed: bool

class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool

SQLModel.metadata.create_all(engine)

# Middleware to track metrics
@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    endpoint = request.url.path
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(process_time)
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint).inc()
    return response

@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "todo-api"}

# Todo API endpoints
@app.get("/todos", response_model=List[TodoResponse])
def get_todos():
    """Get all todos"""
    with Session(engine) as session:
        todos = session.exec(select(Todo)).all()
        return [TodoResponse(id=todo.id, title=todo.title, completed=todo.completed) for todo in todos]

@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate):
    """Create a new todo"""
    with Session(engine) as session:
        new_todo = Todo(title=todo.title, completed=todo.completed)
        session.add(new_todo)
        session.commit()
        session.refresh(new_todo)
        TASKS_CREATED.inc()
        return TodoResponse(id=new_todo.id, title=new_todo.title, completed=new_todo.completed)

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    """Get a specific todo by ID"""
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return TodoResponse(id=todo.id, title=todo.title, completed=todo.completed)

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoUpdate):
    """Update a todo"""
    with Session(engine) as session:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        # Track if task was completed
        was_completed = db_todo.completed
        
        db_todo.title = todo.title
        db_todo.completed = todo.completed
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        
        # Increment counter only when task becomes completed
        if not was_completed and todo.completed:
            TASKS_COMPLETED.inc()
            
        return TodoResponse(id=db_todo.id, title=db_todo.title, completed=db_todo.completed)

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    """Delete a todo"""
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        
        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted successfully"}

# API documentation info
from fastapi.responses import FileResponse
import os

@app.get("/", response_class=FileResponse)
def serve_frontend():
    return FileResponse(os.path.join("templates", "index.html"))