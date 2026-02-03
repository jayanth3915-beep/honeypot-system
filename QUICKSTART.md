# Quick Start Guide - 5 Minutes to Deployment

## ⚡ Fastest Path to Deployment

### Step 1: Get the Code (30 seconds)
Download all files to a folder called `honeypot-system`

### Step 2: Choose Your Deployment (Pick One)

#### Option A: Render.com (Easiest - Recommended)
1. Go to https://render.com → Sign up
2. Click "New +" → "Web Service"
3. Choose "Deploy from GitHub" or upload your repo
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Add Environment Variable:
   - **Key**: `HONEYPOT_API_KEY`
   - **Value**: Your secret key (e.g., `my-secure-key-12345`)
6. Click "Create Web Service"
7. Wait 2 minutes ⏱️
8. Copy your URL: `https://your-app.onrender.com`

✅ **DONE! Your API is live!**

#### Option B: Railway.app (CLI - Fast)
```bash
# Install Railway
npm i -g @railway/cli

# Deploy
cd honeypot-system
railway login
railway init
railway variables set HONEYPOT_API_KEY=your-secret-key
railway up

# Get URL
railway domain
```

✅ **DONE in 2 minutes!**

### Step 3: Test Your Deployment (1 minute)

```bash
# Test health
curl https://your-deployment-url.com/health

# Test scam detection
curl -X POST https://your-deployment-url.com/api/v1/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-secret-key" \
  -d '{
    "conversation_id": "test_001",
    "message": "Dear customer, your bank account will be blocked. Update KYC now: http://fake.com"
  }'
```

Expected response: JSON with scam detection and agent response.

✅ **If you see JSON, you're ready!**

---

## 🔧 Local Testing (Optional)

```bash
# Install
pip install -r requirements.txt

# Set key
export HONEYPOT_API_KEY="test-key-123"

# Run
python app.py

# Test (in another terminal)
curl http://localhost:5000/health
```

---

## 📋 What You Need to Submit

1. **Your Public API URL**: `https://your-app.render.com` or `https://your-app.railway.app`
2. **Your API Key**: The value you set for `HONEYPOT_API_KEY`

---

## 🎯 API Endpoint

Your submission endpoint:
```
POST https://your-deployment-url.com/api/v1/message
```

Headers:
```
Content-Type: application/json
X-API-Key: your-secret-key
```

Body:
```json
{
  "conversation_id": "conv_id",
  "message": "scammer message here"
}
```

---

## 🚨 Troubleshooting

**"Application Error":**
- Check logs in your platform dashboard
- Verify `requirements.txt` is present
- Ensure environment variable is set

**"Unauthorized":**
- Check your API key is correct
- Try header: `Authorization: Bearer your-key` instead

**"Service Unavailable":**
- Platform might be deploying (wait 1-2 minutes)
- Check platform status page

---

## 📞 Need Help?

1. Check the full README.md
2. See DEPLOYMENT.md for detailed guides
3. Review API_EXAMPLES.md for response formats

---

## ✅ Checklist

- [ ] Code deployed to cloud platform
- [ ] Environment variable `HONEYPOT_API_KEY` set
- [ ] Health endpoint returns 200 OK
- [ ] Test message processed successfully
- [ ] URL and API key ready for submission

**Time to complete: ~5 minutes** ⚡

**You're ready to catch scammers!** 🎣
