import logging
from pathlib import Path


ENV_CONTENT = """# AI_Art_Critic configuration
# Which LLM to use: OpenAI (vision-enabled) or none
LLM_PROVIDER=OpenAI

# OpenAI settings (if using OpenAI)
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini

# Model behavior
AI_TEMPERATURE=0.2
"""


def write_file(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    project_dir = Path(__file__).parent

    env_path = project_dir / ".env"
    env_example_path = project_dir / ".env.example"

    if not env_path.exists():
        write_file(env_path, ENV_CONTENT)
        logging.info("Created .env with placeholders")
    else:
        logging.info(".env already exists — skipped")

    write_file(env_example_path, ENV_CONTENT)
    logging.info("Created/updated .env.example")


if __name__ == "__main__":
    main()



