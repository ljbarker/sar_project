# Search and Rescue (SAR) Agent Framework - CSC 581

## Resource Manager Agent Implementation

This repository contains an implementation of the Resource Manager Agent. Agent data can be outputted with the consolidate_ouput function and uses a JSON format.

## Prerequisites

- Python 3.8 or higher
- pyenv (recommended for Python version management)
- pip (for dependency management)

## Setup and Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd sar-project
```

2. Set up Python environment:

```bash
# Using pyenv (recommended)
pyenv install 3.9.6  # or your preferred version
pyenv local 3.9.6

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate     # On Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

4. Configure environment variables:

#### Google Gemini:

- Obtain required API keys:
  1. `pip install google-generativeai`
  2. `import google.generativeai as genai`
  3. Google Gemini API Key: Obtain at https://aistudio.google.com/apikey
- Configure with the following:
  ```
  genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
  ```

Make sure to keep your `.env` file private and never commit it to version control.

## Project Structure

```
sar-project/
├── src/
│   └── sar_project/         # Main package directory
│       └── agents/          # Agent implementations
│       └── config/          # Configuration and settings
│       └── knowledge/       # Knowledge base implementations
├── tests/                   # Test directory
├── pyproject.toml           # Project metadata and build configuration
├── requirements.txt         # Project dependencies
└── .env                     # Environment configuration
```

## Development

This project follows modern Python development practices:

1. Source code is organized in the `src/sar_project` layout
2. Use `pip install -e .` for development installation
3. Run tests with `pytest tests/`
4. Follow the existing code style and structure
5. Make sure to update requirements.txt when adding dependencies

## Example Use-Case

### Scenario

A search and rescue operation requires the allocation of resources such as helicopters and boats. The Resource Manager Agent needs to:

1. Identify available resources.
2. Plan the deployment of resources.
3. Allocate resources based on priority.
4. Optimize resource allocation using Linear Programming.
5. Query external databases for recent information.
6. Make trade-off decisions based on available options.

### Example Code

```python
from sar_project.agents.resource_manager_agent import ResourceManagerAgent

# Initialize the agent
agent = ResourceManagerAgent()

# Identify resources
agent.resources = {
    "helicopter": {"status": "available", "available_from": 1},
    "boat": {"status": "in_use", "available_from": 2}
}
print(agent.identify_resources())

# Plan deployment
plan_details = ["helicopter", "boat"]
print(agent.plan_deployment(plan_details))

# Allocate resources
allocation_details = {"helicopter": "agency1", "boat": "agency2"}
print(agent.allocate_resources(allocation_details))

# Optimize allocation
criteria = {
    "costs": [1, 2],
    "constraints": [[1, 1]],
    "bounds": [1]
}
print(agent.optimize_allocation(criteria))

# Query external databases
agent.databases = ["https://api.example.com/resource_data"]
query = {"type": "helicopter"}
print(agent.query_database(query))

# Make trade-off decisions
options = [
    {"resource": "helicopter", "priority": 2},
    {"resource": "boat", "priority": 1}
]
print(agent.trade_off_decision(options))
```

## Recent Changes

### Edits to `resource_manager_agent.py`

In the latest commit, the following changes were made to `resource_manager_agent.py`:

1. **Added `optimize_allocation` method**:

   - This method uses Linear Programming to optimize resource allocation based on provided criteria.
   - **Feedback 2**: This addresses the suggestion to use an optimizer for determining criteria numerically.
   - Example usage:
     ```python
     criteria = {
         "costs": [1, 2],
         "constraints": [[1, 1]],
         "bounds": [1]
     }
     print(agent.optimize_allocation(criteria))
     ```

2. **Added `query_database` method**:

   - This method queries external databases for recent information.
   - **Feedback 3**: This enhances the interaction with the `databases` field, allowing the agent to query websites or other databases.
   - Example usage:
     ```python
     agent.databases = ["https://api.example.com/resource_data"]
     query = {"type": "helicopter"}
     print(agent.query_database(query))
     ```

3. **Added `trade_off_decision` method**:

   - This method makes trade-off decisions based on provided options.
   - **Feedback 5**: This helps the agent formulate what is important in trade-off situations.
   - Example usage:
     ```python
     options = [
         {"resource": "helicopter", "priority": 2},
         {"resource": "boat", "priority": 1}
     ]
     print(agent.trade_off_decision(options))
     ```

4. **Enhanced `process_request` method**:
   - Added handling for new request types: `optimize_allocation`, `query_database`, and `trade_off_decision`.
   - **Feedback 4**: This makes the schedules more granular and allows the computer to find schedules that match criteria.

These changes enhance the functionality of the Resource Manager Agent, allowing it to perform more complex operations and interact with external data sources.
