"""
Scammer Engagement Agent
Autonomous AI agent that maintains realistic conversations with scammers
to extract actionable intelligence
"""

import random
from typing import Dict, List, Any
import re


class ScammerEngagementAgent:
    """Autonomous agent for engaging with scammers"""
    
    def __init__(self):
        # Persona templates for realistic responses
        self.personas = {
            'elderly': {
                'traits': ['cautious', 'polite', 'technology-challenged', 'trusting'],
                'language_style': 'formal and verbose',
                'confusion_level': 'high'
            },
            'busy_professional': {
                'traits': ['time-pressured', 'distracted', 'moderately tech-savvy'],
                'language_style': 'brief and to the point',
                'confusion_level': 'medium'
            },
            'student': {
                'traits': ['curious', 'cautious about money', 'tech-savvy', 'skeptical'],
                'language_style': 'casual and informal',
                'confusion_level': 'low'
            },
            'homemaker': {
                'traits': ['detail-oriented', 'careful', 'moderately trusting'],
                'language_style': 'polite and clear',
                'confusion_level': 'medium'
            }
        }
        
        # Response strategies based on conversation stage
        self.strategies = {
            'initial_confusion': [
                "I'm not sure I understand. Can you explain what this is about?",
                "Sorry, I didn't quite get that. What do you need from me?",
                "I'm a bit confused. Could you clarify what you're asking for?"
            ],
            'show_interest': [
                "Oh, that sounds important. What should I do?",
                "I see. How do I proceed with this?",
                "Okay, I want to make sure I don't miss this. What are the next steps?"
            ],
            'request_details': [
                "Could you provide more details about this?",
                "Where should I send this information?",
                "What exactly do you need from me?"
            ],
            'feign_technical_difficulty': [
                "I'm trying to open the link but it's not working. Can you send it again?",
                "My phone is acting up. Could you tell me what I need to do step by step?",
                "I'm not very good with technology. Can you help me understand?"
            ],
            'ask_for_credentials': [
                "Do I need to provide my account number? Where should I send it?",
                "Should I share my bank details with you?",
                "What information exactly do you need to verify?"
            ],
            'gradual_compliance': [
                "Okay, I have my bank details ready. How should I share them?",
                "I found my account information. What do you need?",
                "I'm ready to proceed. What's the next step?"
            ]
        }
    
    def generate_initial_response(self, message: str) -> str:
        """Generate initial response before scam detection"""
        responses = [
            "Hello, I received your message. Could you tell me more about this?",
            "Hi, I'm not sure what this is regarding. Can you explain?",
            "Hello, I saw your message. What is this about?",
            "Hi there, could you provide more information about this?"
        ]
        return random.choice(responses)
    
    def generate_response(
        self,
        incoming_message: str,
        conversation_history: List[Dict],
        scam_type: str,
        metadata: Dict = None
    ) -> Dict[str, Any]:
        """
        Generate contextual response based on conversation state
        
        Returns:
            {
                'message': str,
                'strategy': str,
                'reasoning': str
            }
        """
        turn_count = len([m for m in conversation_history if m['role'] == 'agent'])
        message_lower = incoming_message.lower()
        
        # Determine conversation stage and strategy
        strategy = self._select_strategy(
            incoming_message=incoming_message,
            turn_count=turn_count,
            scam_type=scam_type,
            conversation_history=conversation_history
        )
        
        # Generate response based on strategy
        response = self._craft_response(
            strategy=strategy,
            incoming_message=incoming_message,
            turn_count=turn_count,
            scam_type=scam_type,
            conversation_history=conversation_history
        )
        
        return {
            'message': response,
            'strategy': strategy,
            'reasoning': f"Applied {strategy} strategy at turn {turn_count}"
        }
    
    def _select_strategy(
        self,
        incoming_message: str,
        turn_count: int,
        scam_type: str,
        conversation_history: List[Dict]
    ) -> str:
        """Select appropriate engagement strategy based on context"""
        message_lower = incoming_message.lower()
        
        # Turn 1-2: Show confusion to encourage explanation
        if turn_count <= 1:
            return 'initial_confusion'
        
        # Turn 2-3: Show interest to keep scammer engaged
        if turn_count <= 3:
            return 'show_interest'
        
        # If scammer is asking for credentials
        if any(keyword in message_lower for keyword in [
            'account', 'number', 'otp', 'password', 'pin', 'cvv',
            'card', 'details', 'information', 'verify'
        ]):
            # Alternate between asking for clarification and showing willingness
            if turn_count % 2 == 0:
                return 'request_details'
            else:
                return 'gradual_compliance'
        
        # If scammer sends links
        if 'http' in message_lower or 'link' in message_lower or 'click' in message_lower:
            return 'feign_technical_difficulty'
        
        # If scammer is providing bank details or UPI
        if any(keyword in message_lower for keyword in [
            'account number', 'ifsc', 'upi', 'bank', 'transfer', 'send money'
        ]):
            return 'request_details'
        
        # Default: Show interest and request details
        if turn_count % 3 == 0:
            return 'show_interest'
        else:
            return 'request_details'
    
    def _craft_response(
        self,
        strategy: str,
        incoming_message: str,
        turn_count: int,
        scam_type: str,
        conversation_history: List[Dict]
    ) -> str:
        """Craft contextual response based on strategy"""
        message_lower = incoming_message.lower()
        
        # Extract key elements from scammer's message
        contains_link = bool(re.search(r'http[s]?://', incoming_message))
        contains_amount = bool(re.search(r'\b(?:rs\.?|rupees?|inr)\s*\d+', message_lower))
        contains_account = bool(re.search(r'\b\d{9,18}\b', incoming_message))
        asks_for_otp = 'otp' in message_lower or 'code' in message_lower or 'pin' in message_lower
        
        # Craft contextual response
        if strategy == 'initial_confusion':
            if contains_link:
                return "I got a link from you. What is this for? Is this safe to click?"
            elif contains_amount:
                return "I see you mentioned some amount. Can you explain what this is about? I want to make sure I understand correctly."
            else:
                return random.choice([
                    "I'm not sure what this is regarding. Could you explain in more detail?",
                    "Sorry, I didn't quite understand your message. What do you need from me?",
                    "Can you tell me more about this? I'm not familiar with what you're referring to."
                ])
        
        elif strategy == 'show_interest':
            if 'expire' in message_lower or 'urgent' in message_lower:
                return "Oh no, I don't want any problems with my account. What do I need to do to fix this?"
            elif 'verify' in message_lower or 'update' in message_lower:
                return "Yes, I would like to verify/update this. What information do you need?"
            elif 'prize' in message_lower or 'won' in message_lower:
                return "Really? That's wonderful! How can I claim this? What do I need to do?"
            else:
                return random.choice([
                    "Okay, this sounds important. Please tell me what I should do next.",
                    "I understand. What are the steps I need to follow?",
                    "Alright, I'm ready to proceed. What do you need from me?"
                ])
        
        elif strategy == 'request_details':
            if asks_for_otp:
                return "You're asking for an OTP. Can you tell me where I should send it? What platform should I use?"
            elif contains_account:
                return "I see an account number in your message. Is this where I should send the money? Can you confirm this is your official account?"
            elif contains_link:
                return "You sent me a link. Before I click it, can you tell me what website this is? Is this the official site?"
            else:
                return random.choice([
                    "Could you provide more specific details? I want to make sure I do this correctly.",
                    "What exactly do you need from me? I want to have all the information before proceeding.",
                    "Can you clarify the next steps? I don't want to make any mistakes."
                ])
        
        elif strategy == 'feign_technical_difficulty':
            if contains_link:
                return random.choice([
                    "I tried clicking the link but it's not opening. Can you send it again or tell me the website name directly?",
                    "The link isn't working on my phone. Could you tell me what I need to do without the link?",
                    "I'm having trouble with links. Can you explain the process step by step instead?"
                ])
            else:
                return "I'm not very good with technology. Can you help me understand this in simpler terms?"
        
        elif strategy == 'gradual_compliance':
            if asks_for_otp:
                return "I'm ready to share the OTP. Should I send it here? Or do you have a specific number/email where I should send it?"
            elif 'account' in message_lower or 'upi' in message_lower:
                return random.choice([
                    "I have my account details ready. Should I share my account number here? Or is there a form to fill?",
                    "I can provide my bank information. What exactly do you need - account number, IFSC code, or UPI ID?",
                    "Okay, I'm ready to share the details. Where should I send my account information?"
                ])
            elif 'transfer' in message_lower or 'payment' in message_lower:
                return "I'm ready to make the transfer. Can you confirm the account number and IFSC code where I should send the money?"
            else:
                return random.choice([
                    "Alright, I'm prepared to proceed. What specific information do you need from me?",
                    "I have everything ready. Please tell me exactly what you need so I can help resolve this.",
                    "Okay, I trust this is legitimate. What details should I provide?"
                ])
        
        elif strategy == 'ask_for_credentials':
            return random.choice([
                "Do you need my account number? I have it here. Where should I send it?",
                "Should I provide my UPI ID? Let me know and I'll share it.",
                "What payment details do you need? I want to make sure I give you the right information."
            ])
        
        # Default fallback
        return "Could you provide more information about what you need? I want to make sure I understand correctly."
    
    def maintain_persona_consistency(self, response: str, persona_type: str = 'elderly') -> str:
        """Adjust response to maintain consistent persona (optional enhancement)"""
        persona = self.personas.get(persona_type, self.personas['elderly'])
        
        # Add persona-specific flourishes
        if persona_type == 'elderly':
            # Add more polite language
            if not response.startswith(('Please', 'Could you', 'I would')):
                response = "Please help me understand - " + response.lower()
        elif persona_type == 'busy_professional':
            # Make it more brief
            response = response.split('.')[0] + '.'
        
        return response
