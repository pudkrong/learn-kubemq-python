"""
Script to subscribe to Kubemq events and forward them to a queue.

This application listens for events on the specified subscription channel,
then forwards those events to a target queue channel for further processing.
"""

import time
from dotenv import load_dotenv
import os
import kubemq.pubsub as pubsub
import kubemq.queues as queues
load_dotenv()

# Configuration constants
KUBEMQ_SERVER_ADDRESS = os.getenv("KUBEMQ_SERVER_ADDRESS")
EVENT_SUBSCRIPTION_CHANNEL = os.getenv("EVENT_SUBSCRIPTION_CHANNEL")
QUEUE_DESTINATION_CHANNEL = os.getenv("QUEUE_DESTINATION_CHANNEL")

print(f"[Env] {KUBEMQ_SERVER_ADDRESS}")

def main():
    """Main application logic:
    1. Initialize Kubemq clients
    2. Set up event subscription
    3. Keep the application running until user termination
    4. Gracefully release resources on exit
    """
    try:
        # Initialize clients for PubSub and Queue operations
        pubsub_client = pubsub.Client(
            address=KUBEMQ_SERVER_ADDRESS,
            client_id="event-forwarder"
        )
        queue_client = queues.Client(
            address=KUBEMQ_SERVER_ADDRESS,
            client_id="queue-sender"
        )

        def on_receive_event(event: pubsub.EventMessageReceived):
            """Handle incoming events by forwarding them to the command queue."""
            # Decode and log received event details
            message = event.body.decode("utf-8")
            print(f"[Event Received] Id:{event.id}, From:{event.from_client_id}, Body:{message}")

            # Send the message to the target queue channel
            send_result = queue_client.send_queues_message(
                queues.QueueMessage(
                    channel=QUEUE_DESTINATION_CHANNEL,
                    body=event.body,
                )
            )
            print(f"[Forwarded to Queue] Result: {send_result}")

        def on_error_handler(err: str):
            """Handle subscription errors."""
            print(f"[ERROR] Subscription encountered error: {err}")

        # Configure event subscription
        subscription = pubsub.EventsSubscription(
            channel=EVENT_SUBSCRIPTION_CHANNEL,
            group="",
            on_receive_event_callback=on_receive_event,
            on_error_callback=on_error_handler,
        )

        # Setup cancellation for graceful shutdown
        cancellation_source = pubsub.CancellationToken()
        pubsub_client.subscribe_to_events(
            subscription=subscription,
            cancel=cancellation_source
        )

        print(f"Started listening on channel '{EVENT_SUBSCRIPTION_CHANNEL}'.")

        # Keep application running until user terminates
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nGracefully shutting down...")
        if 'cancellation_source' in locals():
            cancellation_source.cancel()
            print("Subscription unsubscribed successfully.")
        print("Application terminated by user.")
    except Exception as e:
        print(f"[FATAL] {e}")
        if 'cancellation_source' in locals():
            cancellation_source.cancel()
    finally:
        # Ensure clients are closed properly
        if 'pubsub_client' in locals():
            pubsub_client.close()
        if 'queue_client' in locals():
            queue_client.close()

if __name__ == "__main__":
    main()
