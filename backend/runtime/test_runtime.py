from backend.runtime.log_generator import generate_multiple_logs
from backend.runtime.runtime_engine import detect_bruteforce

def main():
    logs = generate_multiple_logs(30)

    alerts = detect_bruteforce(logs)

    print(f"Generated {len(alerts)} runtime alerts.")

if __name__ == "__main__":
    main()
