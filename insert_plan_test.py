from mongo_connection import plans_collection

plan = {
    "day": "Monday",
    "muscle_group": "Chest & Triceps",
    "exercises": [
        {"name": "Bench Press", "sets": 4, "reps": 10},
        {"name": "Tricep Dips", "sets": 3, "reps": 12}
    ],
    "notes": "Start easy and focus on form."
}

result = plans_collection.insert_one(plan)
print("Inserted plan with ID:", result.inserted_id)