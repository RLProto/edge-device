import logging
import os

from asyncua import Client, ua
from asyncua.ua import VariantType

OPCUA_URL = os.getenv("HOST_OPC")

if not OPCUA_URL:
    OPCUA_URL = "nodered"


class OPCUA:
    def __init__(self):
        """
        Initializes the OPCUA class and sets up the OPC UA client.
        """
        self.setup_opcua_client()

    def setup_opcua_client(self) -> None:
        """
        Sets up the OPC UA client connection settings including the server URL and session timeout.
        """
        self.opcua_url = f"opc.tcp://{OPCUA_URL}:53880/UA/VisionOPC"
        self.client = Client(self.opcua_url)
        self.client.session_timeout = 600000

    async def _opcua_write(self, node_id, value, variant_type) -> None:
        """
        Asynchronously writes a value to a specified node on the OPC UA server.

        Args:
            node_id (str): The node identifier.
            value (Any): The value to be written to the node.
            variant_type (VariantType): The type of the value as defined in OPC UA.

        Raises:
            ua.uaerrors._auto.BadNodeIdUnknown: If the specified node ID does not exist.
            Exception: If any other error occurs during the operation.
        """
        try:
            await self.client.connect()
            logging.info(f"Trying to access Node ID: ns=1;s={node_id}")
            result = ua.DataValue(ua.Variant(value, variant_type))
            node = self.client.get_node(f"ns=1;s={node_id}")
            await node.set_value(result)
        except ua.uaerrors._auto.BadNodeIdUnknown as e:
            logging.error(
                f"Node ID not found: {e} - Check the Node ID and Namespace index."
            )
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        finally:
            await self.client.disconnect()

    async def send_values_OPC(self, predictions) -> None:
        """
        Sends prediction results to the OPC UA server by writing to specific nodes.

        Args:
            predictions (dict): A dictionary containing 'classification' and 'confidence-score' of the prediction.
        """
        predicted_class = predictions["classification"]
        predicted_accuracy = float(predictions["confidence-score"])
        await self._opcua_write("classePrevista", predicted_class, VariantType.String)
        await self._opcua_write("valorPrevisto", predicted_accuracy, VariantType.Float)
