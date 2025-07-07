# 1. Base image with Python pre-installed
FROM python:3.11-slim

# 2. set environment variables
# avoid __pycache__
ENV PYTHONDONTWRITEBYTECODE 1 

# shows logs in real time
ENV PYTHONUNBUFFERED 1

# 3. set the working directory in the container
WORKDIR /app

# 4. copy only requirements file first for faster caching
COPY requirements.txt .

# 5. install python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. copy the whole django project into /app
COPY . .

# 7. run django dev server port 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]