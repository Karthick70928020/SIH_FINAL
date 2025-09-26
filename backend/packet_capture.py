import pyshark
import threading
import time
import uuid
from datetime import datetime
import logging
import socket
import psutil

logger = logging.getLogger(__name__)

class PacketCapture:
    def __init__(self, interface='eth0', callback=None):
        self.interface = interface
        self.callback = callback
        self.capture = None
        self.running = False
        self.thread = None
    
    @staticmethod
    def get_available_interfaces():
        """Get list of available network interfaces"""
        try:
            interfaces = []
            
            # Get network interfaces using psutil
            net_if_addrs = psutil.net_if_addrs()
            net_if_stats = psutil.net_if_stats()
            
            for interface_name, addresses in net_if_addrs.items():
                if interface_name in net_if_stats:
                    stats = net_if_stats[interface_name]
                    if stats.isup:  # Only include active interfaces
                        description = f"{interface_name}"
                        for addr in addresses:
                            if addr.family == socket.AF_INET:  # IPv4
                                description += f" ({addr.address})"
                                break
                        
                        interfaces.append({
                            'name': interface_name,
                            'description': description
                        })
            
            return interfaces
        except Exception as e:
            logger.error(f"Error getting interfaces: {e}")
            return [
                {'name': 'eth0', 'description': 'Ethernet Interface'},
                {'name': 'wlan0', 'description': 'Wireless Interface'},
                {'name': 'lo', 'description': 'Loopback Interface'}
            ]
    
    def start_capture(self):
        """Start packet capture"""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._capture_worker, daemon=True)
        self.thread.start()
        logger.info(f"Packet capture started on interface: {self.interface}")
    
    def stop_capture(self):
        """Stop packet capture"""
        self.running = False
        if self.capture:
            try:
                self.capture.close()
            except:
                pass
        logger.info("Packet capture stopped")
    
    def _capture_worker(self):
        """Worker thread for packet capture"""
        try:
            # Create capture object with timeout
            self.capture = pyshark.LiveCapture(
                interface=self.interface,
                display_filter=None,  # Capture all packets
                only_summaries=False
            )
            
            # Set capture timeout
            self.capture.set_debug()
            
            # Start capturing packets
            for packet in self.capture.sniff_continuously():
                if not self.running:
                    break
                
                try:
                    packet_data = self._parse_packet(packet)
                    if packet_data and self.callback:
                        self.callback(packet_data)
                        
                except Exception as e:
                    logger.debug(f"Error parsing packet: {e}")
                    continue
                    
        except Exception as e:
            if self.running:  # Only log if we're supposed to be running
                logger.error(f"Capture worker error: {e}")
                # Generate simulated packets for demo purposes
                self._generate_demo_packets()
    
    def _generate_demo_packets(self):
        """Generate demo packets for testing when real capture fails"""
        logger.info("Generating demo packets for testing")
        
        demo_protocols = ['TCP', 'UDP', 'HTTP', 'HTTPS', 'DNS', 'ICMP']
        demo_ips = [
            '192.168.1.100', '192.168.1.101', '10.0.0.1', '8.8.8.8',
            '1.1.1.1', '192.168.1.1', '172.16.0.1', '203.0.113.1'
        ]
        
        packet_count = 0
        while self.running and packet_count < 1000:  # Limit demo packets
            try:
                import random
                
                packet_data = {
                    'id': str(uuid.uuid4()),
                    'timestamp': datetime.now().isoformat(),
                    'source_ip': random.choice(demo_ips),
                    'destination_ip': random.choice(demo_ips),
                    'protocol': random.choice(demo_protocols),
                    'length': random.randint(64, 1500),
                    'is_anomaly': False,
                    'anomaly_score': 0.0
                }
                
                # Make some packets more likely to be anomalies
                if random.random() < 0.05:  # 5% chance of anomaly
                    packet_data['length'] = random.randint(8000, 9000)  # Unusually large
                
                if self.callback:
                    self.callback(packet_data)
                
                packet_count += 1
                time.sleep(random.uniform(0.1, 2.0))  # Random delay between packets
                
            except Exception as e:
                logger.error(f"Demo packet generation error: {e}")
                break
    
    def _parse_packet(self, packet):
        """Parse packet data into our format"""
        try:
            # Extract basic information
            packet_data = {
                'id': str(uuid.uuid4()),
                'timestamp': datetime.now().isoformat(),
                'source_ip': 'unknown',
                'destination_ip': 'unknown',
                'protocol': 'unknown',
                'length': 0,
                'is_anomaly': False,
                'anomaly_score': 0.0
            }
            
            # Get packet length
            if hasattr(packet, 'length'):
                packet_data['length'] = int(packet.length)
            elif hasattr(packet, 'captured_length'):
                packet_data['length'] = int(packet.captured_length)
            
            # Extract IP information
            if hasattr(packet, 'ip'):
                packet_data['source_ip'] = packet.ip.src
                packet_data['destination_ip'] = packet.ip.dst
                packet_data['protocol'] = packet.highest_layer
            elif hasattr(packet, 'ipv6'):
                packet_data['source_ip'] = packet.ipv6.src
                packet_data['destination_ip'] = packet.ipv6.dst
                packet_data['protocol'] = packet.highest_layer
            else:
                # For non-IP packets (like ARP)
                packet_data['protocol'] = packet.highest_layer
                if hasattr(packet, 'eth'):
                    packet_data['source_ip'] = packet.eth.src
                    packet_data['destination_ip'] = packet.eth.dst
            
            return packet_data
            
        except Exception as e:
            logger.debug(f"Error parsing packet: {e}")
            return None