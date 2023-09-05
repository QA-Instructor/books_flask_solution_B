# Multi-stage build
# Alpine is a minimal linux variant - useful for tiny docker images.
FROM python:3.11.5-alpine AS builder

# Set this ENV so that we can see the logs
ENV PYTHONUNBUFFERED=1

COPY . /app

# Create a user called flaskapp
# It is more secure to create and run an application as a non-root user
RUN adduser -D flaskapp && chown -R flaskapp: /app

# Install the pipenv environment
RUN pip3 install pipenv

USER flaskapp

WORKDIR /app

# Install the contents of the requirements file
# RUN pipenv install -r ./app/requirements.txt
RUN pipenv install

# Run our tests
RUN /bin/sh run_unit_tests.sh

FROM python:3.11.5-alpine AS production

# Finally, copy artifacts
COPY --from=builder /home/flaskapp /home/flaskapp
COPY --from=builder /app/application /app/application
COPY --from=builder /app/run_app.sh /app/run_app.sh
COPY --from=builder /app/app.py /app/app.py

# Set default address to listen on at runtime
ENV HOST_ADDRESS=0.0.0.0

# pipenv is used to run the flask app
RUN pip3 install pipenv

RUN adduser -D flaskapp && chown -R flaskapp: /app

USER flaskapp
WORKDIR /app

EXPOSE 5000
ENTRYPOINT [ "/bin/sh", "run_app.sh" ]