// JS for validating the voter form before submission
document.addEventListener('DOMContentLoaded', function() {
    const voteForm = document.querySelector('#voteForm');

    if (voteForm) {
        voteForm.addEventListener('submit', function(event) {
            const voterId = document.querySelector('#voter_id').value;
            const candidate = document.querySelector('input[name="candidate"]:checked');

            if (!voterId) {
                alert('Please enter your Voter ID.');
                event.preventDefault();  // Stop form from submitting
            } else if (!candidate) {
                alert('Please select a candidate.');
                event.preventDefault();  // Stop form from submitting
            }
        });
    }
});

