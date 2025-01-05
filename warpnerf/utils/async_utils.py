import asyncio

def do_sync(awaitable):
    """
    Runs an awaitable (coroutine or async function call) synchronously.

    Parameters:
        awaitable (coroutine): The awaitable to run.

    Returns:
        The result of the awaitable.
    """
    try:
        # Get the current event loop or create a new one
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If the loop is running, create a task for the awaitable
            return asyncio.create_task(awaitable)
        else:
            # If no loop is running, run the awaitable directly
            return loop.run_until_complete(awaitable)
    except RuntimeError:
        # Create a new event loop if necessary
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        return new_loop.run_until_complete(awaitable)
