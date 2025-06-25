# zhin

The "Navajo Nation Governance Tracker" is a tool designed to provide a comprehensive, up-to-date, and easily accessible platform for tracking the legislative and judicial activities of the Navajo Nation government.

## Prerequisites

This project uses [pdm](https://pdm.fming.dev) for dependency management. Please ensure you have it installed.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd zhin
    ```

2.  **Create the virtual environment:**
    ```bash
    pdm venv create
    ```

3.  **Install dependencies:**
    ```bash
    pdm install
    ```

## Running the Application

To run the main application, which executes all the scrapers, use the following command:

```bash
pdm run zhin
```

## Running Tests

To run the test suite, you first need to install the test dependencies:

```bash
pdm install -G test
```

Then, you can run the tests using `pytest`:

```bash
pdm run pytest
