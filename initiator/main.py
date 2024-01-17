import os
import subprocess
import paho.mqtt.client as mqtt

BROKER_ADDRESS = "mqtt.eclipseprojects.io"
BROKER_PORT = 1883  # Default MQTT port

# Tarball path and TOPIC
TOPIC = "ansible/initiator/hostid/123456789"

SAVE_DIR = f"/tmp/initiator_payloads/{os.getpid()}"
os.makedirs(SAVE_DIR, exist_ok=True)  # Ensure folder exists

def on_connect(client, userdata, flags, rc):
    print("DEBUG::on_connect: function entry")
    if rc == 0:
        print("Connected to MQTT broker...")
        client.subscribe(TOPIC)
    else:
        print("Failed to connect, return code %d...", rc)
    print("DEBUG::on_connect: function exit")

def on_message(client, userdata, msg):
    print("DEBUG::on_message: function entry")
    print("Received tarball data on TOPIC:", msg.topic)
    filename = f"{SAVE_DIR}/received_payload_{os.getpid()}"

    with open(filename, "wb") as payload_file:
        payload_file.write(msg.payload)

    output = subprocess.Popen(
        f"cat {filename}|ansible-runner worker|ansible-runner process ./{SAVE_DIR}",
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE
    )


    client.disconnect()
    print("DEBUG::on_message: function exit")


if __name__ == '__main__':
    print("Starting initiator...")
    print("DEBUG::main: creating MQTT client")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print("Connecting to MQTT broker...")
    client.connect(BROKER_ADDRESS, BROKER_PORT)
    client.loop_forever()

