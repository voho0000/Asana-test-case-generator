# Asana Test Case Generator
Asana Test Case Generator is a Python script that utilizes Asana and OpenAI APIs to create a new Asana task with test steps derived from an existing task's description. The script leverages the GPT-3.5-turbo language model to generate the test steps, making it easier for QA teams to generate test cases from defect descriptions.

## Installation
1. Clone the repository:

2. Install the required packages:
`pip install -r requirements.txt`

3. Create a .env file in the project root directory and add the following environment variables:
'''
ASANA_API_KEY=<your_asana_api_key>
OPENAI_API_KEY=<your_openai_api_key>
'''

## Usage
Run the script with the following command:

`python main.py --task_gid <task_gid> --project_gid <project_gid>`

Replace <task_gid> with the GID of the existing task containing the defect description, and <project_gid> with the GID of the project where the new task with test steps will be created.

`python main.py --task_gid 1234567890123456 --project_gid 9876543210987654`

## Functionality
The script contains the following functions:

- `get_asana_task(task_gid)`: Retrieves a task from Asana using its GID.
- `create_asana_task(project_gid, name, notes)`: Creates a new task in Asana with the specified project GID, name, and notes.
- `transform_description_to_test_steps(defect_description)`: Transforms a defect description into test steps using the OpenAI GPT-3.5-turbo language model.
- `main(task_gid, project_gid)`: Main function that gets the Asana task, transforms its description into test steps, and creates a new task with the generated test steps.

## License
This project is licensed under the MIT License. See the LICENSE file for details.