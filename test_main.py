from contextlib import redirect_stdout
from io import StringIO
import socket
from main import check_service,generate_summary

import unittest
import threading
class TestCheckService(unittest.TestCase):

    def test_reachable_service(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1", 0))
        server.listen(1)

        host, port = server.getsockname()

        def accept_connection():
            connection, address = server.accept()
            connection.close()
            server.close()

        thread = threading.Thread(target=accept_connection)
        thread.start()

        result = check_service(host, port)

        thread.join()

        self.assertEqual(result["status"], "REACHABLE")
        self.assertEqual(result["host"], host)
        self.assertEqual(result["port"], port)
        self.assertGreaterEqual(result["latency_ms"], 0)

    def test_unreachable_service(self):
        temp_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        temp_server.bind(("127.0.0.1",0))
        host,port = temp_server.getsockname()
        temp_server.close()


        result = check_service(host,port)

        self.assertEqual(result['status'],"UNREACHABLE")
        self.assertIn("error",result)
    
    def test_generate_summary(self):
        results = [
            {
                "host": "127.0.0.1",
                "port": 8000,
                "status": "REACHABLE",
                "latency_ms": 10.0
            },
            {
                "host": "127.0.0.1",
                "port": 8001,
                "status": "REACHABLE",
                "latency_ms": 20.0
            },
            {
                "host": "127.0.0.1",
                "port": 8002,
                "status": "UNREACHABLE",
                "error": "Connection refused"
            }
        ]

        output = StringIO()

        with redirect_stdout(output):
            generate_summary(results, 1.5)

        report = output.getvalue()

        self.assertIn("Total Services: 3", report)
        self.assertIn("Reachable Services: 2", report)
        self.assertIn("Unreachable services: 1", report)
        self.assertIn("15.0", report)

    
    def test_summary_when_all_services_unreachable(self):
        results = [
            {
                "host": "127.0.0.1",
                "port": 8001,
                "status": "UNREACHABLE",
                "error": "Connection refused"
            },
            {
                "host": "127.0.0.1",
                "port": 8002,
                "status": "UNREACHABLE",
                "error": "Connection refused"
            }
        ]

        output = StringIO()

        with redirect_stdout(output):
            generate_summary(results, 0.5)

        report = output.getvalue()

        self.assertIn("Reachable Services: 0", report)
        self.assertIn("Unreachable services: 2", report)
        self.assertIn("0", report)


if __name__ == "__main__":
    unittest.main()



