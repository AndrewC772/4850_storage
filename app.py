import connexion
from connexion import NoContent
import yaml
import logging
import logging.config
import datetime
import json
from threading import Thread
from pykafka import KafkaClient
from pykafka.common import OffsetType
import time

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from base import Base
from device import Device
from network import Network
import os


if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())
    datastore = app_config['datastore']

with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')
logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

logging.info(f"Connecting to DB. Hostname:{datastore['hostname']}, Port:{datastore['port']}")

DB_ENGINE = create_engine(f"mysql+mysqlconnector://{datastore['user']}:{datastore['password']}@{datastore['hostname']}:"
                          f"{datastore['port']}/{datastore['db']}")
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def get_health():
    return 200

def add_device(body):
    session = DB_SESSION()

    device_id = body['device_id']
    device_name = body['device_name']
    device_mac = body['mac']
    device_ip = body['ip']
    device_latency = body['latency']
    network_id = body['network_id']
    trace_id = body['trace_id']

    device = Device(device_id, device_name, device_mac, device_ip, device_latency, network_id, trace_id)
    session.add(device)
    session.commit()
    session.close()
    return trace_id


def get_devices(start_timestamp, end_timestamp):
    session = DB_SESSION()

    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%d %H:%M:%S.%f")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%d %H:%M:%S.%f")
    devices = session.query(Device).filter(and_(Device.date_created >= start_timestamp_datetime, Device.date_created < end_timestamp_datetime))

    return_device_list = []

    for device in devices:
        return_device_list.append(device.to_dict())

    session.close()
    logger.info(f"Query for Device after {start_timestamp} returns {len(return_device_list)} results ")
    return return_device_list, 200


def add_network(body):
    session = DB_SESSION()

    network_id = body['network_id']
    network_name = body['network_name']
    network = body['network']
    subnet_mask = body['subnet_mask']
    device_count = body['device_count']
    if 'gateway' in body:
        gateway = body['gateway'] or None
    else:
        gateway = ""
    if 'dns' in body:
        dns = body['dns'] or None
    else:
        dns = ""
    trace_id = body['trace_id']
    network = Network(network_id, network_name, network, subnet_mask, gateway, dns, device_count, trace_id)
    session.add(network)
    session.commit()
    session.close()
    return trace_id


def get_networks(start_timestamp, end_timestamp):
    session = DB_SESSION()

    start_timestamp_datetime = datetime.datetime.strptime(start_timestamp, "%Y-%m-%d %H:%M:%S.%f")
    end_timestamp_datetime = datetime.datetime.strptime(end_timestamp, "%Y-%m-%d %H:%M:%S.%f")
    networks = session.query(Network).filter(and_(Network.date_created >= start_timestamp_datetime, Network.date_created < end_timestamp_datetime))

    return_network_list = []

    for network in networks:
        return_network_list.append(network.to_dict())

    session.close()
    logger.info(f"Query for Networks after {start_timestamp} returns {len(return_network_list)} results ")
    return return_network_list, 200


def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (app_config["events"]["hostname"],
                          app_config["events"]["port"])

    current_kafka_retries = 0
    max_kafka_retries = app_config["kafka"]["retry"]
    while current_kafka_retries < max_kafka_retries:
        try:
            client = KafkaClient(hosts=hostname)
            topic = client.topics[str.encode(app_config["events"]["topic"])]
            break
        except:
            logger.error(f"Failed to connect to Kafka. Retrying in 5 seconds ")
            time.sleep(app_config["kafka"]["retry_wait"])
        current_kafka_retries += 1

    # Create a consume on a consumer group, that only reads new messages
    # (uncommitted messages) when the service re-starts (i.e., it doesn't
    # read all the old messages from the history in the message queue).
    consumer = topic.get_simple_consumer(consumer_group=b'event_group',
                                         reset_offset_on_start=False,
                                         auto_offset_reset=OffsetType.LATEST)
    # This is blocking - it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode('utf-8')
        msg = json.loads(msg_str)
        logger.info("Message: %s" % msg)
        payload = msg["payload"]
        if msg["type"] == "device":  # Change this to your event type
            # Store the event1 (i.e., the payload) to the DB
            print("device triggered")
            trace_id = add_device(payload)
            event_log_received = f"Stored event post_network request with a trace id of {trace_id}"
            logging.debug(event_log_received)
        elif msg["type"] == "network":  # Change this to your event type
            # Store the event2 (i.e., the payload) to the DB
            print("device triggered")
            trace_id = add_network(payload)
            event_log_received = f"Stored event post_network request with a trace id of {trace_id}"
            logging.debug(event_log_received)

        # Commit the new message as being read
        consumer.commit_offsets()


app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("openapi.yml",
            base_path="/storage",
            strict_validation=True,
            validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    # app.debug = True
    app.run(port=8090)
