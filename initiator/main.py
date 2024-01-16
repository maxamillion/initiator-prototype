import tarfile
import paho.mqtt.client as mqtt

broker_address = "mqtt.eclipseprojects.io"
broker_port = 1883  # Default MQTT port

# Tarball path and topic
tarball_path = "./example_payload.tar"
topic = "ansible/initiator/hostid/123456789"

save_dir = "/tmp/initiator_payloads/"
os.makedirs(save_dir, exist_ok=True)  # Ensure folder exists

def on_connect(client, userdata, flags, rc):
    if rc == 0:
            print("Connected to MQTT broker")
            client.subscribe(topic)
        else:
            print("Failed to connect, return code %d\n", rc)

def on_message(client, userdata, msg):
    print("Received tarball data on topic:", msg.topic)
    filename = f"{save_dir}/received_tarball_{os.getpid()}.tar.gz"

    with open(filename, "wb") as tarball_file:
        tarball_file.write(msg.payload)

    print(f"Tarball saved to: {filename}")

    # Extract the tarball (optional)
    with tarfile.open(filename, "r:gz") as tar:
        tar.extractall(path=save_dir)
        print("Tarball extracted successfully")

def get_work() -> None:
    """
    Prototype for getting an ansible-runner work item from a MQTT broker.
    """

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_address, broker_port)

if __name__ == '__main__':
    get_work()

