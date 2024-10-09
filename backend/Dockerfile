FROM python:3.7.3-stretch

## Step 1:
# Create a working directory
WORKDIR /app/

## Step 2:
# Copy source code to working directory
COPY . /app/
# COPY . nlib /app/

## Step 3:
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt
# hadolint ignore=DL3013
#RUN python3 -m unittest discover -s ./backend -p '*_test.py'

## Step 4:
# Expose port 80
EXPOSE 80

## Step 5:
# Run app.py at container launch
CMD ["python","app.py"]
