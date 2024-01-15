import click

@click.command()
@click.option('--payload', help='Path to ansible-runner transmit payload.')
@click.option('--mqtt-server', help='MQTT server') 
def initiator(payload, mqtt_server) -> None:
    """
    Prototype for initiating an ansible-runner transaction against localhost
    from a MQTT broker.
    """
    print(f'payload: {payload}')
    print(f'mqtt_server: {mqtt_server}')

if __name__ == '__main__':
    initiator()
