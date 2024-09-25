FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_APP=hello.py
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]