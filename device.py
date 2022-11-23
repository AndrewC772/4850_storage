from sqlalchemy import Column, Integer, String, DateTime, Numeric
from base import Base
import datetime


class Device(Base):
    """ Device """

    __tablename__ = "devices"

    device_id = Column(Integer, primary_key=True)
    device_name = Column(String(250), nullable=False)
    mac = Column(String(50), nullable=False)
    ip = Column(String(50), nullable=False)
    latency = Column(Numeric, nullable=False)
    network_id = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False)
    trace_id = Column(String(50), nullable=False)

    def __init__(self, device_id, device_name, mac, ip, latency, network_id, trace_id):
        """ Initializes a new device with attributes """
        self.device_id = device_id
        self.device_name = device_name
        self.mac = mac
        self.ip = ip
        self.latency = latency
        self.network_id = network_id
        self.date_created = datetime.datetime.now()
        self.last_update = datetime.datetime.now()
        self.trace_id = trace_id

    def to_dict(self):
        device_dictionary = {'device_id': self.device_id, 'device_name': self.device_name, 'mac': self.mac,
                             'ip': self.ip, 'latency': self.latency, 'network_id': self.network_id,
                             'date_created': self.date_created, 'last_update': self.last_update,
                             'trace_id': self.trace_id}

        return device_dictionary
