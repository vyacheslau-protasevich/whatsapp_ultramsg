import requests
import base64
import re

from read import read_sheets


def extract_tags(s):
    # Regular expression pattern to match tags in the format {{tag}}
    pattern = r"{{(.*?)}}"
    # Find all matches of the pattern in the string
    tags = re.findall(pattern, s)
    return tags


def file_to_base64(file_path):
    # Read file in binary mode
    with open(file_path, "rb") as file:
        file_content = file.read()

    # Encode file content
    encoded_content = base64.b64encode(file_content)

    # Convert bytes to string
    encoded_string = encoded_content.decode('utf-8')

    return encoded_string


def send_whatsapp_message(format: str, config: dict, update_progress_callback=None, write_log_callback=None,
                          completion_callback=None, error_callback=None):
    ultramsg_instance_id = config["ultramsg_instance_id"]
    ultramsg_token = config["ultramsg_token"]
    service_account_file = config["service_account_file"]
    spreadsheet_id = config["spreadsheet_id"]
    sheet_number = config["sheet_number"]
    message_delay = config["message_delay"]

    a = read_sheets(service_account_file=service_account_file, spreadsheet_id=spreadsheet_id, sheet_number=sheet_number,
                    error_callback=error_callback)
    if a:

        total_messages = len([i for i in a if i["Select"] == "TRUE"])
        if total_messages < 1:
            error_callback(f"No selected messages")
        else:
            if int(message_delay) > 1:
                settings_url = f"https://api.ultramsg.com/{ultramsg_instance_id}/instance/settings?token={ultramsg_token}"
                data = {
                    "sendDelay": message_delay
                }
                resp = requests.post(settings_url, data=data).json()

            current_message = 1
            sent_count = 0

            base_url = f"https://api.ultramsg.com/{ultramsg_instance_id}/messages/chat?token={ultramsg_token}"

            tags = extract_tags(format)

            for i in a:
                if i["Select"] == "TRUE":
                    message_text = ""
                    for j in tags:
                        if j == "Name":
                            message_text += i["Name"]
                        elif j == "Text":
                            message_text += i["text"]
                        else:
                            message_text += j

                    data = {
                        "priority": 1,
                        "referenceId": ""
                    }

                    if i["Phone number"]:
                        data["to"] = i["Phone number"]
                    else:
                        if write_log_callback:
                            write_log_callback(f"Message was not sent, because number is not specified")
                            continue

                    if message_text:
                        data["body"] = message_text
                    else:
                        if write_log_callback:
                            write_log_callback(
                                f"Message was not sent to: {i['Phone number']}, because message text is missing")
                            continue

                    response = requests.post(base_url, data=data).json()
                    # print(response)

                    if update_progress_callback:
                        update_progress_callback(current_message, total_messages)
                        current_message += 1
                    if response and ("sent" in response) and (response["sent"] == "true"):
                        sent_count += 1
                        if write_log_callback:
                            write_log_callback(f"Message sent to: {i['Phone number']}")
                    else:
                        if write_log_callback:
                            write_log_callback(f"Message was not sent to: {i['Phone number']}")

            if completion_callback:
                completion_callback(sent_count, total_messages - sent_count)


def send_whatsapp_photo(format: str, config: dict, update_progress_callback=None, write_log_callback=None,
                        completion_callback=None, error_callback=None):
    ultramsg_instance_id = config["ultramsg_instance_id"]
    ultramsg_token = config["ultramsg_token"]
    service_account_file = config["service_account_file"]
    spreadsheet_id = config["spreadsheet_id"]
    sheet_number = config["sheet_number"]
    message_delay = config["message_delay"]

    a = read_sheets(service_account_file=service_account_file, spreadsheet_id=spreadsheet_id, sheet_number=sheet_number,
                    error_callback=error_callback)

    if a:
        total_messages = len([i for i in a if i["Select"] == "TRUE"])
        if total_messages < 1:
            error_callback(f"No selected messages")
        else:
            if int(message_delay) > 1:
                settings_url = f"https://api.ultramsg.com/{ultramsg_instance_id}/instance/settings?token={ultramsg_token}"
                data = {
                    "sendDelay": message_delay
                }
                resp = requests.post(settings_url, data=data).json()
            current_message = 1
            sent_count = 0

            base_url = f"https://api.ultramsg.com/{ultramsg_instance_id}/messages/image?token={ultramsg_token}"

            tags = extract_tags(format)

            for i in a:
                if i["Select"] == "TRUE":
                    caption = ""
                    for j in tags:
                        if j == "Photo (default)":
                            continue
                        if j == "Name":
                            caption += i["Name"]
                        elif j == "Photo caption":
                            caption += i["photo caption"]
                        else:
                            caption += j

                    data = {
                        "priority": 1,
                        "referenceId": ""
                    }

                    if i["Phone number"]:
                        data["to"] = i["Phone number"]
                    else:
                        if write_log_callback:
                            write_log_callback(f"Message was not sent, because number is not specified")
                            continue

                    if caption:
                        data["caption"] = caption

                    if i["photo url"]:
                        data["image"] = i["photo url"]
                    else:
                        if write_log_callback:
                            write_log_callback(
                                f"Message was not sent to: {i['Phone number']}, because photo url is missing")
                            continue

                    print(data)

                    response = requests.post(base_url, data=data).json()
                    # print(response)

                    if update_progress_callback:
                        update_progress_callback(current_message, total_messages)
                        current_message += 1
                    if response and ("sent" in response) and (response["sent"] == "true"):
                        sent_count += 1
                        if write_log_callback:
                            write_log_callback(f"Message sent to: {i['Phone number']}")
                    else:
                        if write_log_callback:
                            write_log_callback(f"Message was not sent to: {i['Phone number']}")

            if completion_callback:
                completion_callback(sent_count, total_messages - sent_count)


def send_whatsapp_video(format: str, config: dict, update_progress_callback=None, write_log_callback=None,
                        completion_callback=None, error_callback=None):
    ultramsg_instance_id = config["ultramsg_instance_id"]
    ultramsg_token = config["ultramsg_token"]
    service_account_file = config["service_account_file"]
    spreadsheet_id = config["spreadsheet_id"]
    sheet_number = config["sheet_number"]
    message_delay = config["message_delay"]

    a = read_sheets(service_account_file=service_account_file, spreadsheet_id=spreadsheet_id, sheet_number=sheet_number,
                    error_callback=error_callback)

    if a:
        total_messages = len([i for i in a if i["Select"] == "TRUE"])
        if total_messages < 1:
            error_callback(f"No selected messages")
        else:
            if int(message_delay) > 1:
                settings_url = f"https://api.ultramsg.com/{ultramsg_instance_id}/instance/settings?token={ultramsg_token}"
                data = {
                    "sendDelay": message_delay
                }
                resp = requests.post(settings_url, data=data).json()
            current_message = 1
            sent_count = 0

            base_url = f"https://api.ultramsg.com/{ultramsg_instance_id}/messages/video?token={ultramsg_token}"

            tags = extract_tags(format)

            for i in a:
                if i["Select"] == "TRUE":
                    caption = ""
                    for j in tags:
                        if j == "Video (default)":
                            continue
                        if j == "Name":
                            caption += i["Name"]
                        elif j == "Video caption":
                            caption += i["video caption"]
                        else:
                            caption += j

                    data = {
                        "priority": 1,
                        "referenceId": ""
                    }

                    if i["Phone number"]:
                        data["to"] = i["Phone number"]
                    else:
                        if write_log_callback:
                            write_log_callback(f"Message was not sent, because number is not specified")
                            continue

                    if caption:
                        data["caption"] = caption

                    if i["video url"]:
                        data["video"] = i["video url"]
                    else:
                        if write_log_callback:
                            write_log_callback(
                                f"Message was not sent to: {i['Phone number']}, because video url is missing")
                            continue

                    print(data)

                    response = requests.post(base_url, data=data).json()
                    # print(response)

                    if update_progress_callback:
                        update_progress_callback(current_message, total_messages)
                        current_message += 1
                    if response and ("sent" in response) and (response["sent"] == "true"):
                        sent_count += 1
                        if write_log_callback:
                            write_log_callback(f"Message sent to: {i['Phone number']}")
                    else:
                        if write_log_callback:
                            write_log_callback(f"Message was not sent to: {i['Phone number']}")

            if completion_callback:
                completion_callback(sent_count, total_messages - sent_count)
