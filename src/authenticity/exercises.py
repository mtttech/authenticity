"""
exercises.py
Author:     Marcus T Taylor
Created:    11.10.24
Modified:   05.07.24
"""

# https://thefitnessphantom.com/list-of-dumbbell-exercises
exercise_list = {
    "Abs and Obliques": [
        "Bird-Dog Plank",
        "Decline Dumbbell Crunches",
        "Dumbbell Plank Drag",
        "Dumbbell Plank Rowing",
        "Hanging Knee Raises",
        "Leg Raises",
        "Oblique crunches",
        "Reverse Crunches",
        "Russian Twist",
        "Side Plank",
        "Side Plank Hip Lifts",
        "Side-plank Rotation",
        "Standing Oblique Rotation",
        "Straight-Arm Crunches",
        "Toe Touch Crunches",
        "Wood Chop (High to Low)",
        "Wood Chop (Low to High)",
    ],
    "Back": [
        "Bent-Over Row Overhand Grip",
        "Chest-Supported Incline Row",
        "Dumbbell Deadlift",
        "Dumbbell Pendley Row",
        "Dumbbell Renegade Row",
        "Dumbbell Seal Row",
        "Dumbbell Wide Row",
        "Incline I-Y-T Raises",
        "Incline Plank Row",
        "One Arm Dumbbell Row",
        "Underhand Inverted Row",
    ],
    "Biceps": [
        "Alternating Curls",
        "Concentration Curl",
        "Dumbbell Crossbody Curl",
        "Dumbbell Drag Curl",
        "Dumbbell Hammer Curl",
        "Dumbbell Preacher Curl",
        "Dumbbell Reverse Curl",
        "Dumbbell Zottoman Curl",
        "Incline Dumbbell Bicep Curl",
        "Incline Prone Bicep Curl",
        "Preacher Hammer Curl",
        "Single-arm Hammer Curl",
    ],
    "Calves": [
        "Dumbbell Farmer's Walk on Toes",
        "Leaning Single-Leg Calf Raises",
        "Seated Dumbbell Calf Raises",
        "Standing Dumbbell Calf Raises",
    ],
    "Chest": [
        "Around The World",
        "Bridge Press",
        "Decline Bench Press",
        "Deficit Pushup",
        "Dumbbell Pullover",
        "Dumbbell Squeeze Press",
        "Dumbbell Svend Press",
        "Flat Bench Press",
        "Flat Dumbbell Fly",
        "Floor Press",
        "Incline Bench Press",
        "Incline Close Grip DB Press",
        "Incline Dumbbell Fly",
        "Standing Upward Fly",
        "Underhand Grip Chest Press",
    ],
    "Forearm": [
        "Dumbbell Farmers Walk" "Dumbbell Wrist Curl",
        "Dumbbell Wrist Extension",
        "Dumbbell Wrist Rotation",
        "Neutral Grip Wrist Curl",
    ],
    "Glutes": [
        "DB Donkey Kicks",
        "Dumbbell Glute Bridges",
        "Dumbbell Hip Thrust",
        "Frog Pump",
        "Leaning Forward Step-up",
    ],
    "Hamstrings": [
        "DB Good Morning",
        "DB Hamstring Bridge",
        "Hamstring March",
        "Lying Leg Curl",
        "Romanian Deadlift",
        "Single-Leg Deadlift",
        "Stiff-Legged Deadlift",
    ],
    "Lower Back": [
        "Bird-Dog Plank",
        "Dumbbell Hip Lift",
        "Dumbbell Hyperextension",
        "Good Morning",
        "Superman Row",
    ],
    "Shoulders": [
        "Alternating Front Raises",
        "Arnold Press",
        "Bent-over Lateral Raises",
        "Chest Supported Rear Delt Row",
        "Dumbbell Face Pull",
        "Dumbbell Lateral Raises",
        "Dumbbell Shrug",
        "Overhead Press",
        "Push Press",
        "Seated/Incline Y Raises",
        "Upright Row",
    ],
    "Triceps": [
        "Bent-over Single-arm Triceps Kickback",
        "Close Grip Push-Ups",
        "Crush Grip Push-Ups",
        "Floor Press",
        "Lying Prone Incline Triceps Kickback",
        "Lying Triceps Extension",
        "Neutral Grip Dumbbell Bench Press",
        "Seated Overhead Triceps Extension",
        "Single-arm Overhead Triceps Extension",
        "Tate Press",
    ],
    "Quads": [
        "Bulgarian Split Squat",
        "Curtsy Squat",
        "Forward Lunges",
        "Goblet Squat",
        "Leg Extension",
        "Pop Squat",
        "Reverse Lunges",
        "Sumo Squat",
        "Step-up",
    ],
}


def get_exercises_by_group(muscle_group: str) -> list[str]:
    return exercise_list[muscle_group]


def get_muscle_groups() -> list[str]:
    return list(exercise_list.keys())
