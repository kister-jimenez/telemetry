import telemetry
import datetime
import os


class ingest:
    use_test_index = False

    def __init__(self, mode="elastic", server="alpine"):
        if mode == "elastic":
            self.db = telemetry.elastic(server=server)

    def _get_schema(self, name):
        loc = os.path.dirname(__file__)
        return os.path.join(loc, "resources", name)

    def log_ad9361_tx_quad_cal_test(
        self,
        test_name,
        device,
        failed,
        iterations,
        channel,
        date=datetime.datetime.now(),
    ):
        """ Upload AD9361 tx quad cal test data to elasticsearch """
        # Create query
        entry = {
            "test_name": test_name,
            "date": date,
            "failed": failed,
            "iterations": iterations,
            "device": device,
            "channel": channel,
        }
        # Setup index if necessary
        self.db.index_name = "dummy" if self.use_test_index else "ad936x_tx_quad_cal"
        s = self.db.import_schema(self._get_schema("ad936x_tx_quad_cal.json"))
        self.db.create_db_from_schema(s)
        # Add entry
        self.db.add_entry(entry)

    def log_lte_evm_test(
        self,
        test_name,
        standard,
        tx_device,
        rx_device,
        tx_sample_rate,
        rx_sample_rate,
        carrier_frequency,
        evm_db,
        iteration,
        date=datetime.datetime.now(),
    ):
        """ Upload LTE EVM tests to elasticsearch """
        # Create query
        entry = {
            "test_name": test_name,
            "date": date,
            "standard": standard,
            "tx_device": tx_device,
            "rx_device": rx_device,
            "tx_sample_rate": tx_sample_rate,
            "rx_sample_rate": rx_sample_rate,
            "carrier_frequency": carrier_frequency,
            "evm_db": evm_db,
            "iteration": iteration,
        }
        # Setup index if necessary
        self.db.index_name = "lte_evm" if not self.use_test_index else "dummy"
        s = self.db.import_schema(self._get_schema("evm_tests_el.json"))
        self.db.create_db_from_schema(s)
        # Add entry
        self.db.add_entry(entry)
