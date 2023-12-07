#!/usr/bin/env python3
import json
import os
import sys

import openai


def send_query_to_chatgpt(query, context):
    """
    Send the query to the ChatGPT API and retrieve the response.
    :param query: The user's query from tmux session.
    :param context: Previous conversation context.
    :return: The response from ChatGPT.
    """
    # Placeholder for OpenAI API interaction
    openai.api_key = os.environ.get('OPENAI_API_KEY')

    try:
        response = openai.Completion.create(
            engine='davinci',
            prompt=query,
            max_tokens=150,
            # Additional parameters can be added here
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)


def main():
    # Determine XDG base directories
    xdg_data_home = os.environ.get(
        'XDG_DATA_HOME', os.path.expanduser('~/.local/share')
    )
    print(f'{xdg_data_home=}')
    plugin_data_dir = os.path.join(xdg_data_home, 'tmux-chatgpt')
    print(f'{plugin_data_dir=}')

    # Read the user's query from stdin (captured from the tmux pane)
    query = sys.stdin.read()
    print(f'{query=}')

    # Retrieve or initialize the context (here we just use a placeholder for demonstration)
    context = {
        'session': 'example_session_id'
    }  # Replace with actual logic to retrieve context

    # Retrieve the response from ChatGPT
    chatgpt_response = send_query_to_chatgpt(query, context)

    # Output the response back to the tmux pane
    print(chatgpt_response)

    # Save the new context into the appropriate thread folder
    # This would involve hashing the session or similar to identify the correct thread ID
    thread_id = 'example_thread_id'  # Placeholder for real thread ID
    context_path = os.path.join(plugin_data_dir, 'threads', thread_id, 'context.json')
    os.makedirs(os.path.dirname(context_path), exist_ok=True)
    with open(context_path, 'w') as context_file:
        json.dump(context, context_file)


if __name__ == '__main__':
    main()
