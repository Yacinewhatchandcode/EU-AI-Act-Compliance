FROM python:3.11-slim

WORKDIR /app

# Install Python dependencies
RUN pip install --no-cache-dir qrcode[pil] requests

# Copy application code
COPY eu_ai_act.py .
COPY eu_ai_act_server.py .
COPY web/ ./web/

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/stats')" || exit 1

# Run server
CMD ["python", "eu_ai_act_server.py"]
