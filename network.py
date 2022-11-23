from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class Network(Base):
    """ Network """

    __tablename__ = "networks"

    network_id = Column(Integer, primary_key=True)
    network_name = Column(String(250), nullable=False)
    network = Column(String(20), nullable=False)
    subnet_mask = Column(String(20), nullable=False)
    gateway = Column(String(20), nullable=False)
    dns = Column(String(20), nullable=False)
    device_count = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)
    trace_id = Column(String(50), nullable=False)

    def __init__(self, network_id, network_name, network, subnet_mask, gateway, dns, device_count, trace_id):
        """ Initializes a new network with attributes """
        self.network_id = network_id
        self.network_name = network_name
        self.network = network
        self.subnet_mask = subnet_mask
        self.gateway = gateway
        self.dns = dns
        self.device_count = device_count
        self.date_created = datetime.datetime.now()
        self.trace_id = trace_id

    def to_dict(self):
        network_dictionary = {'network_id': self.network_id, 'network_name': self.network_name, 'network': self.network,
                              'subnet_mask': self.subnet_mask, 'gateway': self.gateway, 'dns': self.dns,
                              'device_count': self.device_count, 'date_created': self.date_created,
                              'trace_id': self.trace_id}

        return network_dictionary
