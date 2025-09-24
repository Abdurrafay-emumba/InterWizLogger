# Event Logger API

A simple Python/Flask application that exposes a single POST endpoint (`/log`).  
It accepts an `email` and an `event`, and appends the data to a log file named after the email.  
Each request is stored in **JSON format** along with the current date and timestamp.

---

## Features

- **Single endpoint** (`/log`, method: POST)  
- Accepts JSON payloads like:
  ```json
  {
    "email": "test@test.com",
    "event": "Test Api hit"
  }
  ```
- Saves logs into files inside the `logs/` directory.  
  - The filename is based on the email (non-alphanumeric characters are replaced with `_`).  
  - Each entry contains:
    ```json
    {
        "date": "2025-09-24",
        "timestamp": "14:53:21",
        "email": "test@test.com",
        "event": "Test Api hit"
    }
    ```
- Logs are appended, so multiple hits will create multiple entries.  
- Dockerized for easy deployment.  

---

## Running Locally (without Docker)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. The app will run on `http://127.0.0.1:4598`.

4. Test with curl:
   ```bash
   curl -X POST http://127.0.0.1:4598/log \
     -H "Content-Type: application/json" \
     -d '{"email":"test@test.com","event":"Test Api hit"}'
   ```

5. Logs will appear in `./logs/test_test_com.jsonl` (example filename).

---

## Running with Docker

### Build the Docker image
```bash
docker build -t event-logger .
```

### Run the container
By default, logs are written inside the container at `/app/logs`.  
To persist logs on your host machine, **map a host folder** to the container’s log directory.

```bash
# Create a logs folder on the host
mkdir -p ./host-logs

# Run container with volume mount
docker run -d --name event-logger \
  -p 4598:4598 \
  -v "$(pwd)/host-logs:/app/logs" \
  event-logger
```

### Verify logs
After sending requests, check your host logs:
```bash
cat ./host-logs/test_test_com.jsonl
```

You should see JSON entries for every request.

---

## Example API Call

```bash
curl -X POST http://127.0.0.1:4598/log \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","event":"User signed in"}'
```

This will create (or append to) the file:
```
./host-logs/alice_example_com.jsonl
```
