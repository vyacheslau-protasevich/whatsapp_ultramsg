import configparser
import os


def get_persistent_settings_path():
    home_dir = os.path.expanduser("~")
    app_dir = os.path.join(home_dir, ".myapp")  # Application-specific directory

    if not os.path.exists(app_dir):
        os.makedirs(app_dir)  # Create the directory if it does not exist

    settings_path = os.path.join(app_dir, "app_settings.ini")
    return settings_path


def save_settings_to_file(settings):
    config = configparser.ConfigParser()
    config['Settings'] = settings
    settings_path = get_persistent_settings_path()

    with open(settings_path, 'w') as configfile:
        config.write(configfile)


def load_settings_from_file():
    config = configparser.ConfigParser()
    settings_path = get_persistent_settings_path()
    config.read(settings_path)

    if 'Settings' in config:
        for key in config['Settings']:
            os.environ[key.upper()] = config['Settings'][key]
