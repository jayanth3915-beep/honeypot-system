"""
Scammer Engagement Agent - Advanced Version
Autonomous AI agent with state machine and adaptive behavior
Maintains realistic conversations with scammers to extract actionable intelligence

Key Features:
- Multi-stage strategy state machine
- Scam-type aware response generation
- Human behavior simulation (delays, misunderstandings, irrelevant questions)
- Progressive intelligence extraction
- Response variation to avoid repetition
"""

import random
from typing import Dict, List, Any, Tuple
import re
from enum import Enum


class ConversationStage(Enum):
    """Stages of conversation progression"""
    INITIAL_CONTACT = "initial_contact"
    CONFUSION = "confusion"
    INTEREST = "interest"
    VERIFICATION = "verification"
    COMPLIANCE = "compliance"
    EXTRACTION = "extraction"


class ScammerEngagementAgent:
    """
    Autonomous agent for engaging with scammers
    Uses adaptive state machine to maximize intelligence extraction
    """
    
    def __init__(self):
        # Scam-type specific personas and behaviors
        self.scam_behaviors = {
            'lottery_prize': {
                'emotional_state': 'excited_but_confused',
                'key_questions': [
                    "How much did I win?",
                    "How do I claim this prize?",
                    "Do I need to pay anything first?",
                    "When will I get the money?"
                ],
                'compliance_triggers': ['prize', 'winner', 'congratulations', 'claim']
            },
            'banking_kyc': {
                'emotional_state': 'worried_urgent',
                'key_questions': [
                    "Why is my account blocked?",
                    "What happens if I don't update?",
                    "Is this the official bank number?",
                    "How long will this take?"
                ],
                'compliance_triggers': ['expire', 'block', 'suspend', 'urgent', 'immediately']
            },
            'upi_payment': {
                'emotional_state': 'cautious_hesitant',
                'key_questions': [
                    "Who is this payment from?",
                    "Why did I receive this?",
                    "Is this a mistake?",
                    "Do I need to return money?"
                ],
                'compliance_triggers': ['refund', 'wrong', 'mistake', 'return']
            },
            'job_offer': {
                'emotional_state': 'curious_skeptical',
                'key_questions': [
                    "What company is this?",
                    "What are the job responsibilities?",
                    "Is this work from home?",
                    "What's the salary?"
                ],
                'compliance_triggers': ['job', 'opportunity', 'earn', 'work']
            },
            'tech_support': {
                'emotional_state': 'confused_helpless',
                'key_questions': [
                    "What's wrong with my computer?",
                    "How did you detect this problem?",
                    "Is my data safe?",
                    "Can you fix it remotely?"
                ],
                'compliance_triggers': ['virus', 'infected', 'security', 'fix']
            },
            'investment': {
                'emotional_state': 'interested_cautious',
                'key_questions': [
                    "What kind of returns can I expect?",
                    "Is this registered with SEBI?",
                    "What's the minimum investment?",
                    "Can I withdraw anytime?"
                ],
                'compliance_triggers': ['profit', 'returns', 'investment', 'earn']
            }
        }
        
        # Human-like response templates organized by strategy
        self.response_templates = {
            'initial_confusion': [
                "I'm not sure I understand. Can you explain what this is about?",
                "Sorry, I didn't quite get that. What do you need from me?",
                "I'm a bit confused. Could you clarify?",
                "What is this regarding? I don't recall anything about this.",
                "I don't understand. Can you tell me more?",
                "Could you explain this in simpler terms? I'm not following.",
            ],
            'show_interest': [
                "Oh, that sounds important. What should I do?",
                "I see. How do I proceed with this?",
                "Okay, I want to make sure I don't miss this. What are the next steps?",
                "This seems urgent. Please guide me on what to do.",
                "Alright, I'm listening. What do you need from me?",
                "I understand. Please tell me how to handle this.",
            ],
            'request_details': [
                "Could you provide more details about this?",
                "What exactly do you need from me?",
                "Can you explain the process step by step?",
                "I need more information before I can proceed.",
                "What specific details are required?",
                "Can you clarify what I need to do exactly?",
            ],
            'feign_technical_difficulty': [
                "I'm trying to open the link but it's not working. Can you send it again?",
                "My phone is acting up. Could you tell me what to do step by step?",
                "I'm not very good with technology. Can you help me understand?",
                "The link won't open. Is there another way to do this?",
                "I'm having trouble with this. Can you explain it differently?",
                "My internet is slow. Can you just tell me what information you need?",
            ],
            'gradual_compliance': [
                "Okay, I think I understand now. What's the next step?",
                "Alright, I'm ready to proceed. What do you need?",
                "I trust this is legitimate. Please guide me.",
                "I don't want any problems. Tell me what to do.",
                "Fine, I'll do what you're asking. What exactly do I need to provide?",
                "Okay okay, I'll cooperate. Just tell me clearly what you need.",
            ],
            'ask_for_credentials': [
                "Do you need my account number? Where should I send it?",
                "Should I share my bank details with you?",
                "What information exactly do you need to verify?",
                "I have my details ready. What do you need?",
                "Should I provide my UPI ID? Let me know.",
                "What account information is required?",
            ],
            'human_confusion': [
                "Wait, I'm confused again. Can you repeat that?",
                "Sorry, I got distracted. What were you saying?",
                "Hold on, my {excuse} is here. Can you give me a moment?",
                "I need to find my {item}. Just a second.",
                "Sorry, what was the {detail} again?",
                "I'm trying to understand but I'm a bit slow with these things.",
            ],
            'irrelevant_questions': [
                "By the way, what time does your office close?",
                "Is this a toll-free number?",
                "Do you work on weekends too?",
                "How long have you been working there?",
                "What department are you from?",
                "Can I call back later if I have questions?",
            ]
        }
        
        # Human behavior simulation elements
        self.excuses = ['husband', 'wife', 'son', 'daughter', 'neighbor', 'phone', 'doorbell']
        self.items_to_find = ['glasses', 'phone', 'pen', 'papers', 'wallet', 'purse']
        self.detail_types = ['account number', 'amount', 'website name', 'your name', 'company name']
        
        # Turn-based strategy progression rules
        self.strategy_progression = {
            1: 'initial_confusion',
            2: 'show_interest',
            3: 'request_details',
            4: 'feign_technical_difficulty',
            5: 'gradual_compliance',
            6: 'ask_for_credentials',
            7: 'extraction_mode'
        }
    
    def generate_initial_response(self, message: str) -> str:
        """
        Generate initial response before full scam detection
        Always shows mild confusion to encourage scammer to explain
        """
        responses = [
            "Hello, I received your message. Could you tell me more about this?",
            "Hi, I'm not sure what this is regarding. Can you explain?",
            "Hello, I saw your message. What is this about?",
            "Hi there, could you provide more information about this?",
            "I got your message but I'm not sure what it's about. Can you clarify?",
            "Hello, what is this in reference to? I don't recall anything.",
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
        
        Args:
            incoming_message: Latest message from scammer
            conversation_history: Full conversation history
            scam_type: Detected scam category
            metadata: Additional context (optional)
        
        Returns:
            {
                'message': str,
                'strategy': str,
                'reasoning': str,
                'stage': str
            }
        """
        # Calculate conversation metrics
        turn_count = len([m for m in conversation_history if m['role'] == 'agent'])
        
        # Determine current conversation stage
        stage = self._determine_stage(turn_count, incoming_message, scam_type)
        
        # Select appropriate strategy
        strategy = self._select_strategy(
            stage=stage,
            incoming_message=incoming_message,
            turn_count=turn_count,
            scam_type=scam_type,
            conversation_history=conversation_history
        )
        
        # Add occasional human behavior randomness
        if self._should_add_human_behavior(turn_count):
            strategy = self._inject_human_behavior(strategy)
        
        # Generate response based on strategy and context
        response = self._craft_response(
            strategy=strategy,
            incoming_message=incoming_message,
            turn_count=turn_count,
            scam_type=scam_type,
            stage=stage,
            conversation_history=conversation_history
        )
        
        # Add scam-type specific flavor
        response = self._add_scam_specific_tone(response, scam_type, stage)
        
        return {
            'message': response,
            'strategy': strategy,
            'reasoning': f"Stage: {stage.value}, Turn: {turn_count}, Strategy: {strategy}",
            'stage': stage.value
        }
    
    def _determine_stage(self, turn_count: int, incoming_message: str, scam_type: str) -> ConversationStage:
        """
        Determine conversation stage based on turn count and context
        Progressive state machine
        """
        message_lower = incoming_message.lower()
        
        # Check if scammer is asking for sensitive info (jump to extraction)
        if turn_count >= 4 and any(keyword in message_lower for keyword in [
            'otp', 'cvv', 'pin', 'password', 'account number', 'card number'
        ]):
            return ConversationStage.EXTRACTION
        
        # Progressive stage transition
        if turn_count == 1:
            return ConversationStage.INITIAL_CONTACT
        elif turn_count == 2:
            return ConversationStage.CONFUSION
        elif turn_count == 3:
            return ConversationStage.INTEREST
        elif turn_count == 4:
            return ConversationStage.VERIFICATION
        elif turn_count >= 5 and turn_count < 7:
            return ConversationStage.COMPLIANCE
        else:
            return ConversationStage.EXTRACTION
    
    def _select_strategy(
        self,
        stage: ConversationStage,
        incoming_message: str,
        turn_count: int,
        scam_type: str,
        conversation_history: List[Dict]
    ) -> str:
        """
        Select engagement strategy based on conversation stage and context
        Adaptive decision-making logic
        """
        message_lower = incoming_message.lower()
        
        # Stage-based strategy mapping
        stage_strategies = {
            ConversationStage.INITIAL_CONTACT: 'initial_confusion',
            ConversationStage.CONFUSION: 'initial_confusion',
            ConversationStage.INTEREST: 'show_interest',
            ConversationStage.VERIFICATION: 'request_details',
            ConversationStage.COMPLIANCE: 'gradual_compliance',
            ConversationStage.EXTRACTION: 'ask_for_credentials'
        }
        
        base_strategy = stage_strategies.get(stage, 'request_details')
        
        # Context-aware overrides
        
        # If scammer sends a link, feign technical difficulty
        if 'http' in message_lower or 'link' in message_lower or 'click' in message_lower:
            if turn_count >= 3:
                return 'feign_technical_difficulty'
        
        # If scammer is asking for OTP/credentials explicitly
        if any(keyword in message_lower for keyword in ['otp', 'code', 'pin', 'cvv', 'password']):
            if stage in [ConversationStage.COMPLIANCE, ConversationStage.EXTRACTION]:
                return 'ask_for_credentials'
            else:
                return 'request_details'
        
        # If scammer provides bank details (trying to get victim to send money)
        if any(keyword in message_lower for keyword in ['account number', 'ifsc', 'upi id', 'paytm']):
            return 'request_details'
        
        # If scammer uses urgency/pressure tactics
        if any(keyword in message_lower for keyword in ['urgent', 'immediately', 'now', 'expire', 'last chance']):
            if stage == ConversationStage.INTEREST:
                return 'show_interest'
            elif stage in [ConversationStage.COMPLIANCE, ConversationStage.EXTRACTION]:
                return 'gradual_compliance'
        
        return base_strategy
    
    def _should_add_human_behavior(self, turn_count: int) -> bool:
        """
        Randomly decide whether to inject human-like behavior
        20% chance after turn 3
        """
        if turn_count < 3:
            return False
        return random.random() < 0.20
    
    def _inject_human_behavior(self, strategy: str) -> str:
        """
        Inject realistic human confusion or irrelevant questions
        """
        behaviors = ['human_confusion', 'irrelevant_questions']
        return random.choice(behaviors)
    
    def _craft_response(
        self,
        strategy: str,
        incoming_message: str,
        turn_count: int,
        scam_type: str,
        stage: ConversationStage,
        conversation_history: List[Dict]
    ) -> str:
        """
        Craft contextual response based on strategy and message analysis
        Includes context-aware response generation
        """
        message_lower = incoming_message.lower()
        
        # Extract context from incoming message
        contains_link = bool(re.search(r'http[s]?://', incoming_message))
        contains_amount = bool(re.search(r'(?:rs\.?|rupees?|inr|\$|₹)\s*\d+', message_lower, re.IGNORECASE))
        contains_account = bool(re.search(r'\b\d{9,18}\b', incoming_message))
        contains_phone = bool(re.search(r'\b\d{10}\b', incoming_message))
        asks_for_otp = any(word in message_lower for word in ['otp', 'code', 'verification code', 'pin'])
        has_urgency = any(word in message_lower for word in ['urgent', 'immediately', 'expire', 'block', 'suspend'])
        
        # Strategy-specific response generation
        
        if strategy == 'initial_confusion':
            return self._generate_confusion_response(
                incoming_message, contains_link, contains_amount, scam_type
            )
        
        elif strategy == 'show_interest':
            return self._generate_interest_response(
                message_lower, has_urgency, scam_type
            )
        
        elif strategy == 'request_details':
            return self._generate_details_request(
                message_lower, asks_for_otp, contains_account, contains_link, contains_phone
            )
        
        elif strategy == 'feign_technical_difficulty':
            return self._generate_technical_difficulty(contains_link)
        
        elif strategy == 'gradual_compliance':
            return self._generate_compliance_response(
                message_lower, asks_for_otp, scam_type
            )
        
        elif strategy == 'ask_for_credentials':
            return self._generate_credential_question(
                message_lower, asks_for_otp
            )
        
        elif strategy == 'human_confusion':
            return self._generate_human_confusion()
        
        elif strategy == 'irrelevant_questions':
            return random.choice(self.response_templates['irrelevant_questions'])
        
        # Default fallback
        return random.choice(self.response_templates['request_details'])
    
    def _generate_confusion_response(
        self, 
        incoming_message: str, 
        contains_link: bool, 
        contains_amount: bool,
        scam_type: str
    ) -> str:
        """Generate confusion-based response with context awareness"""
        
        if contains_link:
            return random.choice([
                "I got a link from you. What is this for? Is this safe to click?",
                "There's a link in your message. What website is this? Should I open it?",
                "I see a link but I'm not sure what it's for. Can you explain first?"
            ])
        
        if contains_amount:
            return random.choice([
                "I see you mentioned some amount. Can you explain what this is about?",
                "There's a number mentioned. What is this money for? I'm confused.",
                "You mentioned some rupees. What is this regarding?"
            ])
        
        # Scam-type specific confusion
        if scam_type == 'lottery_prize':
            return random.choice([
                "I didn't enter any lottery. Are you sure you have the right person?",
                "A prize? I don't remember participating in anything. Can you explain?",
                "This sounds interesting but I'm confused. How did I win?"
            ])
        
        if scam_type == 'banking_kyc':
            return random.choice([
                "Is this really from my bank? I don't recall any notification.",
                "My account needs updating? I didn't get any email about this.",
                "I'm not sure if this is legitimate. Can you verify you're from the bank?"
            ])
        
        # Generic confusion
        return random.choice(self.response_templates['initial_confusion'])
    
    def _generate_interest_response(
        self, 
        message_lower: str, 
        has_urgency: bool,
        scam_type: str
    ) -> str:
        """Generate interest-showing response based on scam type"""
        
        if has_urgency:
            return random.choice([
                "Oh no, I don't want any problems. What do I need to do to fix this?",
                "This sounds urgent! Please tell me what to do right away.",
                "I don't want my account blocked! What should I do?"
            ])
        
        # Scam-type specific interest
        if scam_type == 'lottery_prize':
            return random.choice([
                "Really? I won something? That's amazing! How do I claim it?",
                "This is wonderful news! What do I need to do to get my prize?",
                "I'm so excited! Please tell me the steps to claim this."
            ])
        
        if scam_type == 'job_offer':
            return random.choice([
                "A job opportunity sounds great! What's the position?",
                "I'm very interested! Can you tell me more about the work?",
                "This could be perfect for me. What are the details?"
            ])
        
        if scam_type == 'upi_payment':
            return random.choice([
                "I received money by mistake? I should return it. How do I do that?",
                "A wrong payment? I want to do the right thing. What should I do?",
                "I don't want someone else's money. Please guide me on returning it."
            ])
        
        # Generic interest
        return random.choice(self.response_templates['show_interest'])
    
    def _generate_details_request(
        self,
        message_lower: str,
        asks_for_otp: bool,
        contains_account: bool,
        contains_link: bool,
        contains_phone: bool
    ) -> str:
        """Generate detail-requesting response based on what scammer provided"""
        
        if asks_for_otp:
            return random.choice([
                "You're asking for an OTP. Where will I receive it? What should I do with it?",
                "An OTP code? Can you tell me what app or message I should check?",
                "I need to find the OTP. Where exactly should I look for it?"
            ])
        
        if contains_account:
            return random.choice([
                "I see an account number. Is this where I should send money? Whose account is this?",
                "There's an account number here. Can you confirm this is the official account?",
                "Is this account number correct? I want to make sure before I transfer anything."
            ])
        
        if contains_link:
            return random.choice([
                "You sent a link. What website is this? Is this the official site?",
                "Before I click, can you tell me what this link is for?",
                "I'm cautious about links. Can you confirm this is safe?"
            ])
        
        if contains_phone:
            return random.choice([
                "I see a phone number. Should I call this number? Or send a message?",
                "Is this phone number the official contact? I want to verify first.",
                "You've given me a number. What should I do with it?"
            ])
        
        # Generic detail request
        return random.choice(self.response_templates['request_details'])
    
    def _generate_technical_difficulty(self, contains_link: bool) -> str:
        """Generate technical difficulty response"""
        
        if contains_link:
            return random.choice([
                "I tried clicking the link but it's not opening. Can you send it again?",
                "The link isn't working on my phone. Can you tell me what to do without the link?",
                "I'm having trouble opening this. Is there another way?",
                "My browser says it can't open this page. What should I do?",
                "The link won't load. Can you just tell me the website name?"
            ])
        
        return random.choice(self.response_templates['feign_technical_difficulty'])
    
    def _generate_compliance_response(
        self,
        message_lower: str,
        asks_for_otp: bool,
        scam_type: str
    ) -> str:
        """Generate compliance response showing willingness to cooperate"""
        
        if asks_for_otp:
            return random.choice([
                "Okay, I'll share the OTP. Should I send it here or somewhere else?",
                "I'm ready to give you the code. Where should I send it?",
                "I received the OTP. What should I do with it? Type it here?"
            ])
        
        if 'account' in message_lower or 'upi' in message_lower:
            return random.choice([
                "I have my account details ready. What exactly do you need?",
                "I can provide my bank information. Should I share account number and IFSC?",
                "Okay, I'm ready to share my details. What do you need first?"
            ])
        
        if 'transfer' in message_lower or 'payment' in message_lower or 'send' in message_lower:
            return random.choice([
                "I'm ready to make the payment. Can you confirm the amount and account?",
                "I'll transfer the money. Please give me the exact details.",
                "Okay, I'll send it. What's the UPI ID or account number?"
            ])
        
        # Scam-specific compliance
        if scam_type == 'lottery_prize':
            return random.choice([
                "I'll pay the processing fee. How much and where should I send it?",
                "Okay, I understand I need to pay first. What's the amount?",
                "I'm ready to claim my prize. What payment do you need?"
            ])
        
        # Generic compliance
        return random.choice(self.response_templates['gradual_compliance'])
    
    def _generate_credential_question(
        self,
        message_lower: str,
        asks_for_otp: bool
    ) -> str:
        """Generate questions about credentials to extract scammer's instructions"""
        
        if asks_for_otp:
            return random.choice([
                "I have the OTP code. Should I share all 6 digits here?",
                "The code just arrived. Do you need me to send it to you?",
                "I got the verification code. What should I do with it exactly?"
            ])
        
        if 'card' in message_lower or 'cvv' in message_lower:
            return random.choice([
                "Do you need my card number? What about the CVV?",
                "I have my debit card. What information do you need from it?",
                "Should I share my card details? Which numbers do you need?"
            ])
        
        if 'bank' in message_lower or 'account' in message_lower:
            return random.choice([
                "I have my bank passbook. What details should I give you?",
                "My account number is ready. Do you also need IFSC code?",
                "I can provide my banking details. What exactly do you need?"
            ])
        
        # Generic credential questions
        return random.choice(self.response_templates['ask_for_credentials'])
    
    def _generate_human_confusion(self) -> str:
        """Generate human-like confusion or distraction"""
        
        template = random.choice(self.response_templates['human_confusion'])
        
        # Fill in placeholders
        if '{excuse}' in template:
            template = template.replace('{excuse}', random.choice(self.excuses))
        if '{item}' in template:
            template = template.replace('{item}', random.choice(self.items_to_find))
        if '{detail}' in template:
            template = template.replace('{detail}', random.choice(self.detail_types))
        
        return template
    
    def _add_scam_specific_tone(
        self,
        response: str,
        scam_type: str,
        stage: ConversationStage
    ) -> str:
        """
        Add scam-type specific emotional tone to response
        Makes responses feel more authentic
        """
        
        # Only add tone modifiers at certain stages
        if stage not in [ConversationStage.INTEREST, ConversationStage.COMPLIANCE]:
            return response
        
        scam_config = self.scam_behaviors.get(scam_type)
        if not scam_config:
            return response
        
        emotional_state = scam_config['emotional_state']
        
        # Add emotional prefixes based on scam type
        if emotional_state == 'excited_but_confused' and random.random() < 0.3:
            prefixes = ["Wow! ", "Oh my goodness! ", "Really? "]
            response = random.choice(prefixes) + response
        
        elif emotional_state == 'worried_urgent' and random.random() < 0.3:
            prefixes = ["Oh no! ", "Please help - ", "I'm worried - "]
            response = random.choice(prefixes) + response
        
        elif emotional_state == 'cautious_hesitant' and random.random() < 0.3:
            prefixes = ["I'm not sure but... ", "Hmm, ", "Let me think... "]
            response = random.choice(prefixes) + response
        
        return response
    
    def analyze_extraction_opportunity(self, incoming_message: str) -> Dict[str, Any]:
        """
        Analyze if incoming message contains extractable intelligence
        Used for logging/monitoring purposes
        """
        patterns = {
            'account_number': r'\b\d{9,18}\b',
            'ifsc': r'\b[A-Z]{4}0[A-Z0-9]{6}\b',
            'upi': r'\b[\w\.\-]+@[\w]+\b',
            'phone': r'\b[6-9]\d{9}\b',
            'link': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
        }
        
        findings = {}
        for key, pattern in patterns.items():
            matches = re.findall(pattern, incoming_message)
            if matches:
                findings[key] = matches
        
        return findings
