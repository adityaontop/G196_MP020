# Use a slim Python runtime image to keep the container footprint small.
FROM python:3.12-slim

# Set the working directory used by the following build and run steps.
WORKDIR /app

# Copy dependency declarations first so Docker can reuse the install layer.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Add the project source, API application, and trained model artifact.
COPY src ./src
COPY app ./app
COPY models ./models

# Make the source package importable by the API process.
ENV PYTHONPATH=/app/src

# Document the port used by the Uvicorn server.
EXPOSE 8000

# Start the FastAPI app and listen on all container interfaces.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
