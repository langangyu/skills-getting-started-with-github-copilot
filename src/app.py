"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
# Add more activities: 2 sports, 2 artistic, 2 intellectual
activities = {
    "Soccer Team": {
        "description": "Join the school soccer team and compete in local leagues",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": []
    },
    "Basketball Club": {
        "description": "Practice basketball skills and play friendly matches",
        "schedule": "Mondays and Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": []
    },
    "Art Club": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": []
    },
    "Drama Society": {
        "description": "Participate in theater productions and acting workshops",
        "schedule": "Fridays, 4:00 PM - 6:00 PM",
        "max_participants": 25,
        "participants": []
    },
    "Math Olympiad": {
        "description": "Prepare for math competitions and solve challenging problems",
        "schedule": "Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 15,
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": []
    },
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specificy activity
    activity = activities[activity_name]

    #validate studuent is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Already signed up for this activity")
    # Validate max participants
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")
    # Validate email format
    if "@" not in email or "." not in email.split("@")[-1]:
        raise HTTPException(status_code=400, detail="Invalid email format")
    # Validate email domain
    if not email.endswith("@mergington.edu"):
        raise HTTPException(status_code=400, detail="Email must be from mergington.edu")
    # Validate email is not empty
    if not email:
        raise HTTPException(status_code=400, detail="Email cannot be empty")
    # Validate email is not too long
    if len(email) > 50:
        raise HTTPException(status_code=400, detail="Email is too long")
    # Validate email is not too short
    if len(email) < 5:
        raise HTTPException(status_code=400, detail="Email is too short")
    # Validate email is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Already signed up for this activity")
    

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
