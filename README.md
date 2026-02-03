# AI-Powered Agentic Honey-Pot System

An intelligent system that detects scam messages and autonomously engages scammers to extract actionable intelligence such as bank account details, UPI IDs, and phishing links.

## 🎯 Features

- **Intelligent Scam Detection**: Multi-pattern detection system that identifies various scam types
- **Autonomous Agent Engagement**: AI agent that maintains realistic conversations with scammers
- **Intelligence Extraction**: Automatically extracts and structures valuable scam intelligence
- **Multi-turn Conversations**: Supports extended conversations with conversation history
- **Secure API**: Protected with API key authentication
- **Real-time Processing**: Low-latency responses for seamless interaction

## 🏗️ Architecture

```
┌─────────────────┐
│  Mock Scammer   │
│      API        │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│         Honey-Pot API Endpoint          │
├─────────────────────────────────────────┤
│  1. Scam Detection Module               │
│     - Pattern matching                  │
│     - Keyword analysis                  │
│     - Context evaluation                │
│                                         │
│  2. Agent Engagement Engine             │
│     - Strategy selection                │
│     - Contextual response generation    │
│     - Persona maintenance               │
│                                         │
│  3. Intelligence Extractor              │
│     - Bank account extraction           │
│     - UPI ID extraction                 │
│     - Phishing URL detection            │
│     - Contact info extraction           │
└─────────────────────────────────────────┘
```

## 📋 Requirements

- Python 3.8+
- Flask 3.0+
- Internet connection for deployment

## 🚀 Installation

### 1. Clone or Download the Project

```bash
# If you have the files, navigate to the directory
cd honeypot-system
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
# .env
HONEYPOT_API_KEY=your-secret-api-key-here
PORT=5000
```

Or export them directly:

```bash
export HONEYPOT_API_KEY="your-secret-api-key-here"
export PORT=5000
```

### 4. Run the Server

```bash
python app.py
```

The server will start on `http://0.0.0.0:5000`

## 🌐 Deployment

### Deploy to a Public Server

For evaluation, you need to deploy this to a publicly accessible endpoint. Here are some options:

#### Option 1: Deploy to Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### Option 2: Deploy to Render
1. Create account at render.com
2. Connect your Git repository
3. Set environment variables
4. Deploy as Web Service

#### Option 3: Deploy to Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create new app
heroku create your-honeypot-app

# Set environment variables
heroku config:set HONEYPOT_API_KEY=your-secret-key

# Deploy
git push heroku main
```

#### Option 4: Deploy to DigitalOcean/AWS/GCP
- Set up a VM instance
- Install Python and dependencies
- Run with gunicorn: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`

## 📡 API Documentation

### Base URL
```
https://your-deployed-url.com
```

### Authentication
All API requests require an API key in the headers:

```
X-API-Key: your-secret-api-key
```

or

```
Authorization: Bearer your-secret-api-key
```

---

### Endpoints

#### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-29T10:30:00Z",
  "service": "honeypot-system"
}
```

---

#### 2. Process Scam Message
```http
POST /api/v1/message
Content-Type: application/json
X-API-Key: your-secret-api-key
```

**Request Body:**
```json
{
  "conversation_id": "conv_12345",
  "message": "Dear customer, your bank account will be blocked. Click here to verify: http://fake-bank.com",
  "timestamp": "2024-01-29T10:30:00Z",
  "metadata": {
    "sender_id": "scammer_001",
    "platform": "sms"
  }
}
```

**Response:**
```json
{
  "conversation_id": "conv_12345",
  "scam_detection": {
    "detected": true,
    "confidence": 0.85,
    "scam_type": "phishing",
    "indicators": [
      "Matched phishing pattern",
      "Contains urgency language (2 instances)",
      "Contains external link"
    ]
  },
  "agent_response": {
    "message": "I got a link from you. What is this for? Is this safe to click?",
    "strategy": "initial_confusion",
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
        "url": "http://fake-bank.com",
        "domain": "fake-bank.com",
        "is_suspicious": true,
        "suspicion_reasons": ["Potential bank phishing"]
      }
    ],
    "email_addresses": [],
    "amounts_mentioned": [],
    "summary": {
      "total_phishing_urls": 1,
      "intelligence_quality_score": 12.0
    }
  },
  "timestamp": "2024-01-29T10:30:01Z"
}
```

---

#### 3. Get Conversation History
```http
GET /api/v1/conversation/{conversation_id}
X-API-Key: your-secret-api-key
```

**Response:**
```json
{
  "conversation_id": "conv_12345",
  "conversation": {
    "messages": [
      {
        "role": "scammer",
        "content": "Your bank account will be blocked...",
        "timestamp": "2024-01-29T10:30:00Z"
      },
      {
        "role": "agent",
        "content": "I got a link from you. What is this for?",
        "timestamp": "2024-01-29T10:30:01Z",
        "strategy": "initial_confusion"
      }
    ],
    "scam_detected": true,
    "scam_type": "phishing",
    "turn_count": 1,
    "extracted_intelligence": {...}
  }
}
```

---

#### 4. List All Conversations
```http
GET /api/v1/conversations
X-API-Key: your-secret-api-key
```

**Response:**
```json
{
  "total_conversations": 5,
  "conversations": [
    {
      "conversation_id": "conv_12345",
      "scam_detected": true,
      "turn_count": 8,
      "intelligence_count": 3,
      "start_time": "2024-01-29T10:30:00Z"
    }
  ]
}
```

## 🧪 Testing

### Test with cURL

```bash
# Health check
curl https://your-deployed-url.com/health

# Send a scam message
curl -X POST https://your-deployed-url.com/api/v1/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{
    "conversation_id": "test_001",
    "message": "Congratulations! You have won Rs 5 lakhs. Send your account number to claim.",
    "metadata": {
      "platform": "sms"
    }
  }'
```

### Test Multi-turn Conversation

```bash
# Turn 1
curl -X POST https://your-deployed-url.com/api/v1/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{
    "conversation_id": "multi_turn_001",
    "message": "Your KYC is pending. Update now to avoid account block."
  }'

# Turn 2 (using same conversation_id)
curl -X POST https://your-deployed-url.com/api/v1/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-api-key" \
  -d '{
    "conversation_id": "multi_turn_001",
    "message": "Please share your account number and IFSC code: 123456789012, SBIN0001234"
  }'
```

## 📊 Intelligence Extracted

The system can extract:

1. **Bank Account Numbers**: 9-18 digit account numbers
2. **IFSC Codes**: Bank branch codes (e.g., SBIN0001234)
3. **UPI IDs**: Payment identifiers (e.g., user@paytm)
4. **Phone Numbers**: Indian mobile numbers
5. **Phishing URLs**: Suspicious links with analysis
6. **Email Addresses**: Contact emails
7. **Amounts**: Monetary values mentioned
8. **PAN Cards**: Tax identification numbers
9. **Payment Apps**: Mentioned payment platforms

## 🎭 Agent Strategies

The autonomous agent uses multiple strategies:

1. **Initial Confusion**: Shows uncertainty to encourage explanation
2. **Show Interest**: Demonstrates engagement to keep scammer talking
3. **Request Details**: Asks for clarification to extract more info
4. **Feign Technical Difficulty**: Claims tech issues to get alternative contact methods
5. **Gradual Compliance**: Shows willingness to proceed, extracting credentials
6. **Ask for Credentials**: Directly prompts for payment/account details

## 🔍 Scam Types Detected

- Financial Fraud (account blocking, KYC)
- Payment Scams (UPI, digital wallets)
- Phishing (suspicious links)
- Impersonation (fake authorities)
- Lottery/Prize Scams
- Job Scams
- And more...

## 📈 Evaluation Metrics

The system tracks:

- **Scam Detection Accuracy**: Confidence scores and indicators
- **Engagement Duration**: Time spent in conversation
- **Turn Count**: Number of back-and-forth exchanges
- **Intelligence Quality**: Quantity and value of extracted data
- **Intelligence Quality Score**: 0-100 score based on extracted data value

## 🔒 Security Considerations

- API key authentication required for all endpoints
- No storage of actual user credentials
- Aadhar numbers automatically masked
- Conversation data stored temporarily (use Redis/DB for production)

## 🛠️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HONEYPOT_API_KEY` | API authentication key | `your-secret-api-key-here` |
| `PORT` | Server port | `5000` |

### Customization

Modify these files to customize behavior:

- `scam_detector.py`: Add/modify scam patterns
- `agent_engine.py`: Adjust response strategies
- `intelligence_extractor.py`: Add new extraction patterns

## 📝 Example Scam Scenarios

### Scenario 1: Bank Account Phishing
```json
{
  "message": "Dear customer, your SBI account will expire. Update KYC: http://sbi-update.tk"
}
```

### Scenario 2: UPI Verification Scam
```json
{
  "message": "Your Paytm account needs verification. Share OTP received on your phone."
}
```

### Scenario 3: Prize Scam
```json
{
  "message": "Congratulations! You won Rs 10 lakhs. Transfer Rs 500 processing fee to 9876543210@paytm"
}
```

## 🤝 Integration with Mock Scammer API

The system is designed to work with a Mock Scammer API that sends messages to your endpoint:

```
Mock Scammer API → Your Endpoint → Process → Response
```

Ensure your public endpoint URL is registered with the Mock Scammer API along with your API key.

## 📞 Support

For issues or questions:
1. Check the logs: The server logs all requests and errors
2. Verify API key authentication
3. Test with the health check endpoint first
4. Ensure all dependencies are installed

## 🎓 Best Practices

1. **Deploy Securely**: Use HTTPS in production
2. **Monitor Logs**: Track all scam interactions
3. **Update Patterns**: Regularly update scam detection patterns
4. **Rate Limiting**: Implement rate limiting for production
5. **Data Storage**: Use persistent storage (Redis/PostgreSQL) for production
6. **Scaling**: Use multiple workers with gunicorn for high traffic

## 📄 License

This project is for educational and evaluation purposes.

---

**Built for AI-Powered Agentic Honey-Pot Challenge** 🚀
