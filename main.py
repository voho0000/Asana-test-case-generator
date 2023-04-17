import asana
import openai
import os
import requests
import json
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up API key
ASANA_API_KEY = os.getenv('ASANA_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Function to get a asana
def get_asana_task(task_gid):
    client = asana.Client.access_token(ASANA_API_KEY)
    client.headers.update({
        "Asana-Enable": "new_user_task_lists,new_goal_memberships"
    })
    task = client.tasks.get_task(task_gid)
    return task

# Function to create a new task in Asana
def create_asana_task(project_gid, name, notes):
    client = asana.Client.access_token(ASANA_API_KEY)
    client.headers.update({
        "Asana-Enable": "new_user_task_lists,new_goal_memberships"
    })
    new_task = client.tasks.create({"projects": [project_gid], "name": name, "notes": notes})
    return new_task

def transform_description_to_test_steps(defect_description):
    prompt = f"從下述描述產生test case: {defect_description}"
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1000,
        "temperature": 0.5
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {OPENAI_API_KEY}"
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions', headers=headers, data=json.dumps(data))
    response_json = response.json()
    test_steps = response_json['choices'][0]['message']['content'].strip()
    return test_steps


parser = argparse.ArgumentParser(description='Asana Test Case Generator')
parser.add_argument('--task_gid', required=True, help='Task GID to process')
parser.add_argument('--project_gid', required=True, help='Project GID where the new task will be created')
args = parser.parse_args()

def main(task_gid, project_gid):
    task = get_asana_task(task_gid)
    defect_description = task['notes']
    print("Defect Description:", defect_description)

    test_steps = transform_description_to_test_steps(defect_description)
    print("Test Steps:", test_steps)

    task_name = 'New Test Case'
    new_task = create_asana_task(project_gid, task_name, test_steps)
    print("New task created:", new_task['gid'])
    
if __name__ == "__main__":
    main(args.task_gid, args.project_gid)