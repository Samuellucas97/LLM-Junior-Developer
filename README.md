<p align="center"> 
  <img style="margin: -30px; max-height: 500px; max-width: 500px; " src="assets/logo.png"   /> 
</p>

<p align="center">

<a href="https://github.com/Ranith1/LLM-Junior-Developer/stargazers" target="blank">
<img src="https://img.shields.io/github/stars/Ranith1/LLM-Junior-Developer?style=flat-square" alt="github-profile-readme-generator stars"/>
</a>
<a href="https://github.com/Ranith1/LLM-Junior-Developer/issues" target="blank">
<img src="https://img.shields.io/github/issues/Ranith1/LLM-Junior-Developer?style=flat-square" alt="github-profile-readme-generator issues"/>
</a>
<a href="https://github.com/Ranith1/LLM-Junior-Developer/pulls" target="blank">
<img src="https://img.shields.io/github/issues-pr/Ranith1/LLM-Junior-Developer?style=flat-square" alt="github-profile-readme-generator pull-requests"/>
</a>

</p>

This MIT-lincesed project comphreends an LLM assistant that embeds a Socratic framework at the system-prompt level, enforcing one-question-at-a-time dialogue, reflective checkpoints, and graduated hints, to promote learning during code generation, explanation, and debugging.


### Table of Contents


- [Socratic Framework](#socratic-framework-&-software-architecture)
- [Quick Start with Docker](#quick-start-with-docker)
- [Local Development Setup](#local-development-setup)
- [Production Environment Variables](#production-environment-variables)
- [Troubleshooting](#troubleshooting)
- [Contributors and How to Contribute](#contributors-and-how-to-contribute)

## Socratic Framework & Software Architecture

The Socratic method (Liu et al., 2024) is central, using inquiry to promote critical thinking and self-directed learning. The method starts with context-based questions that guide learners toward independent reasoning about programming concepts instead of offering direct solutions. The approach uses a step-by-step Socratic questioning sequence, starting with broad exploratory prompts (e.g., "What do you expect this function to do?") and moving to targeted diagnostic questions (e.g., "Why do you think this line causes an error?"). Based on the learner's responses, the tool adapts—refining its next questions or hints—to progressively guide users to discover solutions independently. This interactive, reflective dialogue supports tasks like debugging, code summarisation, and vulnerability detection, while also deepening learners' conceptual understanding of programming principles.

The architecture supports the Socratic framework and system-level prompt for educational interactions. The front-end, implemented using React.js in Typescript, provides a chat interface for Socratic dialogues. The Node.js back-end applies framework logic and the system-level prompt, tracks sessions, detects stuck users, and escalates via emails. LLM integration (ChatGPT) generates questions under refined Socratic system-level prompts, guided by the Socratic-style prompt. MongoDB stores interaction logs for adaptive learning feedback. Notification services alert seniors for pair programming escalation. Data flow ensures Socratic progression: user queries trigger framework steps informed by the system prompt, with responses stored for educational continuity.

<p align="center"> 
  <img style="margin: -30px; max-height: 500px; max-width: 500px;" src="assets/architecture.png"  /> 
</p>

## Quick Start with Docker

The fastest way to get the application running is using Docker Compose, which sets up MongoDB, backend, and frontend automatically.

### Prerequisites
- Docker and Docker Compose installed
- Git

### 1. Clone the Repository
```bash
$ git clone https://github.com/Ranith1/LLM-Junior-Developer.git
Cloning into 'LLM-Junior-Developer'...
remote: Enumerating objects: 1234, done.
remote: Counting objects: 100% (1234/1234), done.
remote: Compressing objects: 100% (890/890), done.
remote: Total 1234 (delta 432), reused 987 (delta 321)
Receiving objects: 100% (1234/1234), 45.67 MiB | 5.20 MiB/s, done.
Resolving deltas: 100% (432/432), done.
$ cd LLM-Junior-Developer
```

### 2. (Optional) Generate JWT Secret
```bash
$ openssl rand -base64 32
A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0U1v2W3x4Y5z6A7b8C9d0E1f2
```
Save this value - you'll need it below.

### 3. (Optional) Create .env File
Create a `.env` file in the root directory for custom configuration:
```bash
JWT_SECRET=your-generated-secret-from-step-2
JWT_EXPIRES_IN=7d
PORT=5001
NODE_ENV=development
FRONTEND_URL=http://localhost:5173
```

If you skip this step, defaults will be used (JWT_SECRET=change-me).

### 4. Start All Services
```bash
$ docker-compose up --build
Building mongodb
Step 1/4 : FROM mongo:latest
 ---> abc123def456
Step 2/4 : COPY ./init /docker-entrypoint-initdb.d
 ---> Using cache

Building backend
Step 1/8 : FROM node:20
 ---> xyz789uvw012
...
Successfully built abc123def456
Successfully tagged llm-junior-developer_backend:latest
Starting mongodb ... done
Starting backend ... done
Starting frontend ... done
```

This will:
- Start MongoDB on port 27017
- Run database initialization script
- Start backend on port 5001
- Start frontend on port 5173

### 5. Access the Application
Open your browser to **http://localhost:5173**

### 6. Stop Services
```bash
$ docker-compose down
Stopping frontend  ... done
Stopping backend   ... done
Stopping mongodb   ... done
Removing frontend  ... done
Removing backend   ... done
Removing mongodb   ... done
Removing network llm-junior-developer_default
```

To also remove the database volume:
```bash
$ docker-compose down -v
Stopping frontend  ... done
Stopping backend   ... done
Stopping mongodb   ... done
Removing frontend  ... done
Removing backend   ... done
Removing mongodb   ... done
Removing network llm-junior-developer_default
Removing volume llm-junior-developer_mongodb_data
```

### Docker Services Overview

| Service | Port | Description |
|---------|------|-------------|
| MongoDB | 27017 | Database |
| Backend | 5001 | Node.js API server |
| Frontend | 5173 | React + Vite dev server |

## Local Development Setup

For development without Docker, follow these steps to run services individually.

### Prerequisites

Before starting, ensure you have the following installed:

- **Node.js** (v20.19+ for frontend, v18+ for backend)
- **MongoDB** (local installation)
- **Python** 3.11+ (for database setup)
- **Git**

### 1️⃣ Clone the Repository
```bash
$ git clone https://github.com/Ranith1/LLM-Junior-Developer.git
Cloning into 'LLM-Junior-Developer'...
remote: Enumerating objects: 1234, done.
remote: Counting objects: 100% (1234/1234), done.
Successfully cloned.
$ cd LLM-Junior-Developer
```

### 2️⃣ Install MongoDB Locally

**On macOS:**
```bash
$ brew tap mongodb/brew
Tapping mongodb/brew...
$ brew install mongodb-community
Installing mongodb-community...
$ brew services start mongodb-community
==> Successfully started `mongodb-community`
$ mongosh --version
21.3.0
```

**On Windows:**
- Download from: https://www.mongodb.com/try/download/community
- Install and start MongoDB service
- Verify with:
```bash
$ mongosh --version
21.3.0
```

**On Linux:**
```bash
$ curl -fsSL https://www.mongodb.org/static/pgp/server-ubuntu2404.asc | sudo gpg --dearmor -o /usr/share/keyrings/mongodb-server-7.0.gpg
$ echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-7.0.gpg ] http://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
$ sudo systemctl start mongod
Started mongod.service
# Follow: https://www.mongodb.com/docs/manual/administration/install-on-linux/
```

### 3️⃣ Set Up the Database

```bash
$ cd database
$ python3 -m venv .venv
created virtual environment PyPy
$ source .venv/bin/activate  # macOS/Linux
# or on Windows: .venv\Scripts\activate
(.venv) $ pip install pymongo python-dotenv
Collecting pymongo
  Downloading pymongo-4.6.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (519 kB)
Successfully installed pymongo-4.6.0 python-dotenv-1.0.1
(.venv) $ touch .env
```

**Add to `database/.env`:**
```env
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=supersecret
MONGODB_URI=mongodb://localhost:27017/junior_llm
MONGO_DB=junior_llm
```

**Run database setup:**
```bash
(.venv) $ python3 db_setup.py
Connecting to MongoDB...
Schema setup complete for DB: junior_llm
```

### 4️⃣ Set Up the Backend

```bash
$ cd ../backend
$ npm install
added 587 packages, and audited 588 packages in 45s
$ touch .env
```

**Add to `backend/.env`:**
```env
MONGODB_URI=mongodb://localhost:27017/junior_llm
DB_NAME=junior_llm
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
JWT_EXPIRES_IN=7d
PORT=5001
NODE_ENV=development
FRONTEND_URL=http://localhost:5173
```

**Generate JWT_SECRET:**
```bash
$ openssl rand -base64 32
A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8S9t0U1v2W3x4Y5z6A7b8C9d0E1f2
```

**Start backend:**
```bash
$ npm run dev
[19:45:22] [nodemon] 3.0.2
✅ MongoDB connected successfully
🚀 Server running on http://localhost:5001
```

### 5️⃣ Set Up the Frontend

```bash
$ cd ../frontend/socratic-ui
$ npm install
added 256 packages, and audited 257 packages in 30s
$ npm run dev

  VITE v5.0.0  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### 6️⃣ Verify Everything Works

1. Open **http://localhost:5173**
2. Click **Sign Up**
3. Create account:
   - Name: Test User
   - Email: test@example.com
   - Password: password123
   - Role: Student
4. You should be redirected to the dashboard

## Production Environment Variables

When deploying to production, configure the following environment variables for each service:

### Backend Service

| Variable | Description | Example |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/junior_llm` |
| `JWT_SECRET` | Secret key for JWT tokens (generate with `openssl rand -base64 32`) | `your-generated-secret-key` |
| `JWT_EXPIRES_IN` | JWT token expiration time | `7d` |
| `PORT` | Backend server port | `5001` |
| `NODE_ENV` | Environment mode | `production` |
| `FRONTEND_URL` | Frontend application URL (for CORS) | `https://your-frontend-domain.com` |

### LLM Server Service

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM integration | `sk-...` |
| `FRONTEND_URL` | Frontend application URL (for CORS) | `https://your-frontend-domain.com` |

### Frontend Service

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_AUTH_BASE_URL` | Backend API URL | `https://your-backend-domain.com` |
| `VITE_API_BASE_URL` | LLM server URL | `https://your-llm-domain.com` |

**Important Notes:**
- Generate JWT_SECRET using: `openssl rand -base64 32`
- Frontend environment variables are baked into the build - rebuild after changes
- Backend/LLM environment variables can be changed without rebuild
- Ensure CORS is properly configured by setting `FRONTEND_URL` to match your actual frontend domain

## Troubleshooting

### Docker Issues

**Container won't start:**
```bash
$ docker-compose logs [service-name]
# Shows service logs
$ docker-compose down -v
Removing containers and volumes...
$ docker-compose up --build
Building and starting services...
```

**MongoDB connection refused:**
- Check service names in connection strings (use `mongodb`, not `localhost`)
- Verify healthcheck passes:
```bash
$ docker-compose ps
NAME                COMMAND                  SERVICE             STATUS              PORTS
mongodb             "mongod"                 mongodb             Up (healthy)        27017/tcp
backend             "npm run dev"            backend             Up                  5001/tcp
frontend            "npm run dev"            frontend            Up                  5173/tcp
```

### Local Development Issues

**MongoDB connection failed:**
```bash
$ brew services start mongodb-community
==> Successfully started `mongodb-community`
# or check connection string in .env
```

**Port already in use:**
```bash
$ lsof -ti:5001 | xargs kill -9  # Backend
$ lsof -ti:5173 | xargs kill -9  # Frontend
```

**Module not found:**
```bash
$ rm -rf node_modules package-lock.json
$ npm install
added 587 packages in 45s
```

**TypeScript errors:**
```bash
$ npm run build
✓ 1234 modules compiled successfully
# If errors persist, delete node_modules and reinstall
```

### Render Deployment Issues

**Backend won't start:**
- Verify MongoDB Atlas IP whitelist includes 0.0.0.0/0
- Check connection string format and password
- View logs in Render dashboard

**LLM Server not starting:**
- Verify OpenAI API key is correct
- Check `requirements.txt` completeness
- View service logs

**Frontend can't connect:**
- Verify `VITE_AUTH_BASE_URL` and `VITE_API_BASE_URL` are correct
- Rebuild frontend after env var changes
- Check CORS settings allow your frontend URL

**CORS errors:**
- Verify `FRONTEND_URL` set correctly in backend/LLM (with https://)
- Check frontend URL matches environment variables exactly
```bash
$ docker-compose logs backend | grep -i cors
[CORS] Allowing requests from https://your-frontend-domain.com
```

**Services are slow:**
- Normal on free tier (services sleep after 15 min)
- First request takes 30-60s to wake up
- Consider paid plan for always-on

## Contributors and How to Contribute

### Current Contributors

<table>
  <tr>
    <td align="center">
      <a href="https://samuellucas97.github.io/">
        <img src="https://avatars.githubusercontent.com/u/26898930?v=4" width="100px;" alt="Samuel Ferino" style="border-radius: 50%;"/><br />
        <sub><b>Samuel Ferino</b></sub>
      </a><br/>
      <sub>Project Manager</sub>
    </td>
    <td align="center">
      <a href="https://research.monash.edu/en/persons/chetan-arora">
        <img src="https://research.monash.edu/files-asset/666537896/Chetan_Headshot_Square.jpg?w=320&f=webp" width="100px;" alt="Dr. Chetan Arora" style="border-radius: 50%;"/><br />
        <sub><b>Dr. Chetan Arora</b></sub>
      </a><br/>
      <sub>Project Manager</sub>
    </td>
    <td align="center">
      <a href="https://research.monash.edu/en/persons/rashina-hoda">
        <img src="https://research.monash.edu/files-asset/671786728/ProfRashinaHoda_MonashUni.jpg?w=320&f=webp" width="100px;" alt="Prof. Rashina Hoda" style="border-radius: 50%;"/><br />
        <sub><b>Prof. Rashina Hoda</b></sub>
      </a><br/>
      <sub>Project Manager</sub>
    </td>
    <td align="center">
      <img src="https://ui-avatars.com/api/?name=Rehan+Ali&size=100&background=28a745&color=fff&rounded=true" width="100px;" alt="Rehan Ali" style="border-radius: 50%;"/><br />
      <sub><b>Rehan Ali</b></sub><br/>
      <sub>Software Developer</sub>
    </td>
    <td align="center">
      <img src="https://ui-avatars.com/api/?name=Zhijun+Chen&size=100&background=6f42c1&color=fff&rounded=true" width="100px;" alt="Zhijun Chen" style="border-radius: 50%;"/><br />
      <sub><b>Zhijun Chen</b></sub><br/>
      <sub>Software Developer</sub>
    </td>
    <td align="center">
      <img src="https://ui-avatars.com/api/?name=Ranith+Pathiranage&size=100&background=fd7e14&color=fff&rounded=true" width="100px;" alt="Ranith Simanmeru Pathiranage" style="border-radius: 50%;"/><br />
      <sub><b>Ranith Simanmeru Pathiranage</b></sub><br/>
      <sub>Software Developer</sub>
    </td>
  </tr>
</table>

### How to Contribute

We welcome contributions from the community! Here's how you can help:

#### 1. **Report Bugs**
Found a bug? Please open an [issue](https://github.com/Ranith1/LLM-Junior-Developer/issues) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment details (OS, Node version, etc.)

#### 2. **Suggest Improvements**
Have an idea? Open a [discussion](https://github.com/Ranith1/LLM-Junior-Developer/discussions) or issue with:
- Feature description
- Use case and benefits
- Any implementation ideas

#### 3. **Submit Code Changes**

**Fork and Clone:**
```bash
$ git clone https://github.com/YOUR-USERNAME/LLM-Junior-Developer.git
$ cd LLM-Junior-Developer
$ git checkout -b feature/your-feature-name
```

**Make Changes:**
- Follow the existing code style
- Add tests for new functionality
- Update documentation as needed

**Commit and Push:**
```bash
$ git add .
$ git commit -m "Add descriptive commit message"
$ git push origin feature/your-feature-name
```

**Submit Pull Request:**
1. Go to [Pull Requests](https://github.com/Ranith1/LLM-Junior-Developer/pulls)
2. Click "New Pull Request"
3. Select your branch and provide a clear description
4. Link any related issues with `Fixes #issue-number`

#### 4. **Contribution Guidelines**
- Keep commits atomic and well-documented
- Update tests and documentation with code changes
- Follow the existing code structure and naming conventions
- Be respectful and constructive in discussions
- Ensure all tests pass before submitting PR

### Development Setup for Contributors

```bash
$ git clone https://github.com/YOUR-USERNAME/LLM-Junior-Developer.git
$ cd LLM-Junior-Developer
$ docker-compose up --build
```

Or for local development:
- See [Local Development Setup](#local-development-setup) section above

**Run Tests:**
```bash
$ docker-compose exec backend npm test
$ docker-compose exec frontend npm test
```
