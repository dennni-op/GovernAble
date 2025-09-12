# Dockerfile

# 1. Start from an official, lightweight Python base image.
# This gives us a clean Linux environment with Python 3.11 already installed.
FROM python:3.11-slim

# 2. Set the working directory inside the container.
# This is where our application code will live.
WORKDIR /app

# 3. Copy the requirements file first.
# This is a clever optimization. Docker builds in layers. By copying and
# installing the requirements first, Docker won't have to re-install all the
# libraries every single time you change your application code. It only re-runs
# this step if requirements.txt itself changes.
COPY requirements.txt requirements.txt

# 4. Install the Python dependencies.
# The --no-cache-dir flag is a good practice to keep the image size smaller.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your application code into the container.
# The first '.' means "everything in the current directory on your computer".
# The second '.' means "copy it into the working directory (/app) inside the container".
COPY . .

# Note: We don't need a CMD or ENTRYPOINT here because the 'command' in
# docker-compose.yml will override it. This is a great pattern for development.