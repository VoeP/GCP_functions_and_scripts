FROM python:3.10
WORKDIR /
COPY . /comment_analytics


# Upgrade pip
RUN pip install --upgrade pip
# Install requirements
RUN pip install -r comment_analytics/requirements.txt

ENV GOOGLE_APPLICATION_CREDENTIALS=comment_analytics/keys/ml-deployments-practice-07806ac06a8f.json

# Run Python script without any output
CMD ["python", "-u", "comment_analytics/main.py"] >> /dev/null 2>&1
