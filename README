# 📚 Books Microservices

A distributed microservices system designed for user authentication, book management, favorites tracking, and email notifications. Built using modern Python frameworks and tools like FastAPI, gRPC, PostgreSQL, RabbitMQ, and deployed with Docker and Kubernetes.

---

## 🔧 Tech Stack

| Layer         | Technologies                                                                 |
|---------------|------------------------------------------------------------------------------|
| **Backend**   | Python, FastAPI, SQLAlchemy, gRPC, JWT, Pydantic, Alembic                    |
| **Messaging** | RabbitMQ (Publisher/Consumer)                                                |
| **Database**  | PostgreSQL, Redis                                                            |
| **Container** | Docker, Docker Compose                                                       |
| **Orchestration** | Kubernetes (k3s), Ingress (Traefik or NGINX), Helm (optional)           |
| **Others**    | Git, Uvicorn, Pydantic, AsyncIO                                              |

---

## 📦 Services Overview

### 🛡️ Auth Service
- **Handles** user registration, login, JWT authentication.
- **Technologies**: FastAPI, Redis (refresh tokens), RabbitMQ (user registration events).
- **gRPC Server**: Provides user data to Favorites Service.

### 📘 Books Service
- **Handles** book listing and details.
- **gRPC Server**: Serves book details to Favorites Service.

### ❤️ Favorites Service
- **Allows** users to mark books as favorites.
- **gRPC Client**: Fetches user and book data via Auth and Books services.
- **Uses** PostgreSQL for storage.

### 📧 Email Service
- **Consumes** user registration messages from RabbitMQ.
- **Sends** confirmation emails asynchronously.

---

## 📁 Project Structure
books-microservices/
├── k8s/ # Kubernetes manifests
├── services/
│ ├── auth_service/
│ ├── books_service/
│ ├── favorites_service/
│ └── email_service/
├── docker-compose.yaml # Optional local testing setup
├── README.md
└── ...


---

## 🚀 Getting Started

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/your-username/books-microservices.git
cd books-microservices
```

### 2️⃣ Build Docker Images

docker build -t auth_service_image:latest ./services/auth_service
docker build -t books_service_image:latest ./services/books_service
docker build -t favorites_service_image:latest ./services/favorites_service
docker build -t email_service_image:latest ./services/email_service

### 3️⃣ Deploy with Kubernetes (k3s or minikube)

kubectl apply -f k8s/

### 4️⃣ Access via Ingress

Example endpoint:
http://localhost/auth/health
http://localhost/books
http://localhost/favorites

⚠️ Make sure your ingress controller (e.g., Traefik) is active.


🔌 API Endpoints

| Service       | Path                 | Method | Description                  |
| ------------- | -------------------- | ------ | ---------------------------- |
| Auth Service  | `/auth/register`     | POST   | Register user                |
|               | `/auth/login`        | POST   | Login user                   |
| Books Service | `/books`             | GET    | List books                   |
| Favorites     | `/favorites`         | GET    | Get favorites by user        |
| Email Service | (Internal, RabbitMQ) | —      | Receives registration events |


📬 Message Flow Example
User registers via Auth Service.

Auth publishes an event to RabbitMQ.

Email Service consumes the event and sends email.

Favorites Service pulls user info via gRPC from Auth Service.


🔐 Auth Flow
JWT Access Token (short-lived)

Refresh Token stored in Redis

Built-in security utilities for route protection


🧪 Testing & Dev
Run locally with Docker Compose (optional)

Unit tests via Pytest

Postman collection available soon


📘 Demo & Code Samples
📂 Check out sample code and mini version of this system [coming soon].


👨‍💻 Author
Ali Sajadian
📧 [sajadian.ali@gmail.com]
🔗 GitHub
🧠 Python & .NET Full-Stack Developer | FastAPI • gRPC • React


📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

---

### ✅ To Do After Adding:
- Replace `https://github.com/your-username/books-microservices.git` with your real GitHub URL.
- Add your contact info and links in the footer.
- (Optional) Include a diagram or architecture image (can generate if needed).

---

Would you like me to create a **microservices architecture diagram** to include in this README?


