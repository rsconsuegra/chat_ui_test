"""Main entry point for the Chainlit chat application."""

from datetime import datetime, timezone
from logging import getLogger
from typing import cast

import chainlit as cl
from chainlit.cli import run_chainlit

from src.application.use_cases.send_message import SendMessageUseCase
from src.bootstrap import get_container
from src.domain.errors.exceptions import ChatAppError
from src.domain.models.user import User
from src.infrastructure.container import Container

logger = getLogger(__name__)


@cl.on_chat_start
async def on_chat_start() -> None:
    """Handle chat start event.

    Raises:
        ChatAppError: If database initialization or user creation fails.
        Exception: If database initialization or user creation fails.
    """
    try:
        container = get_container()
        cl.user_session.set("container", container)

        username = cl.user_session.get("username")
        if username is None:
            res = await cl.AskUserMessage(
                content="Welcome! Please enter your username to continue:",
                timeout=300,
            ).send()

            if res is None:
                await cl.Message(content="Username is required. Please refresh the page.").send()
                return

            res_data = cast(dict[str, object], res) if isinstance(res, dict) else {}
            output = res_data.get("output")
            if not isinstance(output, str) or not output.strip():
                await cl.Message(content="Username is required. Please refresh the page.").send()
                return

            username = output.strip()
            cl.user_session.set("username", username)

        user_repository = container.get_user_repository()
        user = await user_repository.find_by_username(username)
        if user is None:
            user = User(
                id=0,  # Will be assigned by repository
                username=username,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc),
            )
            user = await user_repository.save(user)

        cl.user_session.set("user_id", user.id)

        provider = container.get_provider()
        await cl.Message(
            content=(
                f"Hello, {username}! Welcome to the LLM Chat Application.\n\n"
                f"Connected provider: {provider.name}.\n"
                f"Your user ID is: {user.id}"
            )
        ).send()

    except ChatAppError as exc:
        logger.exception("Chat initialization failed")
        await cl.Message(content=f"Error initializing chat: {exc}").send()
        raise
    except Exception as exc:
        logger.exception("Unexpected chat initialization error")
        await cl.Message(content=f"Unexpected error initializing chat: {exc}").send()
        raise


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """Handle incoming messages.

    Args:
        message: The Chainlit message object containing user input.

    Raises:
        ChatAppError: If message processing or database operations fail.
        Exception: If message processing or database operations fail.
    """
    try:
        username = cl.user_session.get("username")
        if username is None:
            logger.warning("Missing username in session")
            await cl.Message(content="Please refresh the page and enter your username.").send()
            return

        container = cl.user_session.get("container")
        if not isinstance(container, Container):
            logger.warning("Container missing from session")
            await cl.Message(content="Session error. Please refresh the page.").send()
            return

        user_id = cl.user_session.get("user_id")
        if not isinstance(user_id, int) or user_id <= 0:
            logger.warning("Invalid user id in session")
            await cl.Message(content="Session error. Please refresh the page.").send()
            return

        use_case = SendMessageUseCase(
            message_repository=container.get_message_repository(),
            provider=container.get_provider(),
            prompt_config=container.get_prompt_config(),
        )

        response = cl.Message(content="")
        async for chunk in use_case.stream_response(
            user_id=user_id,
            user_input=message.content,
        ):
            await response.stream_token(chunk)

        await response.send()

    except ChatAppError as exc:
        logger.exception("Chat message processing failed")
        await cl.Message(content=f"Error processing message: {exc}").send()
        raise
    except Exception as exc:
        logger.exception("Unexpected chat message processing error")
        await cl.Message(content=f"Unexpected error processing message: {exc}").send()
        raise


if __name__ == "__main__":
    run_chainlit(__file__)
