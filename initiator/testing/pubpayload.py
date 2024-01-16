import tarfile
import paho.mqtt.client as mqtt

# MQTT broker settings
broker_address = "mqtt.eclipseprojects.io"
broker_port = 1883  # Default MQTT port

# Tarball path and topic
tarball_path = "./example_payload.tar"
topic = "ansible/initiator/hostid/123456789"

# Create MQTT client
client = mqtt.Client()

# Connect to broker
client.connect(broker_address, broker_port)

# Open tarball in binary read mode
with open(tarball_path, "rb") as tarball_file:
    tarball_data = tarball_file.read()

# Publish tarball data to MQTT topic
client.publish(topic, tarball_data, qos=1)  # Set QoS level for reliability

# Disconnect from broker
client.disconnect()

print("Tarball sent successfully!")
