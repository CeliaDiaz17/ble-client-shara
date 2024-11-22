# Welcome to the Click'n-Learn Main Repository!

This repository contains the integrated modules for the **SHEVA robotic platform**, enabling a comprehensive **Student Response System**. The system combines quiz generation, data evaluation, and interactive functionality to enhance the learning experience.

---

## Modules Overview

### 1. **Data Evaluation**
- A Python script that processes and evaluates data received from clickers.

### 2. **Quiz Generation**
- Automatically generates quizzes from user-provided PDFs using the **OpenAI API**.
- The system extracts content and transforms it into an interactive quiz format.

### 3. **Speaker**
- Uses **Google Cloud Text-to-Speech (TTS)** tools to provide the robot with a humanized voice for seamless interaction.

### 4. **Utils**
- An auxiliary module containing shared methods and utility functions used across the project.

### 5. **BLE Functionality**
- Handles **Bluetooth Low Energy (BLE)** connections to receive data from clicker devices.
- The clicker implementation can be found [here](https://github.com/CeliaDiaz17/clicker-M5Stick).

### 6. **Main Module**
- Integrates all other modules into a cohesive system for deployment on the SHEVA platform.

---

## Getting Started

Follow the steps below to set up and run the system on your PC or robotic platform.

### Prerequisites

Ensure you have the following installed:
- **Python 3.8 or newer**
- **Google Cloud TTS and Translate Services** (configured for your environment)
- **OpenAI API services** (with API keys set up)

### Installation Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/CeliaDiaz17/ble-client-shara

2. Open up a terminal and install the main dependencies:
    ```bash
    pip install google-cloud-text-to-speech openai bleak

3. Run the main scripts:
    ```bash
    python3 main.py










