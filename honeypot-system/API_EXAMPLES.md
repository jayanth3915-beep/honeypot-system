# API Response Examples

This document provides detailed examples of API responses from the Honeypot System.

## 1. Health Check Response

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-29T10:30:00.000Z",
  "service": "honeypot-system"
}
```

---

## 2. Scam Detection - Bank Phishing

**Request:**
```json
{
  "conversation_id": "conv_001",
  "message": "Dear customer, your HDFC bank account will be blocked due to pending KYC. Update immediately: http://hdfc-verify.tk",
  "timestamp": "2024-01-29T10:30:00Z",
  "metadata": {
    "platform": "sms",
    "sender_id": "scammer_001"
  }
}
```

**Response:**
```json
{
  "conversation_id": "conv_001",
  "scam_detection": {
    "detected": true,
    "confidence": 0.85,
    "scam_type": "phishing",
    "indicators": [
      "Matched phishing pattern",
      "Contains urgency language (2 instances)",
      "Contains external link",
      "Contains common scam phrases (2 matches)"
    ]
  },
  "agent_response": {
    "message": "I got a link from you. What is this for? Is this safe to click?",
    "strategy": "feign_technical_difficulty",
    "agent_activated": true
  },
  "engagement_metrics": {
    "turn_count": 1,
    "engagement_duration_seconds": 0.5,
    "intelligence_extracted": true
  },
  "extracted_intelligence": {
    "bank_accounts": [],
    "ifsc_codes": [],
    "upi_ids": [],
    "phone_numbers": [],
    "phishing_urls": [
      {
        "url": "http://hdfc-verify.tk",
        "domain": "hdfc-verify.tk",
        "is_suspicious": {
          "is_suspicious": true,
          "reasons": [
            "Suspicious TLD",
            "Potential hdfc phishing"
          ]
        },
        "suspicion_reasons": [
          "Suspicious TLD",
          "Potential hdfc phishing"
        ],
        "extracted_from": "Dear customer, your HDFC bank account will b..."
      }
    ],
    "email_addresses": [],
    "amounts_mentioned": [],
    "pan_cards": [],
    "aadhar_numbers": [],
    "payment_apps": [],
    "extraction_metadata": {
      "total_messages_analyzed": 1,
      "extraction_timestamp": "2024-01-29T10:30:01.000Z",
      "scammer_messages_count": 1
    },
    "summary": {
      "total_bank_accounts": 0,
      "total_ifsc_codes": 0,
      "total_upi_ids": 0,
      "total_phone_numbers": 0,
      "total_phishing_urls": 1,
      "total_suspicious_urls": 1,
      "total_email_addresses": 0,
      "total_amounts_mentioned": 0,
      "total_pan_cards": 0,
      "total_aadhar_numbers": 0,
      "total_payment_apps": 0,
      "intelligence_quality_score": 12.0
    }
  },
  "timestamp": "2024-01-29T10:30:01.500Z"
}
```

---

## 3. High Intelligence Extraction - Complete Details

**Request:**
```json
{
  "conversation_id": "conv_002",
  "message": "Send payment to Account Number: 123456789012, IFSC: SBIN0001234, or use UPI: 9876543210@paytm. Contact on 9876543210 for any issues. Amount: Rs 5000",
  "metadata": {
    "platform": "whatsapp"
  }
}
```

**Response:**
```json
{
  "conversation_id": "conv_002",
  "scam_detection": {
    "detected": true,
    "confidence": 0.92,
    "scam_type": "payment_scam",
    "indicators": [
      "Matched payment_scam pattern",
      "Contains financial terminology (5 instances)",
      "Requests sensitive credentials (1 types)",
      "Contains phone number"
    ]
  },
  "agent_response": {
    "message": "I see an account number in your message. Is this where I should send the money? Can you confirm this is your official account?",
    "strategy": "request_details",
    "agent_activated": true
  },
  "engagement_metrics": {
    "turn_count": 1,
    "engagement_duration_seconds": 0.8,
    "intelligence_extracted": true
  },
  "extracted_intelligence": {
    "bank_accounts": [
      {
        "account_number": "123456789012",
        "length": 12,
        "extracted_from": "Send payment to Account Number: 123456789012,..."
      }
    ],
    "ifsc_codes": [
      {
        "ifsc_code": "SBIN0001234",
        "bank_code": "SBIN",
        "branch_code": "001234",
        "extracted_from": "Send payment to Account Number: 123456789012,..."
      }
    ],
    "upi_ids": [
      {
        "upi_id": "9876543210@paytm",
        "provider": "paytm",
        "extracted_from": "Send payment to Account Number: 123456789012,..."
      }
    ],
    "phone_numbers": [
      {
        "phone_number": "9876543210",
        "formatted": "9876543210",
        "extracted_from": "Send payment to Account Number: 123456789012,..."
      }
    ],
    "phishing_urls": [],
    "email_addresses": [],
    "amounts_mentioned": [
      {
        "amount": 5000.0,
        "formatted": "5000",
        "context": "...UPI: 9876543210@paytm. Contact on 9876543210 for any issues. Amount: Rs 5000"
      }
    ],
    "pan_cards": [],
    "aadhar_numbers": [],
    "payment_apps": ["paytm"],
    "extraction_metadata": {
      "total_messages_analyzed": 1,
      "extraction_timestamp": "2024-01-29T10:35:00.000Z",
      "scammer_messages_count": 1
    },
    "summary": {
      "total_bank_accounts": 1,
      "total_ifsc_codes": 1,
      "total_upi_ids": 1,
      "total_phone_numbers": 1,
      "total_phishing_urls": 0,
      "total_suspicious_urls": 0,
      "total_email_addresses": 0,
      "total_amounts_mentioned": 1,
      "total_pan_cards": 0,
      "total_aadhar_numbers": 0,
      "total_payment_apps": 1,
      "intelligence_quality_score": 61.0
    }
  },
  "timestamp": "2024-01-29T10:35:01.000Z"
}
```

---

## 4. Multi-Turn Conversation - Turn 5 Example

**Request (Turn 5):**
```json
{
  "conversation_id": "conv_003",
  "message": "Yes, verified. Now share your card CVV and expiry date to complete verification."
}
```

**Response:**
```json
{
  "conversation_id": "conv_003",
  "scam_detection": {
    "detected": true,
    "confidence": 0.88,
    "scam_type": "financial_fraud",
    "indicators": [
      "Matched financial_fraud pattern",
      "Requests sensitive credentials (2 types)",
      "Progressive credential harvesting detected"
    ]
  },
  "agent_response": {
    "message": "You're asking for CVV and expiry date. Can you tell me where I should send it? What platform should I use?",
    "strategy": "gradual_compliance",
    "agent_activated": true
  },
  "engagement_metrics": {
    "turn_count": 5,
    "engagement_duration_seconds": 42.3,
    "intelligence_extracted": true
  },
  "extracted_intelligence": {
    "bank_accounts": [
      {
        "account_number": "987654321098",
        "length": 12,
        "extracted_from": "Previous message: Transfer to 987654321098..."
      }
    ],
    "ifsc_codes": [],
    "upi_ids": [],
    "phone_numbers": [],
    "phishing_urls": [
      {
        "url": "http://verify-bank-kyc.com",
        "domain": "verify-bank-kyc.com",
        "is_suspicious": true,
        "extracted_from": "Turn 2: Click here http://verify-bank-kyc.com..."
      }
    ],
    "email_addresses": [],
    "amounts_mentioned": [],
    "pan_cards": [],
    "aadhar_numbers": [],
    "payment_apps": [],
    "extraction_metadata": {
      "total_messages_analyzed": 5,
      "extraction_timestamp": "2024-01-29T10:40:00.000Z",
      "scammer_messages_count": 3
    },
    "summary": {
      "total_bank_accounts": 1,
      "total_ifsc_codes": 0,
      "total_upi_ids": 0,
      "total_phone_numbers": 0,
      "total_phishing_urls": 1,
      "total_suspicious_urls": 1,
      "total_email_addresses": 0,
      "total_amounts_mentioned": 0,
      "total_pan_cards": 0,
      "total_aadhar_numbers": 0,
      "total_payment_apps": 0,
      "intelligence_quality_score": 32.0
    }
  },
  "timestamp": "2024-01-29T10:40:01.000Z"
}
```

---

## 5. Get Conversation History Response

**Request:** `GET /api/v1/conversation/conv_003`

**Response:**
```json
{
  "conversation_id": "conv_003",
  "conversation": {
    "messages": [
      {
        "role": "scammer",
        "content": "Your bank account needs urgent verification",
        "timestamp": "2024-01-29T10:38:00.000Z"
      },
      {
        "role": "agent",
        "content": "I'm not sure what this is regarding. Could you explain?",
        "timestamp": "2024-01-29T10:38:01.000Z",
        "strategy": "initial_confusion"
      },
      {
        "role": "scammer",
        "content": "Click here to verify: http://verify-bank-kyc.com",
        "timestamp": "2024-01-29T10:38:15.000Z"
      },
      {
        "role": "agent",
        "content": "I tried clicking the link but it's not opening. Can you send it again?",
        "timestamp": "2024-01-29T10:38:16.000Z",
        "strategy": "feign_technical_difficulty"
      },
      {
        "role": "scammer",
        "content": "Transfer Rs 500 to account 987654321098",
        "timestamp": "2024-01-29T10:39:00.000Z"
      },
      {
        "role": "agent",
        "content": "I see an account number. Is this where I send the money?",
        "timestamp": "2024-01-29T10:39:01.000Z",
        "strategy": "request_details"
      }
    ],
    "scam_detected": true,
    "agent_activated": true,
    "start_time": "2024-01-29T10:38:00.000Z",
    "turn_count": 3,
    "scam_type": "financial_fraud",
    "confidence": 0.88,
    "indicators": [
      "Matched financial_fraud pattern",
      "Contains urgency language",
      "Contains external link",
      "Contains financial terminology"
    ],
    "extracted_intelligence": {
      "bank_accounts": [
        {
          "account_number": "987654321098",
          "length": 12,
          "extracted_from": "Transfer Rs 500 to account 987654321098"
        }
      ],
      "ifsc_codes": [],
      "upi_ids": [],
      "phone_numbers": [],
      "phishing_urls": [
        {
          "url": "http://verify-bank-kyc.com",
          "domain": "verify-bank-kyc.com",
          "is_suspicious": true
        }
      ],
      "summary": {
        "total_bank_accounts": 1,
        "total_phishing_urls": 1,
        "intelligence_quality_score": 32.0
      }
    }
  }
}
```

---

## 6. List All Conversations Response

**Request:** `GET /api/v1/conversations`

**Response:**
```json
{
  "total_conversations": 3,
  "conversations": [
    {
      "conversation_id": "conv_001",
      "scam_detected": true,
      "turn_count": 1,
      "intelligence_count": 1,
      "start_time": "2024-01-29T10:30:00.000Z"
    },
    {
      "conversation_id": "conv_002",
      "scam_detected": true,
      "turn_count": 1,
      "intelligence_count": 4,
      "start_time": "2024-01-29T10:35:00.000Z"
    },
    {
      "conversation_id": "conv_003",
      "scam_detected": true,
      "turn_count": 5,
      "intelligence_count": 2,
      "start_time": "2024-01-29T10:38:00.000Z"
    }
  ]
}
```

---

## 7. Error Responses

### Unauthorized (Missing API Key)

```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing API key"
}
```

### Bad Request (Missing Message)

```json
{
  "error": "Bad Request",
  "message": "Missing required field: message"
}
```

### Conversation Not Found

```json
{
  "error": "Conversation not found"
}
```

### Internal Server Error

```json
{
  "error": "Internal Server Error",
  "message": "Error details here"
}
```

---

## Response Field Descriptions

### Scam Detection Object

| Field | Type | Description |
|-------|------|-------------|
| `detected` | boolean | Whether scam was detected |
| `confidence` | float | Confidence score (0-1) |
| `scam_type` | string | Type of scam detected |
| `indicators` | array | List of detection indicators |

### Agent Response Object

| Field | Type | Description |
|-------|------|-------------|
| `message` | string | Agent's response message |
| `strategy` | string | Engagement strategy used |
| `agent_activated` | boolean | Whether autonomous agent is active |

### Engagement Metrics Object

| Field | Type | Description |
|-------|------|-------------|
| `turn_count` | integer | Number of conversation turns |
| `engagement_duration_seconds` | float | Total conversation duration |
| `intelligence_extracted` | boolean | Whether intelligence was extracted |

### Extracted Intelligence Summary

| Field | Type | Description |
|-------|------|-------------|
| `total_bank_accounts` | integer | Number of bank accounts found |
| `total_ifsc_codes` | integer | Number of IFSC codes found |
| `total_upi_ids` | integer | Number of UPI IDs found |
| `total_phone_numbers` | integer | Number of phone numbers found |
| `total_phishing_urls` | integer | Number of URLs found |
| `total_suspicious_urls` | integer | Number of suspicious URLs |
| `intelligence_quality_score` | float | Quality score (0-100) |

---

## Intelligence Quality Score Calculation

The quality score is calculated based on:

- Bank Accounts: 20 points each
- UPI IDs: 15 points each
- IFSC Codes: 10 points each
- Phone Numbers: 8 points each
- Phishing URLs: 12 points each
- Email Addresses: 5 points each
- Amounts: 3 points each

Maximum score: 100

---

## Agent Engagement Strategies

1. **initial_confusion** - Shows uncertainty to encourage explanation
2. **show_interest** - Demonstrates engagement
3. **request_details** - Asks for more information
4. **feign_technical_difficulty** - Claims technical problems
5. **gradual_compliance** - Shows willingness to cooperate
6. **ask_for_credentials** - Prompts for sensitive data

---

This documentation covers all possible API responses from the Honeypot System.
