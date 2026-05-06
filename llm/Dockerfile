# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# Copy only requirements first — maximises layer cache reuse
COPY requirements.txt .

# Install deps into an isolated prefix so we can copy them cleanly
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Stage 2: runtime ─────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Security: never run as root in production
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Pull compiled deps from builder (no pip/build tools in final image)
COPY --from=builder /install /usr/local

# Copy application source
COPY --chown=appuser:appgroup . .

# Runtime config — PORT matches what your entrypoint reads from os.environ
ENV PORT=8000 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

EXPOSE ${PORT}

USER appuser

# Use exec-form so signals (SIGTERM) reach uvicorn directly, not a shell
ENTRYPOINT ["python", "server.py"]