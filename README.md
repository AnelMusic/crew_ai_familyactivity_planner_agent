# Family Activity Planner - CrewAI Demo
![crewarch](https://github.com/user-attachments/assets/65b5ee2b-e53c-4059-bc1e-1f6f3f55e7e6)

This project demonstrates the power of collaborative AI agents using CrewAI framework. Through a practical example of planning family activities in a specific location, it shows how multiple specialized agents can work together to solve complex tasks.

## Overview

The demo implements a family activity planning system where four AI agents collaborate:

1. Child Development Specialist: Evaluates activities for developmental appropriateness
2. Local Community Navigator: Scouts suitable local venues and opportunities
3. Family Activity Coordinator: Assesses practical feasibility
4. Final Decision Maker: Synthesizes all information for optimal recommendations

## Quick Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Clone the repository and install requirements:
```bash
git clone https://github.com/AnelMusic/crew_ai_familyactivity_planner_agent
cd crew_ai_familyactivity_planner_agent
pip install -r requirements.txt
```

3. Set up your environment variables in a .env file:
```env
MODEL=gpt-4o-mini
OPENAI_API_KEY=YOUR_API_KEY
SERPER_API_KEY =YOUR_API_KEY
```

## Usage

1. Save the main script as `crew_ai_demo.py`

2. Run the demo:
```bash
python crew_ai_demo.py
```

## Customization

The demo accepts various parameters that can be modified in the `family_activity_parameters` dictionary:

- Location preferences (city, neighborhoods)
- Child details (age, interests)
- Time and budget constraints
- Accessibility requirements
- Language preferences
- Group composition

Example configuration:
```python
family_activity_parameters = {
    'city': "Munich",
    'neighborhood': "Giesing",
    'age': 6,
    'learning_interests': ["nature", "animals"],
    'max_price_per_person': 35,
    # ... other parameters
}
```

## Important Notes

- This is a demonstration project to illustrate CrewAI's agent collaboration capabilities
- The agents use SerperDev for web searches - make sure to have a valid API key
- All activities are hypothetical and should be verified before actual use

## Output

The system generates structured recommendations using Pydantic models, providing detailed information about each suggested activity including:
- Location and accessibility details
- Age appropriateness and learning benefits
- Practical information (timing, cost, requirements)
- Transportation and accessibility details

## Contributing

This is a demo project meant for learning and exploration. Feel free to:
- Experiment with different agent configurations
- Add new parameters or features
- Adapt it for different use cases

## License

This demo is provided as-is for educational purposes.
