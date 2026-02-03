"""
Scam Detection Module
Analyzes messages to detect scam intent using patterns, keywords, and AI reasoning
"""

import re
from typing import Dict, List, Any


class ScamDetector:
    """Detects scam intent in messages"""
    
    def __init__(self):
        # Common scam indicators and patterns
        self.scam_patterns = {
            'financial_fraud': [
                r'\b(?:bank|account|atm|credit card|debit card)\b.*\b(?:block|expire|suspend|verify|update|confirm)\b',
                r'\b(?:urgent|immediate|action required)\b.*\b(?:account|card|bank)\b',
                r'\bKYC\b.*\b(?:update|pending|expire|verify)\b',
                r'\b(?:refund|cashback|reward|prize)\b.*\b(?:claim|pending|won|congratulations)\b',
            ],
            'payment_scam': [
                r'\b(?:paytm|phonepe|gpay|google pay|upi)\b.*\b(?:verify|update|expire|link|activate)\b',
                r'\bsend\b.*\b(?:otp|code|pin|password)\b',
                r'\b(?:transfer|payment)\b.*\b(?:failed|pending|reversed)\b',
            ],
            'phishing': [
                r'(?:click|tap|visit)\b.*\b(?:link|url|website)\b',
                r'\blink\b.*\b(?:verify|update|activate|claim)\b',
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            ],
            'impersonation': [
                r'\b(?:dear customer|valued customer|account holder)\b',
                r'\bfrom\b.*\b(?:bank|government|tax department|IT department)\b',
                r'\b(?:rbi|sebi|income tax|gst)\b',
            ],
            'lottery_prize': [
                r'\b(?:won|winner|selected|lucky)\b.*\b(?:lottery|prize|reward|contest)\b',
                r'\bcongratulations\b.*\b(?:win|won|selected)\b',
                r'\b(?:lakhs?|crores?|million)\b.*\b(?:rupees?|rs\.?|inr)\b',
            ],
            'job_scam': [
                r'\b(?:job|work from home|part time|earn)\b.*\b(?:daily|monthly|weekly)\b',
                r'\b(?:register|registration)\b.*\b(?:fee|amount|payment)\b',
                r'\b(?:guaranteed|assured)\b.*\b(?:income|salary|earning)\b',
            ]
        }
        
        self.urgency_keywords = [
            'urgent', 'immediately', 'asap', 'now', 'today',
            'expire', 'expiring', 'last chance', 'limited time',
            'within 24 hours', 'act now', 'don\'t wait'
        ]
        
        self.credential_requests = [
            'otp', 'pin', 'password', 'cvv', 'card number',
            'account number', 'aadhar', 'pan', 'date of birth',
            'mother\'s maiden name', 'security code'
        ]
        
        self.financial_indicators = [
            'bank account', 'account number', 'ifsc', 'upi id',
            'upi', 'paytm', 'phonepe', 'gpay', 'payment link',
            'transfer money', 'send money', 'pay now'
        ]
    
    def analyze(self, message: str, conversation_history: List[Dict] = None) -> Dict[str, Any]:
        """
        Analyze message for scam indicators
        
        Returns:
            {
                'is_scam': bool,
                'confidence': float (0-1),
                'scam_type': str,
                'indicators': List[str],
                'reasoning': str
            }
        """
        message_lower = message.lower()
        indicators = []
        scam_types_detected = []
        confidence_score = 0.0
        
        # Check for scam patterns
        for scam_type, patterns in self.scam_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    scam_types_detected.append(scam_type)
                    indicators.append(f"Matched {scam_type} pattern")
                    confidence_score += 0.15
                    break  # Only count each scam type once
        
        # Check for urgency keywords
        urgency_count = sum(1 for keyword in self.urgency_keywords if keyword in message_lower)
        if urgency_count > 0:
            indicators.append(f"Contains urgency language ({urgency_count} instances)")
            confidence_score += min(urgency_count * 0.1, 0.3)
        
        # Check for credential requests
        credential_count = sum(1 for cred in self.credential_requests if cred in message_lower)
        if credential_count > 0:
            indicators.append(f"Requests sensitive credentials ({credential_count} types)")
            confidence_score += min(credential_count * 0.15, 0.4)
        
        # Check for financial indicators
        financial_count = sum(1 for indicator in self.financial_indicators if indicator in message_lower)
        if financial_count > 0:
            indicators.append(f"Contains financial terminology ({financial_count} instances)")
            confidence_score += min(financial_count * 0.08, 0.25)
        
        # Check for suspicious links
        if re.search(r'http[s]?://', message_lower):
            indicators.append("Contains external link")
            confidence_score += 0.2
        
        # Check for phone numbers
        if re.search(r'\b\d{10}\b|\+\d{1,3}[\s-]?\d{10}\b', message):
            indicators.append("Contains phone number")
            confidence_score += 0.1
        
        # Check for common scam phrases
        scam_phrases = [
            'verify your account', 'account will be blocked', 'suspended account',
            'claim your reward', 'you have won', 'confirm your identity',
            'update your kyc', 'expired card', 'failed transaction',
            'refund pending', 'tax refund', 'government grant'
        ]
        
        phrase_matches = sum(1 for phrase in scam_phrases if phrase in message_lower)
        if phrase_matches > 0:
            indicators.append(f"Contains common scam phrases ({phrase_matches} matches)")
            confidence_score += min(phrase_matches * 0.12, 0.35)
        
        # Analyze conversation history for evolving patterns
        if conversation_history and len(conversation_history) > 1:
            # Check if scammer is progressively asking for more information
            recent_messages = [msg['content'].lower() for msg in conversation_history[-3:] if msg['role'] == 'scammer']
            
            credential_progression = sum(
                sum(1 for cred in self.credential_requests if cred in msg)
                for msg in recent_messages
            )
            
            if credential_progression >= 2:
                indicators.append("Progressive credential harvesting detected")
                confidence_score += 0.25
        
        # Cap confidence at 1.0
        confidence_score = min(confidence_score, 1.0)
        
        # Determine if it's a scam (threshold: 0.3)
        is_scam = confidence_score >= 0.3
        
        # Determine primary scam type
        primary_scam_type = scam_types_detected[0] if scam_types_detected else 'unknown'
        
        # Generate reasoning
        reasoning = self._generate_reasoning(is_scam, indicators, confidence_score)
        
        return {
            'is_scam': is_scam,
            'confidence': round(confidence_score, 3),
            'scam_type': primary_scam_type,
            'indicators': indicators,
            'reasoning': reasoning,
            'all_detected_types': scam_types_detected
        }
    
    def _generate_reasoning(self, is_scam: bool, indicators: List[str], confidence: float) -> str:
        """Generate human-readable reasoning for the detection"""
        if not is_scam:
            return "Message does not contain sufficient scam indicators."
        
        reasoning = f"Scam detected with {confidence:.1%} confidence. "
        
        if indicators:
            reasoning += f"Key indicators: {', '.join(indicators[:3])}"
            if len(indicators) > 3:
                reasoning += f" and {len(indicators) - 3} more."
        
        return reasoning
    
    def extract_contact_info(self, message: str) -> Dict[str, List[str]]:
        """Extract potential contact information from message"""
        extracted = {
            'phone_numbers': [],
            'urls': [],
            'email_addresses': []
        }
        
        # Extract phone numbers
        phone_pattern = r'\b(?:\+\d{1,3}[\s-]?)?\d{10}\b'
        extracted['phone_numbers'] = list(set(re.findall(phone_pattern, message)))
        
        # Extract URLs
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        extracted['urls'] = list(set(re.findall(url_pattern, message)))
        
        # Extract email addresses
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        extracted['email_addresses'] = list(set(re.findall(email_pattern, message)))
        
        return extracted
