# chatbot.py
import re
import json
import datetime
from typing import Dict, List, Tuple
from pathlib import Path

class RuleBasedChatbot:
    def __init__(self, name: str = "Bot"):
        self.name = name
        self.conversation_history = []
        self.knowledge_base = self._initialize_knowledge_base()
        self.patterns = self._initialize_patterns()
        
    def _initialize_knowledge_base(self) -> Dict:
        """Initialize domain-specific knowledge base"""
        return {
            "weather": {
                "what is weather": "I don't have access to real-time weather data, but you can check weather websites or apps!",
                "weather today": "For accurate weather information, please check a weather service like weather.com",
                "is it raining": "I cannot check current weather conditions. Please use a weather app or website.",
            },
            "time": {
                "current time": f"The current time is {datetime.datetime.now().strftime('%H:%M')}",
                "what time": f"It's {datetime.datetime.now().strftime('%H:%M')} right now",
                "time now": f"The time is {datetime.datetime.now().strftime('%H:%M')}",
            },
            "date": {
                "today date": f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}",
                "what date": f"It's {datetime.datetime.now().strftime('%B %d, %Y')}",
                "current date": f"The current date is {datetime.datetime.now().strftime('%B %d, %Y')}",
            },
            "greeting": {
                "hello": f"Hello! How can I help you today?",
                "hi": f"Hi there! What can I do for you?",
                "hey": f"Hey! How's it going?",
                "good morning": "Good morning! Hope you're having a great start to your day!",
                "good afternoon": "Good afternoon! How can I assist you?",
                "good evening": "Good evening! What brings you here?",
            },
            "farewell": {
                "bye": "Goodbye! Have a great day!",
                "goodbye": "See you later! Take care!",
                "see you": "See you soon! Feel free to come back anytime.",
                "exit": "Goodbye! It was nice chatting with you!",
            },
            "help": {
                "help": "I can help with greetings, small talk, and answer questions about various topics. Try asking me about weather, time, date, or just say hello!",
                "what can you do": "I'm a simple chatbot that can engage in basic conversation. I can tell you the time/date, respond to greetings, and have simple small talk.",
                "capabilities": "My capabilities include: greetings, telling time/date, basic small talk, and responding to help requests.",
            },
            "small_talk": {
                "how are you": "I'm doing well, thank you for asking! How about you?",
                "what's up": "Not much, just here to chat with you! What's on your mind?",
                "how's it going": "Going great! Thanks for asking. How can I help you today?",
                "nice to meet you": "Nice to meet you too! I hope we can have a great conversation.",
                "thank you": "You're welcome! Happy to help!",
                "thanks": "My pleasure! Is there anything else you need?",
                "who are you": f"I'm {self.name}, a simple rule-based chatbot designed to have basic conversations!",
                "what is your name": f"My name is {self.name}! What's yours?",
                "your name": f"I'm called {self.name}!",
            }
        }
    
    def _initialize_patterns(self) -> List[Tuple[str, str, str]]:
        """Initialize regex patterns for intent matching"""
        patterns = [
            # (intent, pattern, response_key)
            ("greeting", r"\b(hello|hi|hey|good morning|good afternoon|good evening)\b", "greeting"),
            ("farewell", r"\b(bye|goodbye|see you|exit)\b", "farewell"),
            ("help", r"\b(help|what can you do|capabilities)\b", "help"),
            ("time", r"\b(time|clock|what.*time)\b", "time"),
            ("date", r"\b(date|today|what.*date)\b", "date"),
            ("weather", r"\b(weather|rain|sunny|temperature|forecast)\b", "weather"),
            ("small_talk", r"\b(how are you|what's up|how's it going|nice to meet|thank|thanks|who are you|your name)\b", "small_talk"),
        ]
        return patterns
    
    def log_conversation(self, user_input: str, bot_response: str):
        """Log conversation to file"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "user": user_input,
            "bot": bot_response
        }
        
        self.conversation_history.append(log_entry)
        
        # Save to file
        log_file = Path("conversation_log.json")
        if log_file.exists():
            with open(log_file, 'r') as f:
                try:
                    history = json.load(f)
                except:
                    history = []
        else:
            history = []
        
        history.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def get_response(self, user_input: str) -> str:
        """Generate response based on user input"""
        user_input_lower = user_input.lower().strip()
        
        # Check for exact matches in knowledge base
        for category, responses in self.knowledge_base.items():
            for key, response in responses.items():
                if key in user_input_lower:
                    self.log_conversation(user_input, response)
                    return response
        
        # Check patterns for intent matching
        for intent, pattern, category in self.patterns:
            if re.search(pattern, user_input_lower):
                # Get a response from the knowledge base category
                for key, response in self.knowledge_base[category].items():
                    if re.search(key, user_input_lower):
                        self.log_conversation(user_input, response)
                        return response
                
                # If no specific key matches, return a default response from the category
                default_response = list(self.knowledge_base[category].values())[0]
                self.log_conversation(user_input, default_response)
                return default_response
        
        # Default response for unknown inputs
        default_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "Interesting! Tell me more about that.",
            "I see. Can you elaborate on that?",
            "That's beyond my current knowledge. Is there something else I can help with?",
            "I'm still learning. Could you ask me something else?"
        ]
        
        import random
        response = random.choice(default_responses)
        self.log_conversation(user_input, response)
        return response
    
    def add_to_knowledge_base(self, category: str, key: str, response: str):
        """Add new knowledge to the bot's knowledge base"""
        if category not in self.knowledge_base:
            self.knowledge_base[category] = {}
        self.knowledge_base[category][key] = response
        print(f"Added '{key}' to {category} knowledge base")
    
    def show_history(self):
        """Display conversation history"""
        if not self.conversation_history:
            print("No conversation history yet.")
            return
        
        print("\n" + "="*50)
        print("CONVERSATION HISTORY")
        print("="*50)
        for entry in self.conversation_history:
            print(f"[{entry['timestamp']}]")
            print(f"  You: {entry['user']}")
            print(f"  {self.name}: {entry['bot']}")
            print("-"*30)

def main():
    """Main interactive function"""
    print("="*60)
    print("WELCOME TO THE RULE-BASED CHATBOT")
    print("="*60)
    print("\nInitializing chatbot...")
    
    bot_name = input("Enter a name for your chatbot (default: Bot): ").strip()
    if not bot_name:
        bot_name = "Bot"
    
    chatbot = RuleBasedChatbot(bot_name)
    
    print(f"\n{chatbot.name}: Hello! I'm ready to chat with you!")
    print("(Type 'history' to see conversation history, 'add' to add knowledge, 'exit' to quit)\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'exit':
                print(f"{chatbot.name}: Goodbye! Have a great day!")
                break
            
            elif user_input.lower() == 'history':
                chatbot.show_history()
                continue
            
            elif user_input.lower() == 'add':
                print("\nAdd new knowledge to the bot:")
                category = input("Enter category (e.g., weather, time, greeting): ").strip()
                key = input("Enter key phrase (e.g., 'what is weather'): ").strip()
                response = input("Enter response: ").strip()
                chatbot.add_to_knowledge_base(category, key, response)
                print("Knowledge added successfully!\n")
                continue
            
            if user_input:
                response = chatbot.get_response(user_input)
                print(f"{chatbot.name}: {response}")
            else:
                print(f"{chatbot.name}: Please say something!")
                
        except KeyboardInterrupt:
            print(f"\n{chatbot.name}: Goodbye! Take care!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
    
    print("\nThank you for using the chatbot!")

if __name__ == "__main__":
    main()