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
    REDIS_HOST='redis'
    REDIS_PORT='6379'
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

## Running the application in Docker

1. **Run the docker compose file**:
    docker compose up --build

3. **Open the application**:
    Open your web browser and go to `http://127.0.0.1:5000`

## Running the application in Minikube

1. **Start Minikube cluster**
    ```sh
    minikube start
    ```

2. **Load the docker image into minikube**
    ```sh
    docker build -t flask-voting-app-web:<tag> .
    minikube image load flask-voting-app-web:<tag>
    ```

3. **Run the Kubernetes manifests**
    ```sh
    kubectl apply -f k8s/dev/namespace.yaml
    kubectl apply -f k8s/dev/configmap.yaml
    kubectl apply -f k8s/dev/secret.yaml
    kubectl apply -f k8s/dev/persistent-volume.yaml
    kubectl apply -f k8s/dev/deployment.yaml
    kubectl apply -f k8s/dev/service.yaml
    ```
4. **Get the Minikube ip**
    ```sh
    minikube ip
    ```

5. **Open the application**:
    Open your web browser and go to `http://<minikube-ip>:30000`

6. **Monitor Minikube cluster dashboard**
    ```sh
    minikube dashboard
    ```

7. **To delete all resources run**
    ```sh
    kubectl delete namespace dev
    ```

## Running the application using Helm

1. **Start Minikube cluster**
    ```sh
    minikube start
    ```

2. Navigate to the project root
   
3. Install the helm chart to create a release `voting-app` in `dev` namespace: 
    ```sh
    helm install voting-app helm-charts \
    --values helm-charts/values-dev.yaml -n dev \
    --create-namespace
    ```
    It will create the namespace automatically if not exist.

4. **Get the minikube ip**
    ```sh
    minikube ip
    ```

5. **Open the application**:
    Open your web browser and go to `http://<minikube-ip>:30000`
   
6. To upgrade the release, run: 
    ```sh
    helm upgrade voting-app helm-charts \
    --values helm-charts/values-dev.yaml -n dev
    ```

7. To list the installed releases in namespace `dev`, run:
    ```sh
    helm ls -n dev
    ```
    To list the installed releases in all namespaces, run:
    ```sh
    helm ls -A
    ```

8. To list all the revisions of a release, run:
    ```sh
    helm history voting-app -n dev
    ```

9. If you want to rollback to a previous revision (say `1`), use:
    ```sh
    helm rollback voting-app 1 -n dev
    ```

10. To uninstall the release, run:
    ```sh
    helm uninstall voting-app -n dev
    ```

## License

This project is licensed under the MIT License.