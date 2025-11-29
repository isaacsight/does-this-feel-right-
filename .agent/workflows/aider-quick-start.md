---
description: Quick start guide for using Aider
---

# Aider Quick Start Guide

Aider is a terminal-based AI coding assistant that works with multiple AI models. Use it when you want flexibility and don't need a GUI.

## Setup API Keys

```bash
# For Claude (same model as Antigravity)
export ANTHROPIC_API_KEY=your-key-here

# For OpenAI
export OPENAI_API_KEY=your-key-here

# For Google Gemini
export GEMINI_API_KEY=your-key-here
```

**Tip:** Add these to your `~/.zshrc` to make them permanent.

## Basic Usage

// turbo
### Start Aider in a project
```bash
cd /Users/isaachernandez/blog\ design
aider
```

// turbo
### Start with specific model
```bash
# Use Claude Sonnet (default, good balance)
aider --model claude-3-5-sonnet-20241022

# Use GPT-4
aider --model gpt-4-turbo

# Use Gemini
aider --model gemini/gemini-2.0-flash-exp
```

// turbo
### Add files to the chat context
```bash
# Start with specific files
aider index.html style.css

# Or add files during chat
/add path/to/file.py
```

## Common Commands (inside Aider)

- `/help` - Show all commands
- `/add <file>` - Add file to chat
- `/drop <file>` - Remove file from chat
- `/ls` - List files in chat
- `/clear` - Clear chat history
- `/undo` - Undo last change
- `/diff` - Show recent changes
- `/commit` - Commit changes
- `/exit` - Exit Aider

## Example Workflows

### Quick Refactoring
```bash
aider src/component.js
# Then type: "Extract the validation logic into a separate function"
```

### Multi-file Feature
```bash
aider --model claude-3-5-sonnet-20241022
# Inside aider:
/add index.html
/add style.css
/add app.js
# Then describe the feature you want
```

### Code Review
```bash
aider --model gpt-4-turbo src/new-feature.py
# Then: "Review this code for bugs and suggest improvements"
```

## Pro Tips

1. **Auto-commit enabled by default** - Aider commits after each change
2. **Use git** - Aider works best in git repos
3. **Switch models mid-chat** - `/model gpt-4` to change models
4. **Cheaper models for simple tasks** - Use `gemini-2.0-flash-exp` for quick edits
5. **Voice mode** - `aider --voice` for hands-free coding (requires API key)

## When to Use Aider vs Antigravity

**Use Aider:**
- Working on remote servers over SSH
- Want to try different AI models
- Need git commit history for changes
- Working in terminal-heavy workflow
- Cost-conscious (can use cheaper models)

**Use Antigravity:**
- Visual design work
- Need to see UI changes immediately
- Prefer polished chat interface
- Working on complex multi-step tasks

## Troubleshooting

**"No API key found"**
```bash
export ANTHROPIC_API_KEY=your-key-here
aider
```

**"Model not available"**
```bash
# List all available models
aider --models
```

**"Git not initialized"**
```bash
git init
git add .
git commit -m "Initial commit"
aider
```
