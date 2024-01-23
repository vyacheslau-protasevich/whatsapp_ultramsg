# Message Constructor for WhatsApp

## Description

This application provides a user-friendly interface to construct and send custom WhatsApp messages. It allows users to create messages with various components, including text, photos, and captions. The application is designed to interact with Google Sheets for data retrieval and uses the Ultramsg API for message delivery.

## Features

- **Message Construction**: Build custom WhatsApp messages with text, photos, and captions.
- **Google Sheets Integration**: Retrieve data from a specified Google Sheet for message personalization.
- **Ultramsg API Integration**: Send messages directly to WhatsApp using the Ultramsg API.
- **Customizable Settings**: Configure API tokens, Google Sheet details, and other settings.
- **Progress Tracking**: Monitor the progress of message sending with a progress bar and logs.

## Installation

1. **Clone the Repository**: Clone this repository to your local machine.
   ```
   git clone https://github.com/your-username/your-repository.git
   ```

2. **Install Dependencies**: Install the required Python libraries.
   ```
   pip install -r requirements.txt
   ```

3. **Run the Application**: Launch the application by running the main script.
   ```
   python main.py
   ```

## Usage

1. **Configure Settings**: Open the settings window to enter your Ultramsg API token, Google Sheet ID, and other relevant information.

2. **Construct Messages**: Use the message constructor interface to create custom messages. You can add text, photos, and captions as needed.

3. **Send Messages**: Once your message is ready, click the "Send" button to deliver it to the specified recipients via WhatsApp.

4. **Monitor Progress**: Watch the progress bar and logs for updates on message sending status.

## Creating a Standalone Executable

To create a standalone executable of the application using PyInstaller:

1. **Install PyInstaller**:
   ```
   pip install pyinstaller
   ```

2. **Create the Executable**:
   Navigate to the project directory and run the following command:
   ```
   pyinstaller --onefile --noconsole main.py
   ```
   Replace `main.py` with the name of your main script file.

3. **Find the Executable**:
   The executable will be created in the `dist` folder within your project directory.

## Configuration

Before using the application, ensure you have the following:

- **Ultramsg API Token**: A valid token from Ultramsg for WhatsApp messaging.
- **Google Sheets API Credentials**: A service account key file for accessing Google Sheets data. (Create application in google cloud console if necessary)
- **Google Sheet ID**: The ID of the Google Sheet containing recipient data.

---
## License

This project is licensed under the [MIT License](LICENSE).