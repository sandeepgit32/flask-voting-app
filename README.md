# Voting Application

This is a simple voting application built with Flask. It allows users to vote for candidates, view results, and manage the voting process.

## Features

- **Admin Authentication**: Admin can open and close the voting process using a passcode.
- **Voting**: Users can vote for their preferred candidates.
- **Results**: Display the total number of votes and the percentage of votes each candidate received.
- **Save Results**: Admin can save the voting results to a CSV file.

## Project Structure

. ├── pycache/ ├── .env ├── app.py ├── candidate_list.txt ├── requirements.txt ├── static/ │ ├── results.css │ ├── scripts.js │ └── styles.css ├── templates/ │ ├── enter_passcode.html │ ├── index.html │ ├── results.html │ ├── thank_you.html │ └── vote.html ├── venv/ │ ├── bin/ │ ├── include/ │ ├── lib/ │ ├── lib64 │ ├── pyvenv.cfg │ └── share/ ├── voter_list.txt └── voting_results.csv


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

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Create a `.env` file** in the root directory and add the following:
    ```
    SECRET_KEY=your_secret_key
    ADMIN_PASSCODE=your_admin_passcode
    ```

5. **Prepare candidate and voter lists**:
    - `candidate_list.txt`: List of candidates in the format `name,party`.
    - `voter_list.txt`: List of voter IDs.

## Running the Application

1. **Run the application**:
    ```sh
    python app.py
    ```

2. **Open the application**:
    Open your web browser and go to `http://127.0.0.1:5000`.

## Usage

- **Admin Login**: Enter the admin passcode to open the voting process.
- **Voting**: Users can vote by entering their voter ID and selecting a candidate.
- **Results**: View the results after closing the voting process.
- **Save Results**: Admin can save the results to a CSV file.

## License

This project is licensed under the MIT License.