# Odd One Out - AI Agent Game

## Overview

"Odd One Out" is a team-based word game implemented using AI agents through the Agno framework. The game features three AI agent players and a referee agent that manages the game flow and determines the results.

## Game Rules

1. **Setup**:
   - Most players receive the same word (these players are the "Majority")
   - One or two players receive a different but related word (these players are the "Odd Ones Out")
   - Each player is unaware of which word other players have received

2. **Gameplay**:
   - Each player takes turns describing their word without saying it directly
   - Players must use related words, characteristics, or associations to describe their word
   - After everyone has described their word once, all players vote on who they think is the "Odd One Out"

3. **Winning Conditions**:
   - The Majority wins if they correctly identify all Odd Ones Out
   - The Odd Ones Out win if they avoid detection or trick the Majority into voting out one of their own
   - Points are awarded to players based on correct voting

## Example

- Majority word: "Apple"
- Odd One Out word: "Pear"
- Players must describe their fruit without saying "apple" or "pear" directly, using characteristics, uses, or associations instead

## Technical Implementation

The game is implemented using the Agno framework with the following components:

### Agents

1. **Player Agents (3)**:
   - Each player agent is initialized with different AI models (DeepSeek, OpenAI GPT-4o, OpenAI o3-mini)
   - Players are given instructions on how to play the game
   - Each player has persistent memory using SQLite storage

2. **Referee Agent**:
   - Manages the game flow and determines results
   - Assigns words to players
   - Collects descriptions and votes
   - Decides when the game ends
   - Uses OpenRouter (Google Gemini) as its model

### Game Flow

1. The referee receives a list of words from the user
2. The referee randomly assigns words to each player
3. Each player describes their word without saying it directly
4. After all descriptions, players vote on who they think is the Odd One Out
5. The referee determines the result based on votes
6. The game may continue for multiple rounds if needed

## Current Limitations and Planned Improvements

- **Strategic Voting**: Currently, agents who are the Odd One Out may not effectively hide themselves when voting
- **Game Balance**: Adjusting difficulty based on word similarity
- **Multi-round Strategy**: Improving agent memory to develop strategies across multiple rounds
- **Dynamic Team Sizes**: Supporting variable numbers of players
- **User Interface**: Developing a more interactive interface for human players to join

## Usage

To run the game:

```python
python test_agno_.py
```

This will start a game with the words "Apple, Pear, Apple" where two players have "Apple" and one player has "Pear".

## Dependencies

- Agno framework
- Various AI models (DeepSeek, OpenAI, OpenRouter, etc.)
- SQLite for agent memory storage
