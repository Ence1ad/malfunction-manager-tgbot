# Malfunction-manager-tgbot
---

## Table of Contents  
  
1. [Introduction](#introduction)  
2. [Features](#key-features)  
3. [Usage](#usage)  
4. [Getting Started](#getting-started)
5. [License](#license)  
---

## Introduction

### Overview
Malfunction-manager-tgbot is a Python-based solution that enables users to register equipment, machinery, and device malfunctions through a Telegram bot. It streamlines the process of reporting issues, tracks their status, and facilitates their resolution. The project integrates with Django for backend management, using APScheduler for scheduling tasks and aiogram for Telegram bot interactions.

## Key Features  

- **Report Malfunctions:** Employees of a service organization can submit malfunction reports via the Telegram bot. They can choose the equipment's location, select the specific equipment, and provide a description of the malfunction. They can also attach photos or videos of the malfunction. The bot adds these reports to the database with a "created" status.

- **Manage Malfunctions:** Managers can access an admin panel in Django to view newly added malfunctions, assess their severity, and set their status. Depending on the status, malfunctions can be assigned for immediate repair or delayed until the availability of resources.

- **Assign for Repair:** Managers can assign malfunctions for repair by setting their status to "assigned." They can specify which employees will handle the repair, allocate necessary materials and spare parts, and provide comments or instructions. The Telegram bot notifies the assigned employees of the new tasks.

- **Spare Parts Management:** The system allows for the management of spare parts. Users can add spare parts to a virtual inventory, track their quantities, and record their installation on specific equipment.

- **Morning Reports:** The bot sends a daily report to the repair team and managers every morning at a specified time (configurable) containing a list of pending malfunctions.

- **Data Manipulation:** The Django admin panel offers a user-friendly way to manipulate data based on user permissions. Additionally, the system supports exporting malfunction reports in various formats, such as PDF, Word, and Excel.

## Usage

Access the Django admin panel to manage data, permissions, and configurations.
Interact with the Telegram bot to report malfunctions and receive notifications.
  
## Getting Started  
  
Follow these steps to set up and run the **malfunction-manager-tgbot** on your local machine:  
  
### Prerequisites  
  
- Python 3.8+  
- Pip (Python package manager)  
- Docker, Docker Compose (for containerization)  
  
### Installation  

1. Create a New Bot: To create a new bot, use the link [BotFather](https://t.me/BotFather) and send the command `/newbot`. Follow the instructions provided by BotFather.

2. Add the bot to your existing group and make it an administrator.

3. Clone the repository:

    ```bash
    git clone https://github.com/Ence1ad/malfunction-manager-tgbot.git  
    ```
   
4. Navigate to the project directory: 
  
    ```bash  
    cd malfunction-manager-tgbot
    ```  
   
5. Create an .env file based on the provided .env.example:

    ```bash  
    cp .env.example .env
    ```  
   
6. Open the .env file in a text editor and fill in the required configuration values. 
    ```env
    # Database Configuration
    POSTGRES_USER= # PostgreSQL database superuser.  
    POSTGRES_PASSWORD= # Password for the PostgreSQL database superuser.
    ...

    # Bot API Configuration  
    BOT_TOKEN= # Bot api token received from the bot-father  
    GROUP_ID= # Your group or supergroup chat id
    ```
7. Ensure you have both Docker and Docker Compose installed:

   - [Install Docker](https://docs.docker.com/get-docker/)
   - [Install Docker Compose](https://docs.docker.com/compose/install/)

8. Build the Docker image and start the services using Docker Compose:

    ```bash  
    docker compose -f docker-compose.yml up --build
    ```

9. To stop the Docker containers, simply run:

    ```bash
    docker compose -f docker-compose.yml down --remove-orphans
    ```

## License  
  
This project is licensed under the [MIT License](LICENSE).  
  
---  