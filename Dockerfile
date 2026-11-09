# The Hollowmere app's box. CI builds it from every release tag (v1.0, v1.1, ...)
# on the production branch and publishes it to ghcr.io.
FROM python:3.12-slim
WORKDIR /app
# Dependencies first: Docker reuses this layer until requirements.txt changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Run as a normal user, not root.
USER 1000
EXPOSE 8000
CMD ["python", "app.py"]
