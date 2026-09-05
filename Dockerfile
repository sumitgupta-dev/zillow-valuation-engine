# 1. Use a lightweight Python OS
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy ALL your project files into the container
# (This includes app/, models/, and data/)
COPY . .

# 5. Change directory into the 'app' folder where main.py lives
WORKDIR /app/app

# 6. Expose port 8000
EXPOSE 8000

# 7. Run the FastAPI server
# Notice we use "0.0.0.0" so it can be accessed from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]