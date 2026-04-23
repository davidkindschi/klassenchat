import os
import uuid
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

messages = []


@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    prefill_content = ''

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'set_username':
            username = request.form.get('username', '').strip()
            if username:
                session['username'] = username
            return redirect(url_for('index'))

        elif action == 'send_message':
            raw = request.form.get('content', '')
            content = raw.strip()
            if not content:
                error = 'Nachricht darf nicht leer sein.'
                prefill_content = raw
            elif len(content) > 500:
                error = f'Nachricht zu lang ({len(content)}/500 Zeichen).'
                prefill_content = raw
            else:
                sender = session.get('username', 'Anonym')
                messages.append({
                    'id': str(uuid.uuid4()),
                    'sender': sender,
                    'content': content,
                    'sent_at': datetime.now(timezone.utc).strftime('%H:%M:%S'),
                    'is_anonym': sender == 'Anonym',
                })
                return redirect(url_for('index'))

        elif action == 'delete_message':
            message_id = request.form.get('message_id')
            current_user = session.get('username')
            if current_user and current_user != 'Anonym':
                messages[:] = [
                    m for m in messages
                    if not (m['id'] == message_id and m['sender'] == current_user)
                ]
            return redirect(url_for('index'))

    return render_template(
        'index.html',
        messages=messages,
        current_user=session.get('username'),
        error=error,
        prefill_content=prefill_content,
    )


if __name__ == '__main__':
    app.run(debug=True)
