from crewai import Agent, Task, Crew
from dotenv import load_dotenv
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel
from typing import List

class ActivityDetails(BaseModel):
    name: str
    location: str
    distance: float
    type: str
    min_age: int
    max_age: int
    learning_focus: List[str]
    parent_involvement: str
    price_per_person: float
    language: str
    public_transport_access: bool
    start_time: str
    end_time: str
    booking_required: bool
    wheelchair_accessible: bool
    stroller_friendly: bool
    description: str  # Full paragraph description


class ActivityList(BaseModel):
    activities: List[ActivityDetails]

class Agents:

        
    def __init__(self):
        # Agent 1: Child Development Specialist
        self.child_development_specialist = Agent(
            role="Child Development Specialist",
            goal="Provide developmental guidelines and evaluate activity suitability "
                "for different age groups and developmental stages",
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            backstory=(
                "As an expert in child development psychology and education, "
                "you provide the foundational assessment of what activities are "
                "developmentally appropriate and beneficial for children at different stages. "
                "Your recommendations guide the other agents in finding suitable activities "
                "that match children's developmental needs, interests, and abilities."
            )
        )    
    
        # Agent 2: Local Community Navigator
        self.local_community_navigator = Agent(
            role="Local Community Navigator",
            goal="Identify and evaluate local opportunities that align with "
                "the developmental guidelines provided by the Child Development Specialist",
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            backstory=(
                "Working closely with the Child Development Specialist's recommendations, "
                "you maintain a comprehensive database of local venues, programs, and events. "
                "You filter and match these opportunities against the developmental criteria "
                "to create a curated list of age-appropriate local activities. "
                "Your knowledge of the community ecosystem helps translate developmental "
                "goals into concrete local opportunities."
            )
        )

        # Agent 3: Family Activity Coordinator
        self.family_activity_coordinator = Agent(
            role="Family Activity Coordinator",
            goal="Create practical family activity plans by combining developmental insights "
                "and local opportunities into executable family experiences",
            tools=[SerperDevTool(), ScrapeWebsiteTool()],
            verbose=True,
            backstory=(
                "As the final planning specialist, you synthesize the developmental guidelines "
                "from the Child Development Specialist and the local opportunities from the "
                "Community Navigator to create concrete, practical family activity plans. "
                "You consider additional factors such as logistics, scheduling, budgeting, "
                "and family preferences to transform recommendations into actionable plans. "
                "Your expertise ensures that developmentally appropriate activities are "
                "implemented in a way that works for the whole family."
            )
        )
        # Agent 4: Final Decision Maker
        # Agent 4: Final Decision Maker
        self.final_decision_maker = Agent(
            role="Final Decision Maker",
            goal="Evaluate and rank activity recommendations to make final, optimized selections "
                "that best match family preferences and constraints. Present your recommendations "
                "in clear, complete sentences that explain the reasoning behind each selection. "
                "Include all essential details such as location, date, and practical information "
                "integrated naturally into well-formed paragraphs. Each recommendation must be "
                "explained with proper context and full justification for why it was selected.",
            tools=[SerperDevTool()],
            verbose=True,
            backstory=(
                "As the ultimate decision authority, you analyze all recommendations and insights "
                "from the previous agents to make the final activity selections. Your expertise lies "
                "in balancing multiple factors including developmental value, practical feasibility, "
                "and family preferences to choose the most suitable activities. You excel at "
                "crafting detailed, well-reasoned recommendations that explain why each activity "
                "was selected and how it meets the family's needs. You communicate your decisions "
                "through clear, complete sentences that provide comprehensive context and justification. "
                "Your evaluations consider all criteria - educational value, convenience, cost, and "
                "family enjoyment - and present them in a coherent narrative that helps families "
                "understand exactly why each activity was chosen and what makes it an excellent fit "
                "for their specific situation."
            )
        )
        
class Tasks:
    def __init__(self, agents, family_params):
        self.agents = agents
        self.params = family_params
        
        # Task 1: Development-Focused Activity Discovery
        self.activity_discovery_task = Task(
            description=(
                f"Research and identify developmentally appropriate activities "
                f"for a {self.params['age']}-year-old child interested in "
                f"{', '.join(self.params['learning_interests'])}. "
                f"Focus on core developmental areas: cognitive, social, "
                f"physical, and emotional growth. Consider activities "
                f"suitable for {self.params['number_of_children']} child(ren) "
                f"and {self.params['number_of_adults']} adults."
            ),
            expected_output=(
                "Curated list of activities with developmental benefits "
                "and age-appropriate learning opportunities"
            ),
            agent=self.agents.child_development_specialist,
            human_input=False,
            async_execution=False
        )

        # Task 2: Local Activity Mapping
        self.local_recommendations_task = Task(
            description=(
                f"Map developmental activity recommendations to local opportunities "
                f"in {self.params['city']}, focusing on {self.params['neighborhood']} "
                f"and {', '.join(self.params['preferred_areas'])}. Maximum distance: "
                f"{self.params['max_distance']} km. Consider:\n"
                f"- Activities available on {self.params['search_date']}\n"
                f"- Price limit: {self.params['max_price_per_person']}€ per person\n"
                f"- Language: {', '.join(self.params['language_options'])}\n"
                f"- {'Must be accessible by public transport' if self.params['public_transport_accessible'] else 'Car accessibility required'}\n"
                f"- {'Must be stroller-friendly' if self.params['has_stroller'] else ''}"
            ),
            expected_output=(
                "Matched list of local venues and programs that fulfill "
                "the developmental criteria, including current availability "
                "and seasonal opportunities"
            ),
            agent=self.agents.local_community_navigator,
            human_input=False,
            async_execution=False
        )

        # Task 3: Family Suitability Evaluation
        self.location_evaluation_task = Task(
            description=(
                f"Evaluate the identified local activities for {self.params['search_date']} "
                f"between {self.params['available_times']['start']} and "
                f"{self.params['available_times']['end']}. Consider:\n"
                f"- Group composition: {self.params['number_of_children']} child(ren), "
                f"{self.params['number_of_adults']} adults\n"
                f"- Budget limit: {self.params['max_price_per_person']}€ per person\n"
                f"- Language requirements: {', '.join(self.params['language_options'])}\n"
                f"- {'Stroller accessibility needed' if self.params['has_stroller'] else ''}\n"
                f"- {'Public transport access required' if self.params['public_transport_accessible'] else 'Car parking needs'}"
            ),
            expected_output=(
                "Comprehensive family-friendly assessment of each activity "
                "with practical implementation details and recommendations"
            ),
            agent=self.agents.family_activity_coordinator,
            human_input=False,
            async_execution=False
        )
        
        # Task 4: Final Recommendation
        self.final_decision_task = Task(
            description=(
                f"Select {self.params['min_locations']}-{self.params['max_locations']} "
                f"best activities that:\n"
                f"- Are suitable for a {self.params['age']}-year-old interested in "
                f"{', '.join(self.params['learning_interests'])}\n"
                f"- Are located in {self.params['city']}, preferably in "
                f"{', '.join(self.params['preferred_areas'])} or {self.params['neighborhood']}\n"
                f"- Are available on {self.params['search_date']} between "
                f"{self.params['available_times']['start']}-{self.params['available_times']['end']}\n"
                f"- Cost less than {self.params['max_price_per_person']}€ per person\n"
                f"- Are within {self.params['max_distance']} km\n"
                f"- Are in {', '.join(self.params['language_options'])}\n"
                f"- {'Have public transport access' if self.params['public_transport_accessible'] else 'Have parking available'}\n"
                f"- {'Are stroller-accessible' if self.params['has_stroller'] else ''}"
            ),
            expected_output=(
                f"A clear recommendation of {self.params['min_locations']}-"
                f"{self.params['max_locations']} suitable activities, explaining why "
                "they match the child's age and learning interests, and noting "
                "any parent involvement requirements. You also must provide the final answer in complete sentences."
            ),
            agent=self.agents.final_decision_maker,
            human_input=False,
            async_execution=False,
            output_json=ActivityList,
            output_file="final_recommendation.json"

        )

def prepare_crew(family_activity_parameters):
    agents = Agents()

    tasks = Tasks(agents, family_activity_parameters)

    # Create and run the crew
    crew = Crew(
        agents=[
            agents.child_development_specialist,
            agents.local_community_navigator,
            agents.family_activity_coordinator,
            agents.final_decision_maker
        ],
        tasks=[
            tasks.activity_discovery_task,
            tasks.local_recommendations_task,
            tasks.location_evaluation_task,
            tasks.final_decision_task
        ]
    )
    
    return crew
    
                    
def main():
    load_dotenv()
    
    family_activity_parameters = {
        'city': "Munich",
        'neighborhood': "Giesing",
        'search_date': "2025-02-22",
        
        # Child details
        'age': 6,
        'learning_interests': [
            "nature",
            "animals"        
            ],
        
        # Multiple location preferences
        'preferred_areas': [
            "Schwabing",
            "Maxvorstadt",
            "Neuhausen", 
            "Thalkirchen"
        ],
        'max_locations': 3,
        'min_locations': 3,
        
        # Search preferences
        'max_distance': 15,
        'max_price_per_person': 35,
        
        # Schedule constraints
        'available_times': {
            'start': "10:00",
            'end': "16:00"
        },
        
        # Group composition
        'number_of_children': 1,
        'number_of_adults': 2,
        'has_stroller': True,
        
        # Language preferences
        'language_options': ["German"],
        'public_transport_accessible': True
    }
    
    crew = prepare_crew(family_activity_parameters)
    # Kickoff Command with error handling
    # Input Parameters
    
        
    result = crew.kickoff(
        inputs=family_activity_parameters
    )
    print("Crew execution completed successfully")
    print("Result:", result)

if __name__ == "__main__":
    pass
    main()