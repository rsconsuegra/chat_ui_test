"""Main entry point for the Chainlit chat application."""

from logging import getLogger

import chainlit as cl
from chainlit.cli import run_chainlit

from src.bootstrap import get_container
from src.domain.errors.exceptions import ChatAppError
from src.infrastructure.container import Container

logger = getLogger(__name__)


@cl.on_chat_start
async def on_chat_start() -> None:
    """Handle chat start event.

    Raises:
        ChatAppError: If database initialization or user creation fails.
        Exception: If an unexpected error occurs.
    """
    container: Container | None = None
    try:
        container = get_container()
        cl.user_session.set("container", container)

        session_adapter = container.get_session_adapter()

        username = await session_adapter.get_or_prompt_username(
            prompt="Welcome! Please enter your username to continue:",
            timeout=300,
        )
        if username is None:
            message_adapter = container.get_message_adapter()
            await message_adapter.send_message(
                "Username is required. Please refresh the page.",
            )
            return

        user = await session_adapter.get_or_create_user(username)

        await session_adapter.set_session_data("username", username)
        await session_adapter.set_session_data("user_id", user.id)

        provider = container.get_provider()
        message_adapter = container.get_message_adapter()
        await message_adapter.send_message(
            f"Hello, {username}! Welcome to the LLM Chat Application.\n\n"
            f"Connected provider: {provider.name}.\n"
            f"Your user ID is: {user.id}",
        )

    except ChatAppError as exc:
        logger.exception("Chat initialization failed")
        if container:
            message_adapter = container.get_message_adapter()
            await message_adapter.send_message(f"Error initializing chat: {exc}")
        raise
    except Exception as exc:
        logger.exception("Unexpected chat initialization error")
        if container:
            message_adapter = container.get_message_adapter()
            await message_adapter.send_message(f"Unexpected error initializing chat: {exc}")
        raise


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """Handle incoming messages.

    Args:
        message: The Chainlit message object containing user input.

    Raises:
        ChatAppError: If message processing or database operations fail.
        Exception: If an unexpected error occurs.
    """
    try:
        container = cl.user_session.get("container")
        if not isinstance(container, Container):
            logger.warning("Container missing from session")
            return

        session_adapter = container.get_session_adapter()

        username = await session_adapter.get_session_data("username")
        if username is None:
            logger.warning("Missing username in session")
            message_adapter = container.get_message_adapter()
            await message_adapter.send_message(
                "Please refresh the page and enter your username.",
            )
            return

        user_id = await session_adapter.get_session_data("user_id")
        if not isinstance(user_id, int) or user_id <= 0:
            logger.warning("Invalid user id in session")
            message_adapter = container.get_message_adapter()
            await message_adapter.send_message(
                "Session error. Please refresh the page.",
            )
            return

        use_case = container.get_send_message_use_case()
        message_adapter = container.get_message_adapter()

        response = message_adapter.create_streaming_message()
        async for chunk in use_case.stream_response(
            user_id=user_id,
            user_input=message.content,
        ):
            await response.stream_token(chunk)

        await response.send()

    except ChatAppError as exc:
        logger.exception("Chat message processing failed")
        container = cl.user_session.get("container")
        if isinstance(container, Container):
            message_adapter = container.get_message_adapter()
            await message_adapter.send_message(f"Error processing message: {exc}")
        raise
    except Exception as exc:
        logger.exception("Unexpected chat message processing error")
        container = cl.user_session.get("container")
        if isinstance(container, Container):
            message_adapter = container.get_message_adapter()
            await message_adapter.send_message(f"Unexpected error processing message: {exc}")
        raise


if __name__ == "__main__":
    run_chainlit(__file__)
