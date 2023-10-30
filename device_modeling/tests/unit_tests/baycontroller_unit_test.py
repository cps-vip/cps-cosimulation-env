# python3 -m unittest -v tests/unit_tests/baycontroller_unit_test.py

from src.bay_level.bay_device import BayDevice
from src.bay_level.bay_controllers import BayController
import unittest

class TestBayController(unittest.TestCase):

    def setUp(self):
        self.bay = BayController("TestBay")
        self.device1 = BayDevice("Device1", "Active", "IEC61850")
        self.device2 = BayDevice("Device2", "Inactive", "IEC61850")
        self.bay.add_device(self.device1)
        self.bay.add_device(self.device2)

    def test_add_device(self):
        self.assertIn(self.device1, self.bay.devices)
        self.assertIn(self.device2, self.bay.devices)

    def test_remove_device(self):
        self.bay.remove_device(self.device1)
        self.assertNotIn(self.device1, self.bay.devices)
        self.assertIn(self.device2, self.bay.devices)

    def test_get_device_names(self):
        device_names = self.bay.get_device_names()
        self.assertEqual(device_names, ["Device1", "Device2"])

    def test_get_bay_status_active(self):
        self.assertEqual(self.bay.get_bay_status(), "Active")

    def test_get_bay_status_inactive(self):
        self.device1.set_status("Inactive")
        self.assertEqual(self.bay.get_bay_status(), "Inactive")

    def test_set_target_voltage(self):
        self.bay.set_target_voltage(1.5)
        self.assertEqual(self.bay.target_voltage, 1.5)

    def test_measure_voltage(self):
        voltage = self.bay.measure_voltage(self.device1)
        self.assertTrue(self.bay.target_voltage - self.bay.voltage_margin <= voltage <= self.bay.target_voltage + self.bay.voltage_margin)

    def test_send_voltage_regulation_command(self):
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.bay.send_voltage_regulation_command(self.device1, 1.0)
            self.assertEqual(mock_stdout.getvalue().strip(), "Sent voltage regulation command to Device1")

    def test_visualize_voltage_history(self):
        with unittest.mock.patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.bay.visualize_voltage_history()
            self.assertTrue("Bay1 Voltage History" in mock_stdout.getvalue())
