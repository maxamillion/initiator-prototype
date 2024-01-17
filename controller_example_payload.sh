### Gross oversimplification of what needs to be done as a shell script
#
#
#

BROKER_HOSTNAME="mqtt.eclipseprojects.io"
BROKER_PORT="1883"
BROKER_TOPIC="ansible/initiator/hostid/123456789"

# detect podman or docker
if [ -x "$(command -v docker)" ]; then
    CONTAINER_ENGINE=docker
elif [ -x "$(command -v podman)" ]; then
    CONTAINER_ENGINE=podman
else
    echo "No container engine found. Exiting."
    exit 1
fi

ansible-runner transmit ./example_payload -p test.yml > /tmp/example_payload.bin

$CONTAINER_ENGINE run --rm -t -v /tmp:/tmp \
    hivemq/mqtt-cli publish -h $BROKER_HOSTNAME -p $BROKER_PORT -t $BROKER_TOPIC \
    --message-file /tmp/example_payload.bin
