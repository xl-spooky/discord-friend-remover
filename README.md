# Discord Self-Bot Friend Remover

**A simple yet powerful Discord self-bot script designed to manage your friend list by removing friends with ease, except for those you wish to keep.**

> **Disclaimer**: This script is for educational purposes only. Using self-bots is against Discord's Terms of Service and can lead to account bans. Use at your own risk.

## Table of Contents

- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## About the Project

The **Discord Self-Bot Friend Remover** is a tool designed for Discord users who want to manage their friend list automatically. This script allows you to:

- Fetch your current friends list.
- Remove friends based on specific criteria.
- Exclude certain friends from being removed.

This project is built with Python and utilizes the `discord.py-self` library, allowing for seamless integration with the Discord API.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.10+**: Make sure Python is installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).
- **pip**: Python package installer, which usually comes with Python. Verify by running `pip --version` in your terminal.

### Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/xl-spooky/discord-friend-remover.git
    ```

2. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

To use the Discord Self-Bot Friend Remover, follow these steps:

1. **Update the `TOKEN` in the script**:

   - Open `main.py` in a text editor.
   - Replace `"YOUR_ACC_TOKEN"` with your Discord user token. **Do not share your token with anyone**.

2. **Run the script**:

   ```bash
   python main.py
   ```

3. **Use the bot commands in Discord**:

   - **`!s remove`**: Removes all friends except those specified in the `DO_NOT_DELETE_IDS` list.

## Configuration

Customize the bot by editing the following settings in `main.py`:

- **`DO_NOT_DELETE_IDS`**: A list of friend user IDs that should not be removed. Update this list with the user IDs you want to exclude.

Example:
```python
DO_NOT_DELETE_IDS = [
    404264989147529217,  # Your friend ID
    123456789012345678,  # Another friend ID
]
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements

- [discord.py-self](https://github.com/dolfies/discord.py-self)
- [Requests: HTTP for Humans™](https://docs.python-requests.org/en/master/)
- [GitHub Emoji Cheat Sheet](https://github.com/ikatyang/emoji-cheat-sheet)
- [Choose an Open Source License](https://choosealicense.com)

