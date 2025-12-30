import paho.mqtt.client as mqtt
import json
import logging

class OTAEventListener:
    def __init__(self, broker, vehicle_id, on_notify=None, on_wake=None, on_stop=None):
        self.broker = broker
        self.vehicle_id = vehicle_id
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.on_notify_cb = on_notify
        self.on_wake_cb = on_wake
        self.on_stop_cb = on_stop

    def start(self):
        try:
            self.client.connect(self.broker, 1883, 60)
            self.client.loop_start()
            logging.info("MQTT Client connected and listening.")
        except Exception as e:
            logging.error(f"MQTT Connection failed: {e}")

    def stop(self):
        self.client.loop_stop()

    def on_connect(self, client, userdata, flags, rc):
        logging.info(f"MQTT Connected with result code {rc}")
        # Subscribe to topics
        topics = [
            f"v1/vehicles/{self.vehicle_id}/ota/notify",
            f"v1/vehicles/{self.vehicle_id}/ota/wake",
            f"v1/fleet/ota/emergency_stop"
        ]
        for t in topics:
            client.subscribe(t)
            logging.info(f"Subscribed to {t}")

    def on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            topic = msg.topic
            
            if "notify" in topic and self.on_notify_cb:
                self.on_notify_cb(payload)
            elif "wake" in topic and self.on_wake_cb:
                self.on_wake_cb(payload)
            elif "emergency_stop" in topic and self.on_stop_cb:
                self.on_stop_cb(payload)
                
        except Exception as e:
            logging.error(f"Failed to handle MQTT message: {e}")

    def publish_heartbeat(self, status):
        topic = f"v1/vehicles/{self.vehicle_id}/ota/heartbeat"
        self.client.publish(topic, json.dumps(status))
