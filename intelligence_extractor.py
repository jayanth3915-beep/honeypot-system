"""
Intelligence Extractor
Extracts actionable intelligence from scam conversations including:
- Bank account numbers
- UPI IDs
- IFSC codes
- Phone numbers
- Phishing URLs
- Email addresses
"""

import re
from typing import Dict, List, Any
from datetime import datetime


class IntelligenceExtractor:
    """Extracts structured intelligence from scam conversations"""
    
    def __init__(self):
        # Regex patterns for intelligence extraction
        self.patterns = {
            'bank_account': r'\b\d{9,18}\b',
            'ifsc_code': r'\b[A-Z]{4}0[A-Z0-9]{6}\b',
            'upi_id': r'\b[a-zA-Z0-9._-]+@[a-zA-Z]+\b',
            'phone_number': r'\b(?:\+91[\s-]?)?[6-9]\d{9}\b',
            'url': r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'amount': r'(?:rs\.?|rupees?|inr)\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',
            'pan_card': r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
            'aadhar': r'\b\d{4}\s?\d{4}\s?\d{4}\b'
        }
        
        # UPI provider patterns
        self.upi_providers = [
            'paytm', 'phonepe', 'googlepay', 'gpay', 'bhim',
            'ybl', 'okhdfcbank', 'oksbi', 'okicici', 'okaxis'
        ]
    
    def extract(self, conversation_history: List[Dict]) -> Dict[str, Any]:
        """
        Extract all intelligence from conversation history
        
        Returns structured intelligence dictionary with all extracted data
        """
        intelligence = {
            'bank_accounts': [],
            'ifsc_codes': [],
            'upi_ids': [],
            'phone_numbers': [],
            'phishing_urls': [],
            'email_addresses': [],
            'amounts_mentioned': [],
            'pan_cards': [],
            'aadhar_numbers': [],
            'payment_apps': [],
            'extraction_metadata': {
                'total_messages_analyzed': len(conversation_history),
                'extraction_timestamp': datetime.utcnow().isoformat(),
                'scammer_messages_count': 0
            }
        }
        
        # Process each message from scammer
        for message_obj in conversation_history:
            if message_obj['role'] == 'scammer':
                intelligence['extraction_metadata']['scammer_messages_count'] += 1
                message = message_obj['content']
                
                # Extract each type of intelligence
                self._extract_bank_accounts(message, intelligence)
                self._extract_ifsc_codes(message, intelligence)
                self._extract_upi_ids(message, intelligence)
                self._extract_phone_numbers(message, intelligence)
                self._extract_urls(message, intelligence)
                self._extract_emails(message, intelligence)
                self._extract_amounts(message, intelligence)
                self._extract_pan_cards(message, intelligence)
                self._extract_aadhar(message, intelligence)
                self._extract_payment_apps(message, intelligence)
        
        # Deduplicate and clean all extracted data
        intelligence = self._deduplicate_intelligence(intelligence)
        
        # Add summary statistics
        intelligence['summary'] = self._generate_summary(intelligence)
        
        return intelligence
    
    def _extract_bank_accounts(self, message: str, intelligence: Dict):
        """Extract bank account numbers"""
        matches = re.findall(self.patterns['bank_account'], message)
        
        for match in matches:
            # Validate account number (9-18 digits)
            if 9 <= len(match) <= 18:
                intelligence['bank_accounts'].append({
                    'account_number': match,
                    'length': len(match),
                    'extracted_from': message[:50] + '...' if len(message) > 50 else message
                })
    
    def _extract_ifsc_codes(self, message: str, intelligence: Dict):
        """Extract IFSC codes"""
        matches = re.findall(self.patterns['ifsc_code'], message.upper())
        
        for match in matches:
            intelligence['ifsc_codes'].append({
                'ifsc_code': match,
                'bank_code': match[:4],
                'branch_code': match[5:],
                'extracted_from': message[:50] + '...' if len(message) > 50 else message
            })
    
    def _extract_upi_ids(self, message: str, intelligence: Dict):
        """Extract UPI IDs"""
        matches = re.findall(self.patterns['upi_id'], message)
        
        for match in matches:
            # Filter out regular email addresses (UPI IDs typically use specific providers)
            upi_provider = match.split('@')[1] if '@' in match else ''
            
            # Check if it's a known UPI provider or looks like a UPI ID
            is_upi = any(provider in upi_provider.lower() for provider in self.upi_providers)
            
            if is_upi or (len(match.split('@')[0]) <= 20 and not '.' in match.split('@')[1]):
                intelligence['upi_ids'].append({
                    'upi_id': match,
                    'provider': upi_provider,
                    'extracted_from': message[:50] + '...' if len(message) > 50 else message
                })
    
    def _extract_phone_numbers(self, message: str, intelligence: Dict):
        """Extract phone numbers"""
        matches = re.findall(self.patterns['phone_number'], message)
        
        for match in matches:
            # Clean the phone number
            cleaned = re.sub(r'[\s-]', '', match)
            
            intelligence['phone_numbers'].append({
                'phone_number': cleaned,
                'formatted': match,
                'extracted_from': message[:50] + '...' if len(message) > 50 else message
            })
    
    def _extract_urls(self, message: str, intelligence: Dict):
        """Extract URLs (potential phishing links)"""
        matches = re.findall(self.patterns['url'], message)
        
        for match in matches:
            # Analyze URL for phishing indicators
            is_suspicious = self._analyze_url_suspiciousness(match)
            
            intelligence['phishing_urls'].append({
                'url': match,
                'domain': self._extract_domain(match),
                'is_suspicious': is_suspicious,
                'suspicion_reasons': is_suspicious.get('reasons', []) if isinstance(is_suspicious, dict) else [],
                'extracted_from': message[:50] + '...' if len(message) > 50 else message
            })
    
    def _extract_emails(self, message: str, intelligence: Dict):
        """Extract email addresses"""
        matches = re.findall(self.patterns['email'], message)
        
        for match in matches:
            # Filter out UPI IDs
            if not any(provider in match.lower() for provider in self.upi_providers):
                intelligence['email_addresses'].append({
                    'email': match,
                    'domain': match.split('@')[1],
                    'extracted_from': message[:50] + '...' if len(message) > 50 else message
                })
    
    def _extract_amounts(self, message: str, intelligence: Dict):
        """Extract mentioned amounts"""
        matches = re.findall(self.patterns['amount'], message, re.IGNORECASE)
        
        for match in matches:
            # Clean and convert amount
            amount_str = re.sub(r'[,\s]', '', match)
            try:
                amount = float(amount_str)
                intelligence['amounts_mentioned'].append({
                    'amount': amount,
                    'formatted': match,
                    'context': self._extract_amount_context(message, match)
                })
            except ValueError:
                pass
    
    def _extract_pan_cards(self, message: str, intelligence: Dict):
        """Extract PAN card numbers"""
        matches = re.findall(self.patterns['pan_card'], message.upper())
        
        for match in matches:
            intelligence['pan_cards'].append({
                'pan_number': match,
                'extracted_from': message[:50] + '...' if len(message) > 50 else message
            })
    
    def _extract_aadhar(self, message: str, intelligence: Dict):
        """Extract Aadhar numbers"""
        matches = re.findall(self.patterns['aadhar'], message)
        
        for match in matches:
            # Mask Aadhar for privacy
            masked = 'XXXX XXXX ' + match[-4:]
            
            intelligence['aadhar_numbers'].append({
                'aadhar_masked': masked,
                'extracted_from': message[:50] + '...' if len(message) > 50 else message
            })
    
    def _extract_payment_apps(self, message: str, intelligence: Dict):
        """Extract mentioned payment apps"""
        message_lower = message.lower()
        
        payment_apps = ['paytm', 'phonepe', 'gpay', 'google pay', 'bhim', 'amazon pay']
        
        for app in payment_apps:
            if app in message_lower:
                if app not in intelligence['payment_apps']:
                    intelligence['payment_apps'].append(app)
    
    def _analyze_url_suspiciousness(self, url: str) -> Dict[str, Any]:
        """Analyze URL for phishing indicators"""
        suspicious = False
        reasons = []
        
        url_lower = url.lower()
        
        # Check for suspicious TLDs
        suspicious_tlds = ['.xyz', '.top', '.club', '.tk', '.ml', '.ga', '.cf', '.gq']
        if any(tld in url_lower for tld in suspicious_tlds):
            suspicious = True
            reasons.append('Suspicious TLD')
        
        # Check for IP address instead of domain
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
            suspicious = True
            reasons.append('Uses IP address')
        
        # Check for URL shorteners
        shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly']
        if any(shortener in url_lower for shortener in shorteners):
            suspicious = True
            reasons.append('URL shortener')
        
        # Check for misspelled banking/payment domains
        legit_domains = ['paytm', 'phonepe', 'googlepay', 'sbi', 'hdfc', 'icici', 'axis']
        for domain in legit_domains:
            if domain in url_lower and not f'{domain}.com' in url_lower and not f'{domain}.in' in url_lower:
                suspicious = True
                reasons.append(f'Potential {domain} phishing')
        
        return {
            'is_suspicious': suspicious,
            'reasons': reasons
        }
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            match = re.search(r'://([^/]+)', url)
            if match:
                return match.group(1)
        except:
            pass
        return 'unknown'
    
    def _extract_amount_context(self, message: str, amount: str) -> str:
        """Extract context around mentioned amount"""
        # Find position of amount in message
        pos = message.lower().find(amount.lower())
        
        if pos == -1:
            return ''
        
        # Extract 30 characters before and after
        start = max(0, pos - 30)
        end = min(len(message), pos + len(amount) + 30)
        
        context = message[start:end]
        if start > 0:
            context = '...' + context
        if end < len(message):
            context = context + '...'
        
        return context
    
    def _deduplicate_intelligence(self, intelligence: Dict) -> Dict:
        """Remove duplicates from extracted intelligence"""
        
        # Deduplicate bank accounts
        seen_accounts = set()
        unique_accounts = []
        for item in intelligence['bank_accounts']:
            if item['account_number'] not in seen_accounts:
                seen_accounts.add(item['account_number'])
                unique_accounts.append(item)
        intelligence['bank_accounts'] = unique_accounts
        
        # Deduplicate IFSC codes
        seen_ifsc = set()
        unique_ifsc = []
        for item in intelligence['ifsc_codes']:
            if item['ifsc_code'] not in seen_ifsc:
                seen_ifsc.add(item['ifsc_code'])
                unique_ifsc.append(item)
        intelligence['ifsc_codes'] = unique_ifsc
        
        # Deduplicate UPI IDs
        seen_upi = set()
        unique_upi = []
        for item in intelligence['upi_ids']:
            if item['upi_id'] not in seen_upi:
                seen_upi.add(item['upi_id'])
                unique_upi.append(item)
        intelligence['upi_ids'] = unique_upi
        
        # Deduplicate phone numbers
        seen_phones = set()
        unique_phones = []
        for item in intelligence['phone_numbers']:
            if item['phone_number'] not in seen_phones:
                seen_phones.add(item['phone_number'])
                unique_phones.append(item)
        intelligence['phone_numbers'] = unique_phones
        
        # Deduplicate URLs
        seen_urls = set()
        unique_urls = []
        for item in intelligence['phishing_urls']:
            if item['url'] not in seen_urls:
                seen_urls.add(item['url'])
                unique_urls.append(item)
        intelligence['phishing_urls'] = unique_urls
        
        # Deduplicate emails
        seen_emails = set()
        unique_emails = []
        for item in intelligence['email_addresses']:
            if item['email'] not in seen_emails:
                seen_emails.add(item['email'])
                unique_emails.append(item)
        intelligence['email_addresses'] = unique_emails
        
        return intelligence
    
    def _generate_summary(self, intelligence: Dict) -> Dict[str, int]:
        """Generate summary statistics of extracted intelligence"""
        return {
            'total_bank_accounts': len(intelligence['bank_accounts']),
            'total_ifsc_codes': len(intelligence['ifsc_codes']),
            'total_upi_ids': len(intelligence['upi_ids']),
            'total_phone_numbers': len(intelligence['phone_numbers']),
            'total_phishing_urls': len(intelligence['phishing_urls']),
            'total_suspicious_urls': sum(1 for url in intelligence['phishing_urls'] if url.get('is_suspicious', {}).get('is_suspicious', False)),
            'total_email_addresses': len(intelligence['email_addresses']),
            'total_amounts_mentioned': len(intelligence['amounts_mentioned']),
            'total_pan_cards': len(intelligence['pan_cards']),
            'total_aadhar_numbers': len(intelligence['aadhar_numbers']),
            'total_payment_apps': len(intelligence['payment_apps']),
            'intelligence_quality_score': self._calculate_quality_score(intelligence)
        }
    
    def _calculate_quality_score(self, intelligence: Dict) -> float:
        """Calculate quality score of extracted intelligence (0-100)"""
        score = 0.0
        
        # High-value intelligence
        score += len(intelligence['bank_accounts']) * 20
        score += len(intelligence['upi_ids']) * 15
        score += len(intelligence['ifsc_codes']) * 10
        
        # Medium-value intelligence
        score += len(intelligence['phone_numbers']) * 8
        score += len(intelligence['phishing_urls']) * 12
        
        # Lower-value intelligence
        score += len(intelligence['email_addresses']) * 5
        score += len(intelligence['amounts_mentioned']) * 3
        
        # Cap at 100
        return min(score, 100.0)
