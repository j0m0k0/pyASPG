from random import random

class CommunicationNetwork:
    """
    Class representing the infrastructure that enables data exchange between smart meters, third-party data aggregators, and utility companies.

    Attributes:
        name (str): The name of the communication network.
        transmitted_data (list): The list of data packets transmitted by the network.
        received_data (list): The list of data packets received by the network.
        reliability (float): The reliability of the network (a factor between 0 and 1).
    """

    def __init__(self, name, reliability=0.99):
        """
        Initialize a CommunicationNetwork instance.

        Args:
            name (str): The name of the communication network.
            reliability (float): The reliability of the network (a factor between 0 and 1).
        """
        if not (0 <= reliability <= 1):
            raise ValueError("Reliability must be between 0 and 1")

        self.name = name
        self.transmitted_data = []
        self.received_data = []
        self.reliability = reliability

    def transmit_data(self, data):
        """
        Simulate the transmission of data.

        Args:
            data (any): The data to be transmitted.

        Returns:
            bool: True if the data was transmitted successfully, False otherwise.
        """
        if random() <= self.reliability:
            self.transmitted_data.append(data)
            return True
        else:
            return False

    def receive_data(self, data):
        """
        Simulate the reception of data.

        Args:
            data (any): The data to be received.

        Returns:
            bool: True if the data was received successfully, False otherwise.
        """
        if random() <= self.reliability:
            self.received_data.append(data)
            return True
        else:
            return False

    def __str__(self):
        """Return a string representation of the communication network."""
        return (f"{self.name} (Reliability: {self.reliability * 100}%, "
                f"Transmitted Data Count: {len(self.transmitted_data)}, "
                f"Received Data Count: {len(self.received_data)})")

# Example usage
def main():
    network = CommunicationNetwork(name="Smart Grid Network", reliability=0.9)
    data_packet_1 = {"meter_id": 1, "usage": 500}
    data_packet_2 = {"meter_id": 2, "usage": 300}

    success_transmit_1 = network.transmit_data(data_packet_1)
    success_transmit_2 = network.transmit_data(data_packet_2)
    success_receive_1 = network.receive_data(data_packet_1)
    success_receive_2 = network.receive_data(data_packet_2)

    print(network)
    print(f"Data Packet 1 Transmit Success: {success_transmit_1}")
    print(f"Data Packet 2 Transmit Success: {success_transmit_2}")
    print(f"Data Packet 1 Receive Success: {success_receive_1}")
    print(f"Data Packet 2 Receive Success: {success_receive_2}")

if __name__ == "__main__":
    main()
