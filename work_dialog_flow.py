from google.cloud import dialogflow
import json
import os
from dotenv import load_dotenv


def detect_intent_texts(google_project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(google_project_id, session_id)

    text_input = dialogflow.TextInput(text=texts, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text, response.query_result.intent.is_fallback


def create_intent(google_project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(google_project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


if __name__ == '__main__':
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    project_id = os.environ['PROJECT_ID']

    with open('questions.json', encoding='utf-8') as file_intents:
        intents = json.load(file_intents)
    for intent_name, training in intents.items():
        questions = training['questions']
        answer = training['answer']
        create_intent(project_id, intent_name, questions, [answer])
