# Deployment Guide - AI Honeypot System

This guide provides step-by-step instructions for deploying your honeypot system to various cloud platforms.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [ ] All project files in a directory
- [ ] Python 3.8+ installed locally (for testing)
- [ ] Git installed (for some deployment methods)
- [ ] A secure API key chosen
- [ ] Tested the system locally

## 🚀 Quick Start - Local Testing

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
export HONEYPOT_API_KEY="your-secure-api-key-123"
export PORT=5000
```

3. **Run the server:**
```bash
python app.py
```

4. **Test in another terminal:**
```bash
python test_honeypot.py
```

## ☁️ Cloud Deployment Options

### Option 1: Render.com (Recommended - Free Tier Available)

**Steps:**

1. **Create a Render account:**
   - Go to https://render.com
   - Sign up with GitHub or email

2. **Create new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your Git repository OR use "Deploy from GitHub"

3. **Configure the service:**
   - Name: `honeypot-system`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. **Add Environment Variables:**
   - Click "Environment" tab
   - Add: `HONEYPOT_API_KEY` = `your-secret-key`
   - Port is automatically set by Render

5. **Deploy:**
   - Click "Create Web Service"
   - Wait for deployment (2-3 minutes)
   - Your URL will be: `https://honeypot-system.onrender.com`

6. **Test your deployment:**
```bash
curl https://honeypot-system.onrender.com/health
```

---

### Option 2: Railway.app (Easy, Free Tier)

**Steps:**

1. **Install Railway CLI:**
```bash
npm i -g @railway/cli
```

2. **Login:**
```bash
railway login
```

3. **Initialize project:**
```bash
cd your-honeypot-directory
railway init
```

4. **Set environment variables:**
```bash
railway variables set HONEYPOT_API_KEY=your-secret-key
```

5. **Deploy:**
```bash
railway up
```

6. **Get your URL:**
```bash
railway domain
```

Your service will be available at: `https://your-app.railway.app`

---

### Option 3: Heroku (Classic Platform)

**Steps:**

1. **Install Heroku CLI:**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login:**
```bash
heroku login
```

3. **Create app:**
```bash
cd your-honeypot-directory
heroku create honeypot-system-yourname
```

4. **Set environment variables:**
```bash
heroku config:set HONEYPOT_API_KEY=your-secret-key
```

5. **Deploy:**
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

6. **Open your app:**
```bash
heroku open
```

Your URL: `https://honeypot-system-yourname.herokuapp.com`

---

### Option 4: DigitalOcean App Platform

**Steps:**

1. **Create DigitalOcean account:**
   - Go to https://www.digitalocean.com
   - Sign up (you may get free credits)

2. **Create new App:**
   - Go to Apps → Create App
   - Connect GitHub repository

3. **Configure:**
   - Detected as Python app automatically
   - Set environment variable: `HONEYPOT_API_KEY`
   - Set build command: `pip install -r requirements.txt`
   - Set run command: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. **Deploy:**
   - Click "Deploy"
   - Wait 2-3 minutes

Your URL: `https://honeypot-system-xxxxx.ondigitalocean.app`

---

### Option 5: AWS EC2 (For Production)

**Steps:**

1. **Launch EC2 Instance:**
   - Ubuntu 22.04 LTS
   - t2.micro (free tier)
   - Configure security group: Allow ports 22, 80, 443

2. **Connect to instance:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Python and dependencies:**
```bash
sudo apt update
sudo apt install python3 python3-pip nginx -y
```

4. **Upload your code:**
```bash
# On your local machine
scp -i your-key.pem -r honeypot-system ubuntu@your-ec2-ip:~/
```

5. **Setup on server:**
```bash
cd honeypot-system
pip3 install -r requirements.txt
export HONEYPOT_API_KEY="your-secret-key"
```

6. **Run with Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app --daemon
```

7. **Configure Nginx (optional but recommended):**
```nginx
# /etc/nginx/sites-available/honeypot
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/honeypot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

### Option 6: Google Cloud Run (Serverless)

**Steps:**

1. **Install Google Cloud SDK:**
```bash
# Follow: https://cloud.google.com/sdk/docs/install
```

2. **Create Dockerfile:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD exec gunicorn --bind :$PORT app:app
```

3. **Build and deploy:**
```bash
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/honeypot
gcloud run deploy honeypot \
  --image gcr.io/YOUR_PROJECT_ID/honeypot \
  --platform managed \
  --region us-central1 \
  --set-env-vars HONEYPOT_API_KEY=your-secret-key
```

---

## 🔐 Security Best Practices

1. **Use Strong API Keys:**
```bash
# Generate secure key
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. **Enable HTTPS:**
   - Most platforms (Render, Railway, Heroku) provide HTTPS automatically
   - For EC2/VPS, use Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

3. **Environment Variables:**
   - Never commit `.env` file to Git
   - Always use platform's secret management

4. **Rate Limiting (Optional):**
```python
from flask_limiter import Limiter
limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/api/v1/message')
@limiter.limit("100 per hour")
def handle_message():
    # ...
```

---

## 🧪 Testing Your Deployment

1. **Health Check:**
```bash
curl https://your-deployment-url.com/health
```

2. **Send Test Message:**
```bash
curl -X POST https://your-deployment-url.com/api/v1/message \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "conversation_id": "test_001",
    "message": "Your account will expire. Click: http://fake.com"
  }'
```

3. **Run Full Test Suite:**
```bash
python test_honeypot.py
# Enter your deployment URL when prompted
```

---

## 📊 Monitoring

### View Logs:

**Render:**
```bash
# In Render dashboard → Logs tab
```

**Railway:**
```bash
railway logs
```

**Heroku:**
```bash
heroku logs --tail
```

**DigitalOcean:**
```bash
# In App Platform → Runtime Logs
```

---

## 🔄 Updating Your Deployment

### For Git-based platforms (Render, Railway, Heroku):
```bash
git add .
git commit -m "Update scam detection patterns"
git push
# Automatic deployment triggered
```

### For manual deployments:
1. SSH to server
2. Pull changes
3. Restart service

---

## 🚨 Troubleshooting

### Common Issues:

1. **"Application Error" or 503:**
   - Check logs for errors
   - Verify all dependencies are installed
   - Ensure PORT environment variable is set

2. **"Unauthorized" errors:**
   - Verify API key is set correctly
   - Check header format: `X-API-Key` or `Authorization: Bearer`

3. **Timeouts:**
   - Increase worker timeout: `gunicorn app:app --timeout 120`
   - Check if server is overloaded

4. **Module not found:**
   - Ensure `requirements.txt` includes all dependencies
   - Run: `pip install -r requirements.txt`

---

## 📞 Platform Support

- **Render**: https://render.com/docs
- **Railway**: https://docs.railway.app
- **Heroku**: https://devcenter.heroku.com
- **DigitalOcean**: https://docs.digitalocean.com
- **AWS**: https://docs.aws.amazon.com
- **Google Cloud**: https://cloud.google.com/docs

---

## ✅ Post-Deployment Checklist

- [ ] Health endpoint responding
- [ ] API authentication working
- [ ] Test scam message processed successfully
- [ ] Intelligence extraction working
- [ ] Multi-turn conversations functioning
- [ ] Logs accessible
- [ ] HTTPS enabled
- [ ] API key secured
- [ ] URL registered with Mock Scammer API

---

**Your honeypot system is now ready to catch scammers! 🎣**
