# Kubemq Event Forwarder to Queue

This application subscribes to Kubemq events and forwards them to a target queue for processing. 

## Installation
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```bash
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Usage
Start the event forwarder:
```bash
python app.py
```

## Configuration
1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit the `.env` file to configure the following parameters:
   - `KUBEMQ_SERVER_ADDRESS`
   - `EVENT_SUBSCRIPTION_CHANNEL`
   - `QUEUE_DESTINATION_CHANNEL`

## Dependencies
Managed via `requirements.txt`. The required packages are:
- `kubemq` (Kubemq Python SDK)
- `python-dotenv`

## Testing
To test the application, follow these steps:

1. Run a kubemq-community docker container:
   ```bash
   docker run -d -p 50000:50000 kubemq/kubemq-community
   ```

2, Run app
   ```bash
   python app.py
   ```

3. Use the kubemq UI to send messages to an event:
   - Open the kubemq UI in your browser at `http://localhost:50000`.
   - Navigate to the "Events" section.
   - Select the event channel you want to send messages to (e.g., `EVENT_SUBSCRIPTION_CHANNEL`).
   - Enter the message payload and click "Send".

4. Monitor the message in the queue:
   - In the kubemq UI, navigate to the "Queues" section.
   - Select the queue channel where the messages are forwarded (e.g., `QUEUE_DESTINATION_CHANNEL`).
   - You should see the forwarded messages in the queue.

5. Verify that the event forwarder is working correctly by checking the console output of the `kubemq-forward` command. It should display the received events and the forwarding results.

By following these steps, you can test the functionality of the Kubemq Event Forwarder to Queue application and ensure that it is correctly forwarding events to the target queue.
