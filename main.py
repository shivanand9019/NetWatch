import socket
import time
from concurrent.futures import ThreadPoolExecutor
import logging



# loggin configuration
logging.basicConfig(
    filename="newtwork.log",
    level=logging.INFO,
    format="%(asctime)s  - %(levelname)s - %(message)s"
)

def check_service(host,port):
    
    try:
        start_time = time.perf_counter()
        with socket.create_connection((host,port), timeout=5):
            end_time = time.perf_counter()
            
            latency = (end_time - start_time) * 1000  # convert to milliseconds
        logging.info(logging.info(
                f"Service {host}:{port} is REACHABLE "
                f"(latency: {latency:.2f} ms)"
            )
        )
        return {
                "host":host,
                "port":port,
                "status":"REACHABLE",
                "latency_ms":round(latency,2)
           }

           
    except OSError as error:
        logging.warning(f"Service {host}:{port} is UNREACHABLE. Error :{error}")
        return {
            "host":host,
            "port":port,
            "status":"UNREACHABLE",
            "error":str(error)
        }


#  sequential running of the services
def sequential_run(services):
    start = time.perf_counter()
    results = []
    for host,port in services:
        result = check_service(host,port)
        results.append(result)
    
    elapsed_time = time.perf_counter() - start
    return results, elapsed_time


# concurrent running of the services
def concurrent_run(services):
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        
        for host, port in services:
            future = executor.submit(check_service,host,port)
            futures.append(future)
        results = []
        for f in futures:
            results.append(f.result())
        
    
    total_time = time.perf_counter() - start
    return results,total_time


# for testing multiple services.
services  = [("localhost", 8080),("google.com", 80), ("example.com", 443),("invalidhost", 1234)]



sequential_results, sequential_time = sequential_run(services)

concurrent_res, concurrent_time = concurrent_run(services)

print("Sequential Results: ")
for result in sequential_results:
    print(result)
print(f"Sequential Time:{sequential_time:.2f}s")


print("Concurrent Results:")
for r in concurrent_res:
    print(r)


print(f"Concurrent Time: {concurrent_time:.2f}s")


if concurrent_time > 0:
    speed_up = round(sequential_time/concurrent_time,2)
    print(f"Speed Up:{speed_up:.2f}x")



#   report generation function
def generate_summary (results,elapsed_time):
    
    no_of_reach = 0;
    no_of_unreach = 0
    count = 0
    latency = 0

    
    for result in results:
        if(result['status'] == 'REACHABLE'):
            latency+=result.get('latency_ms')
            no_of_reach+=1
        else:
            no_of_unreach+=1
    total_services= len(results)

    average_latency = 0;
    if no_of_reach>0:
        average_latency = round(latency/no_of_reach,2)
    else:
        average_latency = 0;
    
    print("Total Services:",total_services)
    print("Reachable Services:",no_of_reach)
    print("Unreachable services:",no_of_unreach)
    print("Average latency ",average_latency)
    print("Total Execution Time:",round(elapsed_time,2),"s")
print("For Concurrent Execution Summary:")
print("--------------------------------------")
generate_summary(concurrent_res,concurrent_time)
print("---------------------------------------")
print("For Sequential Execution Summary:")
print("--------------------------------------")
generate_summary(sequential_results,sequential_time)
print("---------------------------------------")