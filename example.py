from pymongo import MongoClient
import pandas as pd

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client['PipelinesDB']
collection = db['Project2']

# Fetch all documents from the collection
data = list(collection.find({}))

# Initialize lists for structured tables
projects = []
clients = []
technologies = []
team_members = []
milestones = []

# Loop through each document (project)
for doc in data:
    project_id = doc.get("project_id")

    # Project table
    projects.append({
        "project_id": project_id,
        "project_name": doc.get("project_name"),
        "status": doc.get("status"),
        "project_manager": doc.get("team", {}).get("project_manager")
    })

    # Client table
    client_info = doc.get("client", {})
    location = client_info.get("location", {})
    clients.append({
        "project_id": project_id,
        "client_name": client_info.get("name"),
        "industry": client_info.get("industry"),
        "city": location.get("city"),
        "country": location.get("country")
    })

    # Technologies table
    for tech in doc.get("technologies", []):
        technologies.append({
            "project_id": project_id,
            "technology": tech
        })

    # Team Members table
    for member in doc.get("team", {}).get("members", []):
        team_members.append({
            "project_id": project_id,
            "name": member.get("name"),
            "role": member.get("role")
        })

    # Milestones table
    for milestone in doc.get("milestones", []):
        milestones.append({
            "project_id": project_id,
            "milestone_name": milestone.get("name"),
            "due_date": milestone.get("due_date")
        })

# Convert to DataFrames for visualization or further processing
df_projects = pd.DataFrame(projects)
df_clients = pd.DataFrame(clients)
df_technologies = pd.DataFrame(technologies)
df_team_members = pd.DataFrame(team_members)
df_milestones = pd.DataFrame(milestones)

# Example print
print("Projects:\n", df_projects)
print("\nClients:\n", df_clients)
print("\nTechnologies:\n", df_technologies)
print("\nTeam Members:\n", df_team_members)
print("\nMilestones:\n", df_milestones)
