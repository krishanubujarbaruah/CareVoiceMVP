# CareApp Setup Guide

Follow these instructions to set up and run the CareApp on your system, whether you're using Linux/Mac or Windows.

### Unpacking the Application

First, extract the contents of the `CareApp.zip` file into your chosen directory.

### Setting Up the Environment

#### Create a Virtual Environment

For Linux/Mac:
```bash
python3 -m venv venv
```

For Windows:
```bash
python -m venv venv
```

#### Activate the Virtual Environment

For Linux/Mac:
```bash
source venv/bin/activate
```

For Windows:
```cmd
.\venv\Scripts\activate
```

### Installing Required Packages

Once your environment is active, install all necessary dependencies with:

```bash
pip install -r requirements.txt
```

### Shutting Down the Virtual Environment

When you're done working with the application, you can deactivate the virtual environment with:

```bash
deactivate
```

## Initial Setup and Execution

Before you can start using the CareApp, ensure you've completed the following:

1. Verify that Python is installed on your system.
2. Open a terminal or command prompt and change to the directory containing the CareApp.
3. Install the application's dependencies by running `pip install -r requirements.txt`.
4. Locate the `app.py` file .
5. Begin the application by executing `python3 app.py` on Linux/Mac or `python app.py` on Windows.

## Application Demonstration

To see the CareApp in action, watch the demo video provided. 

*Note: Please ensure to follow these instructions as per your operating system for the successful execution of the CareApp.*