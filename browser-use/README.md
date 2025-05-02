# Browser-Use Experiments

## Prerequisites

Open a Terminal and make sure, you are in the `browser-use` folder.

Create a virtual environment

```bash
python3 -m venv .venv
```

Activate the virtual environment

```bash
source .venv/bin/activate
```

Install the required packages

```bash
pip install -r requirements.txt
```

Create a `.env` file in the `browser-use` folder with the following content. You can get your OpenAI API key from the [OpenAI Platform](https://platform.openai.com/api-keys).

```bash
OPENAI_API_KEY=...
```

## Run the code

```bash
python copilot.py
```
