from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id is None:
        return False, "Error: No current question ID provided."

    # Store the answer in the session (You can implement this based on your session storage mechanism)
    session["answer_" + str(current_question_id)] = answer
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''

    # Assuming PYTHON_QUESTION_LIST is a list of dictionaries with 'id' and 'question' keys
    for i, question in enumerate(PYTHON_QUESTION_LIST):
        if question['id'] == current_question_id:
            if i + 1 < len(PYTHON_QUESTION_LIST):
                return PYTHON_QUESTION_LIST[i + 1]['question'], PYTHON_QUESTION_LIST[i + 1]['id']
            else:
                return None, None

    return None, None


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    # Calculate score based on the answers stored in the session
    score = 0
    for question in PYTHON_QUESTION_LIST:
        question_id = question['id']
        answer_key = "answer_" + str(question_id)
        if answer_key in session:
            # Evaluate the answer and update the score accordingly
            score += 1

    final_response = f"Thank you for answering all questions. Your final score is {score}."
    return final_response