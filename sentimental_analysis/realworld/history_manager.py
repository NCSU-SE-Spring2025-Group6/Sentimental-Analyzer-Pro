import json
from django.contrib.auth import get_user
import os
from datetime import datetime

# Define the directory path
directory_path = os.path.join("sentimental_analysis", "media", "user_data")


def create_storage(username):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Create a JSON file with the username and save data along with timestamp
    file_path = os.path.join(directory_path, f"{username}.json")

    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file does not exist, create an empty dictionary
        with open(file_path, 'w') as json_file:
            json.dump({
                "Product_Analysis": {},
                "Image_Analysis": {},
                "News_Analysis": {},
                "Live_Speech": {},
                "Text_Analysis": {},
                "Batch_Analysis": {},
                "Doc_Analysis": {},
                "Audio_Analysis": {},
                "Facebook": {},
                "Twitter": {},
                "Reddit": {},
            }, json_file)


def store_text_analysis(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Text Analysis" section with the new data
    if "Text_Analysis" not in existing_data:
        existing_data["Text_Analysis"] = {}
    existing_data["Text_Analysis"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def store_image_analysis(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Image Analysis" section with the new data
    if "Image_Analysis" not in existing_data:
        existing_data["Image_Analysis"] = {}
    existing_data["Image_Analysis"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def store_news_analysis(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "News Analysis" section with the new data
    if "News_Analysis" not in existing_data:
        existing_data["News_Analysis"] = {}
    existing_data["News_Analysis"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def store_batch_analysis(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Batch Analysis" section with the new data
    if "Batch_Analysis" not in existing_data:
        existing_data["Batch_Analysis"] = {}
    existing_data["Batch_Analysis"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def store_document_analysis(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Document Analysis" section with the new data
    if "Doc_Analysis" not in existing_data:
        existing_data["Doc_Analysis"] = {}
    existing_data["Doc_Analysis"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def store_audio_analysis(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Audio Analysis" section with the new data
    if "Audio_Analysis" not in existing_data:
        existing_data["Audio_Analysis"] = {}
    existing_data["Audio_Analysis"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def store_live_analysis(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Live Analysis" section with the new data
    if "Live_Speech" not in existing_data:
        existing_data["Live_Speech"] = {}
    existing_data["Live_Speech"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def store_facebook_data(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Facebook" section with the new data
    if "Facebook" not in existing_data:
        existing_data["Facebook"] = {}
    existing_data["Facebook"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def store_twitter_data(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Twitter" section with the new data
    if "Twitter" not in existing_data:
        existing_data["Twitter"] = {}
    existing_data["Twitter"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def store_reddit_data(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Reddit" section with the new data
    if "Reddit" not in existing_data:
        existing_data["Reddit"] = {}
    existing_data["Reddit"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

def store_youtube_data(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    with open(file_path, 'r') as json_file:
        existing_data = json.load(json_file)

    # Update the "Reddit" section with the new data
    if "Youtube" not in existing_data:
        existing_data["Youtube"] = {}
    existing_data["Youtube"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


def store_product_analysis(request, data):
    # Get the username of the current user
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
    else:
        username = "Anonymous"
    print(f"Username: {username}")

    # Create storage for the user if it doesn't exist
    create_storage(username)

    # Create a JSON file with the username and save data along with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_path = os.path.join(directory_path, f"{username}.json")
    # Load the existing data from the JSON file
    try:
        with open(file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except json.JSONDecodeError:
        # If the JSON is invalid, create an empty dictionary
        existing_data = {
            "Product_Analysis": {},
            "Image_Analysis": {},
            "News_Analysis": {},
            "Live_Speech": {},
            "Text_Analysis": {},
            "Batch_Analysis": {},
            "Doc_Analysis": {},
            "Audio_Analysis": {},
            "Facebook": {},
            "Twitter": {},
            "Reddit": {},
            "Youtube": {},
        }

    # Update the "Product Analysis" section with the new data
    if "Product_Analysis" not in existing_data:
        existing_data["Product_Analysis"] = {}
    existing_data["Product_Analysis"][timestamp] = data

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)
