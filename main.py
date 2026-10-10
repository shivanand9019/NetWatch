import socket
import time

def check_service(host,port):
    
    try:
        start_time = time.perf_counter()
        with socket.create_connection((host,port), timeout=5):
            end_time = time.perf_counter()
            
            latency = (end_time - start_time) * 1000  # convert to milliseconds
        return {
                "host":host,
                "port":port,
                "status":"REACHABLE",
                "latency_ms":latency
           }
           
    except OSError as error:
        
        return {
            "host":host,
            "port":port,
            "status":"UNREACHABLE",
            "error":str(error)
        }

# for testing multiple services.
services  = [("localhost", 8080),("google.com", 80), ("example.com", 443),("invalidhost", 1234)]

for host, port in services:
    result = check_service(host, port)
    print(result)