# Voting Application

This is a simple voting application built with Flask. It allows users to vote for candidates, view results, and manage the voting process.

## Features

- **Admin Authentication**: Admin can open and close the voting process using a passcode.
- **Voting**: Users can vote for their preferred candidates.
- **Results**: Display the total number of votes and the percentage of votes each candidate received.
- **Save Results**: Admin can save the voting results to a CSV file.

## Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Change directory**
    ```sh
    cd src
    ```

4. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

5. **Create a `.env` file** in the root directory and add the following:
    ```
    FLASK_APP='app.py'
    SECRET_KEY=your_secret_key
    ADMIN_PASSCODE=your_admin_passcode
    ```

6. **Prepare candidate and voter lists**:
    - `candidate_list.txt`: List of candidates in the format `name,party`.
    - `voter_list.txt`: List of voter IDs.

## Running the application in local

1. **Run the application**:
    ```sh
    python app.py
    ```

2. **Open the application**:
    Open your web browser and go to `http://127.0.0.1:5000`

## Running the application in docker

1. **Build the docker image**:
    ```sh
    docker build -t flask-voting-app .
    ```

2. **Run the docker container**:
    docker run --name voting-app -p 5000:5000 flask-voting-app

3. **Open the application**:
    Open your web browser and go to `http://127.0.0.1:5000`

## Usage

- **Admin Login**: Enter the admin passcode to open the voting process.
- **Voting**: Users can vote by entering their voter ID and selecting a candidate.
- **Results**: View the results after closing the voting process.
- **Save Results**: Admin can save the results to a CSV file.

## License

This project is licensed under the MIT License.