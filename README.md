# Kubemq Event Forwarder to Queue

This application subscribes to Kubemq events and forwards them to a target queue for processing. 

## Installation
1. Install dependencies automatically:
   ```bash
   pip install -e .
   ```

## Usage
Start the event forwarder:
```bash
kubemq-forward
```

## Configuration
Edit `app.py` to configure:
- `KUBEMQ_SERVER_ADDRESS`
- `EVENT_SUBSCRIPTION_CHANNEL`
- `QUEUE_DESTINATION_CHANNEL`

## Dependencies
Managed via `setup.py` and `requirements.txt`. The only required package is:
- `kubemq` (Kubemq Python SDK)
