# Pull a base image
FROM python:3.7-slim-buster
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 1
ENV SECRET_KEY j_@4)aa&nzqqjqs0xasril1zi(%-w)c4$1)fsahpu@$$&^8@rk
ENV DATABASE_URL postgres://postgres:admin@db:5432/user_polls
ENV DJANGO_SETTINGS_MODULE project.settings.base
# Create a working directory for the django project
WORKDIR /user_polls_app
# Copy requirements to the container
COPY Pipfile Pipfile.lock /user_polls_app/
# Install the requirements to the container
RUN pip install pipenv && pipenv install --system
# Copy the project files into the working directory
COPY . /user_polls_app/
# Open a port on the container
EXPOSE 8000