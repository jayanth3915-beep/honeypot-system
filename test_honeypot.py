"""
Test Script for Honey-Pot System
Run this to test various scam scenarios and validate the system
"""

import requests
import json
import time
from datetime import datetime


class HoneypotTester:
    """Test the honeypot system with various scam scenarios"""
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'X-API-Key': api_key
        }
    
    def test_health(self):
        """Test health check endpoint"""
        print("\n" + "="*60)
        print("TEST 1: Health Check")
        print("="*60)
        
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def test_scam_scenario(self, scenario_name, message, conversation_id=None):
        """Test a scam detection scenario"""
        print("\n" + "="*60)
        print(f"TEST: {scenario_name}")
        print("="*60)
        
        if not conversation_id:
            conversation_id = f"test_{int(time.time())}"
        
        payload = {
            "conversation_id": conversation_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": {
                "platform": "test",
                "sender_id": "test_scammer"
            }
        }
        
        print(f"\nSending message: {message}")
        print(f"Conversation ID: {conversation_id}")
        
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/message",
                headers=self.headers,
                json=payload
            )
            
            print(f"\nStatus Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n--- Scam Detection ---")
                print(f"Detected: {data['scam_detection']['detected']}")
                print(f"Confidence: {data['scam_detection']['confidence']}")
                print(f"Type: {data['scam_detection']['scam_type']}")
                print(f"Indicators: {data['scam_detection']['indicators']}")
                
                print(f"\n--- Agent Response ---")
                print(f"Message: {data['agent_response']['message']}")
                print(f"Strategy: {data['agent_response']['strategy']}")
                
                print(f"\n--- Metrics ---")
                print(f"Turn Count: {data['engagement_metrics']['turn_count']}")
                print(f"Duration: {data['engagement_metrics']['engagement_duration_seconds']}s")
                
                if data['extracted_intelligence'].get('summary'):
                    print(f"\n--- Intelligence Summary ---")
                    for key, value in data['extracted_intelligence']['summary'].items():
                        if value > 0:
                            print(f"{key}: {value}")
                
                return data
            else:
                print(f"Error: {response.text}")
                return None
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return None
    
    def test_multi_turn_conversation(self):
        """Test a multi-turn conversation"""
        print("\n" + "="*60)
        print("TEST: Multi-Turn Conversation")
        print("="*60)
        
        conversation_id = f"multi_turn_{int(time.time())}"
        
        messages = [
            "Dear customer, your bank account KYC is pending. Update immediately.",
            "We need to verify your account. Please provide your account details.",
            "You can transfer to this account: 123456789012, IFSC: SBIN0001234",
            "For UPI payments, use 9876543210@paytm or send to our secure link: http://fake-bank-verify.com"
        ]
        
        for i, message in enumerate(messages, 1):
            print(f"\n--- Turn {i} ---")
            response = self.test_scam_scenario(
                f"Turn {i}",
                message,
                conversation_id
            )
            
            if response:
                print(f"Agent replied: {response['agent_response']['message']}")
            
            time.sleep(1)  # Brief pause between turns
        
        # Get full conversation
        print(f"\n--- Fetching Full Conversation ---")
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/conversation/{conversation_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                data = response.json()
                conv = data['conversation']
                
                print(f"\nTotal Turns: {conv['turn_count']}")
                print(f"Scam Detected: {conv['scam_detected']}")
                print(f"Scam Type: {conv.get('scam_type', 'N/A')}")
                
                intel = conv['extracted_intelligence']
                print(f"\n--- Extracted Intelligence ---")
                print(f"Bank Accounts: {len(intel.get('bank_accounts', []))}")
                print(f"IFSC Codes: {len(intel.get('ifsc_codes', []))}")
                print(f"UPI IDs: {len(intel.get('upi_ids', []))}")
                print(f"Phone Numbers: {len(intel.get('phone_numbers', []))}")
                print(f"Phishing URLs: {len(intel.get('phishing_urls', []))}")
                
                if intel.get('bank_accounts'):
                    print("\nBank Accounts Found:")
                    for acc in intel['bank_accounts']:
                        print(f"  - {acc['account_number']}")
                
                if intel.get('upi_ids'):
                    print("\nUPI IDs Found:")
                    for upi in intel['upi_ids']:
                        print(f"  - {upi['upi_id']}")
                
                if intel.get('ifsc_codes'):
                    print("\nIFSC Codes Found:")
                    for ifsc in intel['ifsc_codes']:
                        print(f"  - {ifsc['ifsc_code']}")
                
                if intel.get('phishing_urls'):
                    print("\nPhishing URLs Found:")
                    for url in intel['phishing_urls']:
                        print(f"  - {url['url']} (Suspicious: {url.get('is_suspicious', False)})")
                
        except Exception as e:
            print(f"Error fetching conversation: {str(e)}")
    
    def run_all_tests(self):
        """Run all test scenarios"""
        print("\n" + "="*60)
        print("HONEYPOT SYSTEM TEST SUITE")
        print("="*60)
        
        # Test 1: Health check
        health_ok = self.test_health()
        
        if not health_ok:
            print("\n❌ Health check failed! Server may not be running.")
            return
        
        print("\n✅ Health check passed!")
        
        # Test 2: Bank phishing scam
        self.test_scam_scenario(
            "Bank Phishing Scam",
            "Dear customer, your HDFC account will be blocked due to pending KYC. Update now: http://hdfc-kyc-update.tk"
        )
        
        # Test 3: UPI scam
        self.test_scam_scenario(
            "UPI Verification Scam",
            "Your Paytm wallet needs verification. Share the OTP you received to verify your account."
        )
        
        # Test 4: Prize/Lottery scam
        self.test_scam_scenario(
            "Lottery Prize Scam",
            "Congratulations! You have won Rs 25 lakhs in lucky draw. Pay Rs 5000 processing fee to 9876543210@paytm"
        )
        
        # Test 5: Job scam
        self.test_scam_scenario(
            "Work From Home Scam",
            "Earn Rs 50,000 monthly working from home. Register now with Rs 2000 registration fee. Call 9876543210"
        )
        
        # Test 6: Account details extraction
        self.test_scam_scenario(
            "Direct Account Details",
            "Send payment to Account: 123456789012, IFSC: SBIN0001234, or use UPI: scammer@paytm, Contact: 9876543210"
        )
        
        # Test 7: Multi-turn conversation
        self.test_multi_turn_conversation()
        
        print("\n" + "="*60)
        print("TEST SUITE COMPLETED")
        print("="*60)


def main():
    """Main test function"""
    print("Honeypot System Test Script")
    print("-" * 60)
    
    # Configuration
    base_url = input("Enter API base URL (e.g., http://localhost:5000): ").strip()
    api_key = input("Enter API key: ").strip()
    
    if not base_url:
        base_url = "http://localhost:5000"
    
    if not api_key:
        api_key = "your-secret-api-key-here"
    
    # Create tester and run tests
    tester = HoneypotTester(base_url, api_key)
    tester.run_all_tests()


if __name__ == "__main__":
    main()
