import json
import os

def create_helics_config(core_name, core_type, name, offset, period, time_delta, logfile, log_level, uninterruptible, publications, subscriptions):
    config = {
        "coreInit": "--federates=1",
        "coreName": core_name,
        "coreType": core_type,
        "name": name,
        "offset": offset,
        "period": period,
        "timeDelta": time_delta,
        "logfile": logfile,
        "log_level": log_level,
        "uninterruptible": uninterruptible,
        "publications": publications,
        "subscriptions": subscriptions
    }
    return config

def save_config_to_file(config, filename):
    with open(filename, 'w') as f:
        json.dump(config, f, indent=4)

def get_publications_from_file(filepath):
    """Extract publications from a JSON config file."""
    with open(filepath, 'r') as f:
        config = json.load(f)
    return config.get("publications", [])

def list_json_files(directory):
    """Recursively list all JSON files in the specified directory and its subdirectories."""
    json_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files

def map_publication_to_subscription(publication):
    """Map a publication with arbitrary keys to a subscription with required fields."""
    print("\nAvailable fields in the publication:")
    for key, value in publication.items():
        print(f"{key}: {value}")

    name = input("Enter the field to use as the subscription 'name': ")
    key = input("Enter the field to use as the subscription 'key': ")
    type_ = input("Enter the field to use as the subscription 'type': ")

    subscription = {
        "name": publication.get(name, ""),
        "key": publication.get(key, ""),
        "type": publication.get(type_, ""),
        "required": True  # Default to required, but you can modify this if needed
    }
    return subscription

def select_subscriptions_from_files(directory):
    """Allow the user to select publications from JSON files in the directory and add them as subscriptions."""
    subscriptions = []
    json_files = list_json_files(directory)

    if not json_files:
        print("No JSON files found in the 'src' directory or its subdirectories.")
        return subscriptions

    print("\nAvailable JSON files in 'src' directory and subdirectories:")
    for i, file in enumerate(json_files):
        print(f"{i + 1}. {file}")

    while True:
        try:
            file_choice = input("\nEnter the number of the file to load publications from (or 'q' to quit): ")
            if file_choice.lower() == 'q':
                break

            file_index = int(file_choice) - 1
            if file_index < 0 or file_index >= len(json_files):
                print("Invalid choice. Please try again.")
                continue

            selected_file = json_files[file_index]
            file_publications = get_publications_from_file(selected_file)

            if not file_publications:
                print(f"No publications found in '{selected_file}'.")
                continue

            print(f"\nPublications in '{selected_file}' (will be added as subscriptions):")
            for i, pub in enumerate(file_publications):
                print(f"{i + 1}. {pub}")

            pub_choice = input("\nEnter the number of the publication to add as a subscription (or 'q' to quit): ")
            if pub_choice.lower() == 'q':
                continue

            pub_index = int(pub_choice) - 1
            if pub_index < 0 or pub_index >= len(file_publications):
                print("Invalid choice. Please try again.")
                continue

            selected_pub = file_publications[pub_index]
            # Map the publication to a subscription
            subscription = map_publication_to_subscription(selected_pub)
            subscriptions.append(subscription)
            print(f"Added subscription: {subscription['name']}")

        except ValueError:
            print("Invalid input. Please enter a number.")

    return subscriptions

def get_user_input():
    print("HELICS Configuration File Generator")
    print("Please enter the following details:")

    core_name = input("Core Name (e.g., 'Voltage Current Sensor Federate'): ")
    core_type = input("Core Type (e.g., 'zmq'): ")
    name = input("Federate Name (e.g., 'VoltageCurrentSensorSim'): ")
    offset = int(input("Offset (e.g., 0): "))
    period = int(input("Period (e.g., 60): "))
    time_delta = int(input("Time Delta (e.g., 1): "))
    logfile = input("Logfile Name (e.g., 'output.log'): ")
    log_level = input("Log Level (e.g., 'warning'): ")
    uninterruptible = input("Uninterruptible (True/False): ").lower() == "true"

    # Allow the user to add subscriptions from publications in other JSON files
    src_directory = "src"
    if os.path.exists(src_directory):
        print("\nYou can add subscriptions from publications in JSON files in the 'src' directory and its subdirectories.")
        subscriptions = select_subscriptions_from_files(src_directory)
    else:
        print("\n'src' directory not found. Skipping subscription import.")
        subscriptions = []

    # Allow manual addition of subscriptions
    print("\nAdd additional subscriptions manually (leave name blank to finish):")
    while True:
        sub_name = input("Subscription Name: ")
        if not sub_name:
            break
        sub_key = input("Subscription Key: ")
        sub_type = input("Subscription Type (e.g., 'complex'): ")
        sub_required = input("Required (True/False): ").lower() == "true"
        subscriptions.append({
            "name": sub_name,
            "key": sub_key,
            "type": sub_type,
            "required": sub_required
        })

    # Add publications
    publications = []
    print("\nAdd Publications (leave name blank to finish):")
    while True:
        pub_name = input("Publication Name: ")
        if not pub_name:
            break
        pub_key = input("Publication Key: ")
        pub_type = input("Publication Type (e.g., 'complex'): ")
        publications.append({
            "name": pub_name,
            "key": pub_key,
            "type": pub_type
        })

    return core_name, core_type, name, offset, period, time_delta, logfile, log_level, uninterruptible, publications, subscriptions

if __name__ == "__main__":
    # Get user input
    core_name, core_type, name, offset, period, time_delta, logfile, log_level, uninterruptible, publications, subscriptions = get_user_input()

    # Create the configuration
    config = create_helics_config(core_name, core_type, name, offset, period, time_delta, logfile, log_level, uninterruptible, publications, subscriptions)

    # Save the configuration to a file
    output_filename = input("\nEnter the output filename (e.g., 'voltage_current_sensors_config.json'): ")
    save_config_to_file(config, output_filename)

    print(f"\nHELICS configuration file '{output_filename}' created successfully.")