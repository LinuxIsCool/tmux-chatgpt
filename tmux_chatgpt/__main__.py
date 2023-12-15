#!/usr/bin/env python3
import asyncio
import os

import click
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
)


async def list_models_async() -> None:
    models = await client.models.list()
    return models


async def completion_async(message, model='gpt-4') -> None:
    completion = await client.chat.completions.create(
        messages=[
            {
                'role': 'user',
                'content': message,
            }
        ],
        model=model,
    )
    return completion


@click.command()
@click.option(
    '-l',
    '--list-models',
    'list_models_flag',
    default=False,
    is_flag=True,
    help='List available models.',
)
@click.option(
    '-d',
    '--model',
    'model',
    type=click.Choice(['gpt-3.5-turbo', 'gpt-4'], case_sensitive=True),
    default='gpt-4',
    help='The model to use.',
)
@click.option('-m', '--message', 'message', help='The message to send.')
def main(message: str, model: str, list_models_flag: bool):
    if message is None:
        message = input('Enter your message: ')
    asyncio.run(handle_command(message, model, list_models_flag))


async def handle_command(message: str, model: str, list_models_flag: bool):
    if list_models_flag:
        models = await list_models_async()
        models_data = dict(models)['data']
        print(models_data)
    else:
        completion = await completion_async(message=message, model=model)
        print(completion.choices[0].message.content)


# Example of XDG data IO
def handle_io():
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
