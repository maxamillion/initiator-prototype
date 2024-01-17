### Gross oversimplification of what needs to be done as a shell script
#
#
#

BROKER_HOSTNAME="mqtt.eclipseprojects.io"
BROKER_PORT="1883"
BROKER_CLIENT_TOPIC="ansible/initiator/hostid/123456789"
BROKER_INGRESS_TOPIC="ansible/initiator/ingress/hostid/123456789"
TIMESTAMP=$(date +"%y%m%d%H%M%S")
TIMEOUT=120

# detect podman or docker
if [ -x "$(command -v docker)" ]; then
    CONTAINER_ENGINE=docker
elif [ -x "$(command -v podman)" ]; then
    CONTAINER_ENGINE=podman
else
    echo "No container engine found. Exiting."
    exit 1
fi

$CONTAINER_ENGINE run --rm -t \
    hivemq/mqtt-cli subscribe \
    -h $BROKER_HOSTNAME -p $BROKER_PORT -t $BROKER_CLIENT_TOPIC --rcvMax 1 > /tmp/initiator_input_${TIMESTAMP}.bin &

echo "Waiting for input payload to be published to broker..."
while true
do
    if [ -s /tmp/initiator_input_${TIMESTAMP}.bin ]; then
        break
    fi
    sleep 1
    TIMEOUT=$((TIMEOUT-1))
    if [ $TIMEOUT -eq 0 ]; then
        echo "Timed out waiting for input payload to be published to broker. Exiting."
        exit 1
    fi
done

cat /tmp/initiator_input_${TIMESTAMP}.bin | ansible-runner worker | ansible-runner process /tmp/initiator_output_${TIMESTAMP}/

echo "Ran worker ..."

tar -czf /tmp/initiator_output_${TIMESTAMP}.tar.gz /tmp/initiator_output_${TIMESTAMP}/

echo "Creating tarball of output dir ..."

$CONTAINER_ENGINE run --rm -t -v /tmp:/tmp \
    hivemq/mqtt-cli publish -h $BROKER_HOSTNAME -p $BROKER_PORT -t $BROKER_INGRESS_TOPIC \
    --message-file /tmp/initiator_output_${TIMESTAMP}.tar.gz

echo "Initiator ran the payload and published the results!"
