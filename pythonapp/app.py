from flask import Flask, request, render_template_string

app = Flask(__name__)

tickets = []  # In-memory ticket store

TICKET_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Support Ticket</title>
</head>
<body>
    <h2>Submit a Support Ticket</h2>
    <form method="POST">
        <label>Name:</label><br>
        <input type="text" name="name" required><br><br>

        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>

        <label>Issue:</label><br>
        <textarea name="issue" rows="4" cols="40" required></textarea><br><br>

        <input type="submit" value="Submit Ticket">
    </form>

    {% if submitted %}
        <h3>✅ Ticket Submitted!</h3>
        <p><strong>Ticket Number:</strong> #{{ ticket_no }}</p>
        <p><strong>Name:</strong> {{ name }}</p>
        <p><strong>Email:</strong> {{ email }}</p>
        <p><strong>Issue:</strong> {{ issue }}</p>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def ticket():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        issue = request.form['issue']

        # Generate a ticket number
        ticket_no = len(tickets) + 1
        ticket_data = {
            'ticket_no': ticket_no,
            'name': name,
            'email': email,
            'issue': issue
        }
        tickets.append(ticket_data)

        return render_template_string(TICKET_FORM, submitted=True, ticket_no=ticket_no, name=name, email=email, issue=issue)

    return render_template_string(TICKET_FORM, submitted=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
