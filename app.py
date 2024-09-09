from flask import Flask, render_template, redirect, request, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'eW91cl9zZWNyZXRfa2V5'  # Set the secret key to something unique and secret

# Simulating JSON data
# Load the data from the JSON file
with open('questions.json') as f:
    questions = json.load(f)

# Home route displays a list of subcategories
@app.route('/')
def index():
    return render_template('index.html', questions=questions)

# Route for displaying a single flashcard for each topic
@app.route('/questions/<area_id>')
def area(area_id):
    area = next((s for s in questions if s["area_id"] == area_id), None)

    if area is None:
        flash(f"Area {area_id} not found", 'error')
        return redirect(request.referrer or url_for('index'))

    return render_template(
        'area.html',
        area=area,
        questions=questions[area_id]['questions']
    )

# Route for displaying a single flashcard for each topic
@app.route('/questions/<area_id>/<question_id>')
def question(area_id, question_id):
    area = next((s for s in questions if s["area_id"] == area_id), None)

    if area is None:
        flash(f"Area {area_id} not found", 'error')
        return redirect(request.referrer or url_for('index'))

    question = next((s for s in area['questions'] if s["question_id"] == question_id), None)

    if question is None:
        flash(f"Question {question_id} not found", 'error')
        return redirect(request.referrer or url_for('index'))

    # Navigation for previous and next topics
    current_index = area['questions'].index(question)
    prev_index = current_index - 1 if current_index > 0 else None
    next_index = current_index + 1 if current_index < len(area['questions']) - 1 else None

    questions_length = len(area['questions'])

    return render_template(
        'question.html',
        area=area,
        questions=questions,
        question=question,
        prev_index=prev_index, 
        next_index=next_index,
        questions_length=questions_length,
        current_index=current_index
    )

if __name__ == '__main__':
    app.run(debug=True)
