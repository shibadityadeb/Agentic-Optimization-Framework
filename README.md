## Anthropic Claude LLM Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

2. Set your Anthropic API key:
   - Copy `.env.example` to `.env` and add your real API key.
   - Or set `ANTHROPIC_API_KEY` in your environment.

3. The analyzer agent will use Claude via the Anthropic API for LLM calls.
