FROM python:3.7.3-stretch

## Step 1:
# Create a working directory
WORKDIR /app/

## Step 2:
# Copy source code to working directory
COPY . main.py /app/

## Step 3:
RUN pip install --trusted-host pypi.python.org -r requirements.txt

## Step 4:
EXPOSE 5000

## Step 5:
# Run app.py at container launch
CMD ["python","main.py"]