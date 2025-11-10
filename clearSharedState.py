python3 -c "import asyncio; from data.shared_state import SharedState; \
asyncio.run(SharedState.init()); asyncio.run(SharedState.clear_all())"
