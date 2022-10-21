
chat_rooms = {
    "kumnal": [1,2,3,4,5,6],
    "kumkumkum": [],
    "new room": ["n", "empty"]
}

if "new room" in chat_rooms:
    if "empty" in chat_rooms["new room"]:
        (chat_rooms["new room"]).remove("empty")

print(chat_rooms)