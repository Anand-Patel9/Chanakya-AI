memory_store = {}


def save_interaction(user_id, query, response):
    if user_id not in memory_store:
        memory_store[user_id] = []

    memory_store[user_id].append({
        "query": query,
        "response": response
    })


def get_memory(user_id):
    return memory_store.get(user_id, [])[-5:]  # last 5 interactions