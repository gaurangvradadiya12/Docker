import subprocess
from flask import Flask, render_template_string

app = Flask(__name__)
tickets = []
services_to_check = ["nginx", "sshd", "cron"]  # Add your services here

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Multi-Service Monitoring</title>
</head>
<body>
    <h2>Multi-Service Monitoring Dashboard</h2>

    <table border="1" cellpadding="8">
        <tr>
            <th>Service</th>
            <th>Status</th>
            <th>Ticket</th>
        </tr>
        {% for service, status, ticket in service_statuses %}
        <tr>
            <td>{{ service }}</td>
            <td>{{ status }}</td>
            <td>
                {% if ticket %}
                    🚨 Ticket #{{ ticket['ticket_no'] }}: {{ ticket['issue'] }}
                {% else %}
                    ✅ No Issue
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def check_service_status(service):
    try:
        output = subprocess.check_output(
            f"ps -A | grep -w {service} | grep -v grep",
            shell=True
        )
        return 'active' if output else 'inactive'
    except subprocess.CalledProcessError:
        return 'inactive'

@app.route('/')
def monitor():
    service_statuses = []

    for service in services_to_check:
        status = check_service_status(service)
        ticket = None

        if status != 'active':
            ticket_no = len(tickets) + 1
            ticket = {
                'ticket_no': ticket_no,
                'issue': f"Service '{service}' is not running."
            }
            tickets.append(ticket)

        service_statuses.append((service, status, ticket))

    return render_template_string(HTML_TEMPLATE, service_statuses=service_statuses)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
