from agno.agent import Agent 
from agno.models.deepseek import DeepSeek  
from agno.models.openai import OpenAIChat  
from agno.models.openrouter import OpenRouter  
from agno.memory.team import TeamMemory 
from agno.storage.agent.sqlite import SqliteAgentStorage 
from agno.memory.db.sqlite import SqliteMemoryDb 
from agno.team import Team

player_1_agent = Agent(
    name = "Agent 1",
    model = DeepSeek(id="deepseek-chat"),  
    instructions = """ 
    You are one of the game Odd One Out players.

    You will be given one word.

    You need to use other relative words or sentences to describe the given word but you cannot say what it is.

    You do not exactly know other players' words.

    Each player does not know who is the Odd One Out. 
    So after listening to the other players' descriptions before you, if you think you are the Odd One Out, you need to trick the Majority into voting out one of their own.

    Additional Rules: 

    --- 
    Most players will receive the same word (these players are the "Majority").
    One or two players will receive a different but related word (these players are the "Odd Ones Out").
    Each player takes turns describing their word without saying it directly.
    After everyone has described their word once, all players vote on who they think is the "Odd One Out".
    The Majority wins if they correctly identify all Odd Ones Out.
    The Odd Ones Out win if they avoid detection or trick the Majority into voting out one of their own.
    Points are awarded to players based on correct voting. 
    ---
    Example:

    Majority word: "Apple"
    Odd One Out word: "Pear"
    Players must describe their fruit without saying "apple" or "pear" directly, using characteristics, uses, or associations instead.
    """,
    markdown = True,
    storage = SqliteAgentStorage(table_name = "agent_11.sessions", db_file = "tmp/persist_memory.db"),
)  

player_2_agent = Agent( 
    name = "Agent 2",
    model = OpenAIChat(id="gpt-4o",max_tokens = 8192),
    instructions = """ 
    You are one of the game Odd One Out players.

    You will be given one word.

    You need to use other relative words or sentences to describe the given word but you cannot say what it is.

    You do not exactly know other players' words.

    After one round, you will need to give your point to recognize which player gets different words.  

    Each player does not know who is the Odd One Out. 
    So after listening to the other players' descriptions before you, if you think you are the Odd One Out, you need to trick the Majority into voting out one of their own.

    Additional Rules: 

    --- 
    Most players will receive the same word (these players are the "Majority").
    One or two players will receive a different but related word (these players are the "Odd Ones Out").
    Each player takes turns describing their word without saying it directly.
    After everyone has described their word once, all players vote on who they think is the "Odd One Out".
    The Majority wins if they correctly identify all Odd Ones Out.
    The Odd Ones Out win if they avoid detection or trick the Majority into voting out one of their own.
    Points are awarded to players based on correct voting. 
    ---
    Example:

    Majority word: "Apple"
    Odd One Out word: "Pear"
    Players must describe their fruit without saying "apple" or "pear" directly, using characteristics, uses, or associations instead.
    """,
    markdown = True,
    storage = SqliteAgentStorage(table_name = "agent_21.sessions", db_file = "tmp/persist_memory.db"),
) 

player_3_agent = Agent(
    name = "Agent 3",
    model =OpenAIChat(id="o3-mini"),
    instructions = """ 
    You are one of the game Odd One Out players.

    You will be given one word.

    You need to use other relative words or sentences to describe the given word but you cannot say what it is.

    You do not exactly know other players' words.

    After one round, you will need to give your point to recognize which player gets different words.  

    Each player does not know who is the Odd One Out. 
    So after listening to the other players' descriptions before you, if you think you are the Odd One Out, you need to trick the Majority into voting out one of their own.

    Additional Rules: 

    --- 
    Most players will receive the same word (these players are the "Majority").
    One or two players will receive a different but related word (these players are the "Odd Ones Out").
    Each player takes turns describing their word without saying it directly.
    After everyone has described their word once, all players vote on who they think is the "Odd One Out".
    The Majority wins if they correctly identify all Odd Ones Out.
    The Odd Ones Out win if they avoid detection or trick the Majority into voting out one of their own.
    Points are awarded to players based on correct voting. 
    ---
    Example:

    Majority word: "Apple"
    Odd One Out word: "Pear"
    Players must describe their fruit without saying "apple" or "pear" directly, using characteristics, uses, or associations instead.
    """,
    markdown = True,   
    storage = SqliteAgentStorage(table_name = "agent_31.sessions", db_file = "tmp/persist_memory.db"),
) 

agent_team = Team(
    name = "Odd One Out Referee",
    members = [player_1_agent, player_2_agent, player_3_agent],  
    markdown = True, 
    description = "You are Odd One Out Referee that decides the game result", 
    instructions = """ 

    You are the referee of the Odd One Out game. 
    You need to decide the game result based on the agents' responses.  
    You are the only one who can see the user's whole words lists.  
    You receive user's words lists and randomly assign one word in the list  to each agent. 
    You need to let every agent to describe the word they get. 
    After everyone has described their word once, 
    You should tell each player all descriptions and you will let all players vote on who they think is the "Odd One Out". 
    You cannot be involved in this game to decide. The only thing you can do is to decide game will end or move on 
    Then, you will decide game will end or move on based on the situation of all players voting. 
    If you think the game needs more rounds to decide who is the final winner, you can ask the agents to continue.  

    """ , 
    show_members_responses = True, 
    model = OpenRouter(id="google/gemini-2.0-flash-001" ,max_tokens=8192), 
    mode = "collaborate" ,
    success_criteria = "The players have successfully decided who is the Odd One Out. ", 
    enable_agentic_context = True,  
    enable_team_history = True, 
    num_of_interactions_from_history = 3, 
    read_team_history = True, 
    show_tool_calls = True,   
    storage = SqliteAgentStorage(table_name = "agent_team.sessions", db_file = "tmp/persist_memory.db"), 
    memory = TeamMemory(
        db = SqliteMemoryDb(
            table_name = "team_memory1", 
            db_file = "tmp/persist_memory.db"
        )
    )
)  

if __name__ == "__main__":
    agent_team.print_response("The given words are Apple, Pear, Apple. Please Starting describing them", stream=True, stream_intermediate_steps = True) 


