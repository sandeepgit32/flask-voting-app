import os, csv
import redis
import pickle
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, send_file

# Load environment variables from .env file
load_dotenv()

# Connect to Redis
redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CANDIDATE_FILE = os.path.join(BASE_DIR, 'candidate_list.txt')
VOTER_FILE = os.path.join(BASE_DIR, 'voter_list.txt')
RESULTS_FILE = os.path.join(BASE_DIR, 'voting_results.csv')
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
admin_passcode = os.getenv('ADMIN_PASSCODE')


class Candidate:
    def __init__(self, name, party):
        self.name = name
        self.party = party

    def __str__(self):
        return f'{self.name} ({self.party})'


class Voter:
    def __init__(self, id):
        self.id = id
        self.has_voted = False

    def __str__(self):
        return f'{self.id}'


# Initialize candidates from file
def initialize_candidates():
    candidates = []
    votes = {}
    with open(CANDIDATE_FILE) as f:
        for line in f:
            name, party = line.strip().split(",")
            candidate = Candidate(name, party)
            candidates.append(candidate)
            votes[candidate.name] = 0
    redis_client.set("candidates", pickle.dumps(candidates))
    redis_client.set("votes", pickle.dumps(votes))
    redis_client.set("voting_open", "False")


# Initialize voters from file
def initialize_voters():
    voters = []
    with open(VOTER_FILE) as f:
        voters.extend([Voter(line.strip()) for line in f])
    redis_client.set("voters", pickle.dumps(voters))
    redis_client.set("total_votes_cast", 0)


def set_redis_data(key, value):
    if (key == "candidates") or (key == "voters") or (key == "votes"):
        redis_client.set(key, pickle.dumps(value))
    else:
        redis_client.set(key, value)


def get_redis_data(key):
    try:
        value = redis_client.get(key)
        if value is None:
            return None
        if (key == "candidates") or (key == "voters") or (key == "votes"):
            return pickle.loads(value)
        elif key == "total_votes_cast":
            return int(value)
        return value
    except redis.RedisError as e:
        print(f"Redis error: {e}")
        return None


# Check if the voter is valid
def is_valid_voter(voter_id):
    voters = get_redis_data("voters")
    return any(voter.id == voter_id for voter in voters)


@app.route('/', methods=['GET', 'POST'])
def home():
    voting_open = get_redis_data("voting_open")
    if voting_open == "True":
        return redirect(url_for('vote'))
    
    if request.method == 'POST':
        passcode = request.form['passcode']
        if passcode == admin_passcode:
            initialize_candidates()
            initialize_voters()
            voting_open = "True"  # Admin opens the voting
            total_votes_cast = 0
            set_redis_data("voting_open", voting_open)
            set_redis_data("total_votes_cast", total_votes_cast)
            return redirect(url_for('vote'))
        else:
            flash("Invalid passcode.", 'error')
    return render_template('index.html')


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    voting_open = get_redis_data("voting_open")
    total_votes_cast = get_redis_data("total_votes_cast")
    voters = get_redis_data("voters")
    candidates = get_redis_data("candidates")
    if voting_open == "False":
        flash("Voting is not open yet. Please wait for the admin to open voting.", 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        voter_id = request.form['voter_id']
        if not is_valid_voter(voter_id):
            return redirect(url_for('thank_you', message="You are not a registered voter!"))

        voter = next(voter for voter in voters if voter.id == voter_id)

        if voter.has_voted:
            # Display thank you style message if voter already voted
            return redirect(url_for('thank_you', message="You have already voted!"))

        selected_candidate = request.form.get('candidate')
        if selected_candidate:
            votes = get_redis_data("votes")
            votes[selected_candidate] += 1
            voter.has_voted = True
            total_votes_cast += 1  # Increment vote counter
            set_redis_data("votes", votes)
            set_redis_data("voters", voters)
            set_redis_data("total_votes_cast", total_votes_cast)
            return redirect(url_for('thank_you', message="Thank you for voting!"))
        else:
            flash("Please select a candidate.", 'error')

    return render_template(
        'vote.html', 
        candidates=candidates, 
        total_votes_cast=total_votes_cast, 
        total_voters=len(voters)
    )


@app.route('/thank_you')
def thank_you():
    message = request.args.get('message', "Thank you for voting!")
    return render_template('thank_you.html', message=message)


@app.route('/results', methods=['GET', 'POST'])
def results():
    voting_open = get_redis_data("voting_open")
    if voting_open == "True":
        return redirect(url_for('vote'))
    if request.method == 'POST':
        passcode = request.form['passcode']
        if passcode == admin_passcode:
            votes = get_redis_data("votes")
            total_votes = sum(votes.values())
            return render_template('results.html', votes=votes, total_votes=total_votes)
        else:
            flash("Invalid passcode.", 'error')
            return redirect(url_for('results'))
    return render_template('enter_passcode.html')


@app.route('/reset', methods=['POST'])
def reset_ballot():
    passcode = request.form.get('passcode')
    if passcode == admin_passcode:
        initialize_candidates()
        initialize_voters()
        total_votes_cast = 0
        set_redis_data("total_votes_cast", total_votes_cast)
        flash("The ballot has been reset.", 'success')
        return redirect(url_for('vote'))
    else:
        flash("Invalid passcode.", 'error')
        return redirect(url_for('vote'))


@app.route('/close', methods=['POST'])
def close_voting():
    passcode = request.form.get('passcode')
    if passcode == admin_passcode:
        voting_open = "False"
        set_redis_data("voting_open", voting_open)
        return redirect(url_for('results'))
    else:
        flash("Invalid passcode.", 'error')
        return redirect(url_for('vote'))
    

@app.route('/save_results', methods=['POST'])
def save_results():
    with open(RESULTS_FILE, 'w', newline='') as csvfile:
        fieldnames = ['Candidate', 'Party', 'Votes']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        candidates = get_redis_data("candidates")
        votes = get_redis_data("votes")
        for candidate in candidates:
            writer.writerow({
                'Candidate': candidate.name, 
                'Party': candidate.party, 
                'Votes': votes.get(candidate.name, 0)
            })
    return send_file(RESULTS_FILE, as_attachment=True)


if __name__ == '__main__':
    initialize_candidates()
    initialize_voters()
    app.run(debug=True)
