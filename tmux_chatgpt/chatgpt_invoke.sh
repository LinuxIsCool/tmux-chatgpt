#!/usr/bin/env bash
echo "chatgpt_invoke.sh started" >> /tmp/chatgpt_debug.log

# Determine XDG base directories
XDG_DATA_HOME="${XDG_DATA_HOME:-$HOME/.local/share}"
XDG_CONFIG_HOME="${XDG_CONFIG_HOME:-$HOME/.config}"
echo "XDG directories set" >> /tmp/chatgpt_debug.log

# Define the data and config directories for the tmux-chatgpt plugin
PLUGIN_DATA_DIR="$XDG_DATA_HOME/tmux-chatgpt"
PLUGIN_CONFIG_DIR="$XDG_CONFIG_HOME/tmux-chatgpt"

# Ensure the directories exist
mkdir -p "$PLUGIN_DATA_DIR/threads" "$PLUGIN_CONFIG_DIR"

# Move to the executing scripts directory and save the path to $SCRIPTS_DIR
SCRIPTS_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
echo "SCRIPTS_DIR: $SCRIPTS_DIR" >> /tmp/chatgpt_debug.log

# Function to invoke fzf with popup and capture the selected thread
invoke_chatgpt() {
    echo "About to display fzf popup..." >> /tmp/chatgpt_debug.log

    # Create a temporary file to capture the selection from fzf
    local temp_file=$(mktemp)
    
    # Open fzf in a tmux popup window and write selection to temporary file
    tmux display-popup -E "bash -c 'printf \"New Conversation\n\$(ls -1 \"$PLUGIN_DATA_DIR/threads\")\" | fzf > \"$temp_file\"'"

    # Read the selection from the file
    local selected_thread=$(cat "$temp_file")
    echo "Selected thread: $selected_thread" >> /tmp/chatgpt_debug.log

    # Clean up the temporary file
    rm "$temp_file"

    # Start new thread
    if [[ $selected_thread == "New Conversation" ]]; then
        python "$SCRIPTS_DIR/__main__.py"

    # Continue existing thread with context
    else
        local context_file="$PLUGIN_DATA_DIR/threads/${selected_thread}/context.json"
        echo "Context file: $context_file" >> /tmp/chatgpt_debug.log
        # XXX TODO: Starting a session with context.
        # (cat "$context_file") | python3 "$SCRIPTS_DIR/__main__.py -m"
    fi

    rm -f "$pane_content_file"
}

invoke_chatgpt
