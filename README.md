# NetWatch

This is a simple Python project I made to check whether different services are reachable over the network and to compare how fast the checks run in different ways.

The idea is pretty basic: it tries to open a TCP connection to a host and port, checks if it works, measures the connection time, and then prints the results. I also added a concurrent version using threads so we can compare sequential and parallel execution.

## What this project does

- Checks if a host and port are accepting TCP connections
- Measures how long the connection takes
- Tests services one by one and also at the same time
- Logs successful and failed attempts
- Prints a short summary with reachable count, unreachable count, average latency, and total time
- Includes unit tests to check the main behaviors

## Tech used

- Python
- Socket programming
- `ThreadPoolExecutor` for concurrency
- `logging` for saving result messages
- `unittest` for testing

## How to run it

Open the project folder and run:

```bash
python main.py
```

To run the tests:

```bash
python -m unittest test_main.py -v
```

## How it works

1. The program loops through a list of services like `host` and `port`.
2. It tries to connect to each one using a TCP socket.
3. If the connection succeeds, it records the time it took.
4. It runs the checks in normal sequential order and also in parallel.
5. Then it prints the results and compares the total time.

## Notes

This project is useful for learning network checking and multi-threading, but it is not a full monitoring system.

A few important things to keep in mind:

- Just because a port is open does not mean the app behind it is working correctly.
- The latency here is only for TCP connection setup, not for full HTTP request time.
- Results can change depending on network quality, DNS, and timeout settings.

## Possible improvements

- Let the user choose services and timeouts from a config file
- Add periodic checks over time
- Make the output more structured and easier to read
- Add more tests for edge cases and error handling
