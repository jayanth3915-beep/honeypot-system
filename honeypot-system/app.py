"""
AI-Powered Agentic Honey-Pot System
Main API server for detecting and engaging with scammers
"""

from flask import Flask, request, jsonify
import os
from datetime import datetime
import json
from scam_detector import ScamDetector
from agent_engine import ScammerEngagementAgent
from intelligence_extractor import IntelligenceExtractor

app = Flask(__name__)

# =========================
# CONFIGURATION
# =========================
API_KEY = "123456"
DATA_FILE = "data/conversations.json"

# =========================
# INITIALIZE COMPONENTS
# =========================
scam_detector = ScamDetector()
engagement_agent = ScammerEngagementAgent()
intelligence_extractor = IntelligenceExtractor()

# =========================
# DATA PERSISTENCE HELPERS
# =========================
def load_conversations():
    """Load conversations from JSON file at startup"""
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_conversations():
    """Save conversations to JSON file"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(conversation_store, f, indent=2)

# Load existing conversations
conversation_store = load_conversations()

# =========================
# AUTHENTICATION
# =========================
def verify_api_key(request):
    """Verify the API key from request headers"""
    api_key = request.headers.get('X-API-Key') or request.headers.get('Authorization')
    if api_key and api_key.replace('Bearer ', '') == API_KEY:
        return True
    return False

# =========================
# ROUTES
# =========================
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'honeypot-system'
    }), 200


@app.route('/api/v1/message', methods=['POST'])
def handle_message():

    if not verify_api_key(request):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Invalid or missing API key'
        }), 401

    try:
        data = request.get_json()

        if not data or 'message' not in data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Missing required field: message'
            }), 400

        conversation_id = data.get(
            'conversation_id',
            f"conv_{datetime.utcnow().timestamp()}"
        )
        incoming_message = data.get('message', '')
        metadata = data.get('metadata', {})

        # Initialize conversation if new
        if conversation_id not in conversation_store:
            conversation_store[conversation_id] = {
                'messages': [],
                'scam_detected': False,
                'agent_activated': False,
                'extracted_intelligence': {},
                'start_time': datetime.utcnow().isoformat(),
                'turn_count': 0
            }

        conversation = conversation_store[conversation_id]

        # Store scammer message
        conversation['messages'].append({
            'role': 'scammer',
            'content': incoming_message,
            'timestamp': datetime.utcnow().isoformat()
        })
        conversation['turn_count'] += 1

        # Scam detection
        if not conversation['scam_detected']:
            scam_analysis = scam_detector.analyze(
                incoming_message,
                conversation['messages']
            )
            if scam_analysis['is_scam']:
                conversation['scam_detected'] = True
                conversation['scam_type'] = scam_analysis['scam_type']
                conversation['confidence'] = scam_analysis['confidence']
                conversation['indicators'] = scam_analysis['indicators']

        # Agent response
        if conversation['scam_detected']:
            conversation['agent_activated'] = True
            agent_response = engagement_agent.generate_response(
                incoming_message=incoming_message,
                conversation_history=conversation['messages'],
                scam_type=conversation.get('scam_type', 'unknown'),
                metadata=metadata
            )
            response_message = agent_response['message']
            strategy = agent_response['strategy']
        else:
            response_message = engagement_agent.generate_initial_response(incoming_message)
            strategy = 'initial_engagement'

        # Store agent message
        conversation['messages'].append({
            'role': 'agent',
            'content': response_message,
            'timestamp': datetime.utcnow().isoformat(),
            'strategy': strategy
        })

        # Intelligence extraction
        extracted_intel = intelligence_extractor.extract(conversation['messages'])
        conversation['extracted_intelligence'].update(extracted_intel)

        # Engagement metrics
        start = datetime.fromisoformat(conversation['start_time'])
        engagement_duration = (datetime.utcnow() - start).total_seconds()

        response = {
            'conversation_id': conversation_id,
            'scam_detection': {
                'detected': conversation['scam_detected'],
                'confidence': conversation.get('confidence', 0.0),
                'scam_type': conversation.get('scam_type', 'none'),
                'indicators': conversation.get('indicators', [])
            },
            'agent_response': {
                'message': response_message,
                'strategy': strategy,
                'agent_activated': conversation['agent_activated']
            },
            'engagement_metrics': {
                'turn_count': conversation['turn_count'],
                'engagement_duration_seconds': round(engagement_duration, 2),
                'intelligence_extracted': len(conversation['extracted_intelligence']) > 0
            },
            'extracted_intelligence': conversation['extracted_intelligence'],
            'timestamp': datetime.utcnow().isoformat()
        }

        # 🔥 SAVE TO JSON FILE
        save_conversations()

        return jsonify(response), 200

    except Exception as e:
        app.logger.error(f"Error processing message: {str(e)}")
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@app.route('/api/v1/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):

    if not verify_api_key(request):
        return jsonify({'error': 'Unauthorized'}), 401

    if conversation_id not in conversation_store:
        return jsonify({'error': 'Conversation not found'}), 404

    return jsonify({
        'conversation_id': conversation_id,
        'conversation': conversation_store[conversation_id]
    }), 200


@app.route('/api/v1/conversations', methods=['GET'])
def list_conversations():

    if not verify_api_key(request):
        return jsonify({'error': 'Unauthorized'}), 401

    summaries = []
    for conv_id, conv in conversation_store.items():
        summaries.append({
            'conversation_id': conv_id,
            'scam_detected': conv['scam_detected'],
            'turn_count': conv['turn_count'],
            'intelligence_count': len(conv['extracted_intelligence']),
            'start_time': conv['start_time']
        })

    return jsonify({
        'total_conversations': len(summaries),
        'conversations': summaries
    }), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
