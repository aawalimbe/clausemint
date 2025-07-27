# AI Service Setup Guide for Clausemint

This guide will help you set up the AI services needed for Clausemint to work properly.

## 🔍 **Current Issue**
The application is showing "I apologize, but I'm having trouble connecting to the AI service" because the AI service is not properly configured.

## 🚀 **Quick Solutions**

### **Option 1: Use OpenAI (Easiest - 5 minutes)**

1. **Get OpenAI API Key**:
   - Go to https://platform.openai.com/
   - Sign up/Login
   - Go to API Keys section
   - Create a new API key

2. **Configure Environment**:
   ```bash
   # Edit your .env file in backend/
   AI_PROVIDER=openai
   OPENAI_API_KEY=your-openai-api-key-here
   ```

3. **Test the Setup**:
   ```bash
   cd backend
   python test_ai_service.py
   ```

4. **Test Streaming** (Optional but recommended):
   ```bash
   python test_streaming.py
   ```

### **Option 2: Use Mistral AI (Recommended for MVP - 10 minutes)**

1. **Install Ollama**:
   - Download from: https://ollama.ai/
   - Install the application
   - Start Ollama (it should run automatically)

2. **Pull Mistral Model**:
   ```bash
   ollama pull mistral
   ```

3. **Verify Installation**:
   ```bash
   ollama list
   # Should show: mistral:latest
   ```

4. **Test the Setup**:
   ```bash
   cd backend
   python test_ai_service.py
   ```

5. **Test Streaming** (Optional but recommended):
   ```bash
   python test_streaming.py
   ```

## 🔧 **Detailed Setup Instructions**

### **For OpenAI Users:**

1. **Environment Configuration**:
   ```bash
   # In backend/.env file
   AI_PROVIDER=openai
   OPENAI_API_KEY=sk-your-actual-api-key-here
   MISTRAL_API_KEY=local
   MISTRAL_BASE_URL=http://localhost:11434
   ```

2. **Cost Considerations**:
   - OpenAI charges per token used
   - NDA generation typically costs $0.01-$0.05 per document
   - Set up billing limits in OpenAI dashboard

### **For Mistral AI Users:**

1. **Install Ollama**:
   - **Windows**: Download installer from https://ollama.ai/
   - **macOS**: `brew install ollama`
   - **Linux**: `curl -fsSL https://ollama.ai/install.sh | sh`

2. **Start Ollama Service**:
   ```bash
   ollama serve
   ```

3. **Download Mistral Model**:
   ```bash
   ollama pull mistral
   ```

4. **Environment Configuration**:
   ```bash
   # In backend/.env file
   AI_PROVIDER=mistral
   OPENAI_API_KEY=your-openai-api-key-here  # Optional fallback
   MISTRAL_API_KEY=local
   MISTRAL_BASE_URL=http://localhost:11434
   ```

## 🧪 **Testing Your Setup**

Run the diagnostic script:
```bash
cd backend
python test_ai_service.py
```

**Expected Output for Success:**
```
🔍 AI Service Connectivity Test
==================================================
Current AI Provider: mistral
📡 Testing Connection...
Status: connected
🧪 Testing AI Generation...
✅ AI Response: Hello, AI is working!
==================================================
Test completed!
```

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **"Ollama is not running"**:
   - Start Ollama: `ollama serve`
   - Check if it's running: `curl http://localhost:11434/api/tags`

2. **"OpenAI API key not configured"**:
   - Add your API key to `.env` file
   - Restart the Django server

3. **"Connection timeout"**:
   - Check your internet connection
   - Verify firewall settings
   - Try switching providers

### **Provider Switching:**

To switch between providers:
```bash
# Switch to OpenAI
AI_PROVIDER=openai

# Switch to Mistral
AI_PROVIDER=mistral
```

## 💡 **Recommendations**

### **For Development/MVP:**
- Use **Mistral AI** (free, local, no API costs)
- Install Ollama and pull the mistral model
- **Streaming is enabled by default** - provides real-time feedback

### **For Production:**
- Use **OpenAI** (more reliable, better performance)
- Set up proper API key management
- Monitor usage and costs

### **For Testing:**
- Use the diagnostic script to verify setup
- Test with simple NDA generation first
- Test streaming functionality: `python test_streaming.py`

## 🚀 **Streaming Benefits**

### **Why Streaming?**
- **No Timeout Issues**: Eliminates 60-second timeout problems
- **Real-time Feedback**: Users see AI generating text live
- **Better UX**: Loading animations with actual progress
- **Handles Slow Systems**: Works even on slower hardware
- **First Request Friendly**: No more "first request timeout" issues
- **Universal Solution**: Works for all AI providers (Mistral, OpenAI, Llama, etc.)

### **How It Works:**
1. **Frontend** sends request to streaming endpoints (e.g., `/api/nda/generate/streaming/`)
2. **Backend** streams response chunks in real-time using Server-Sent Events (SSE)
3. **Frontend** displays progress as AI generates text
4. **User** sees document being created live

### **Streaming Endpoints Available:**
- **NDA Generation**: `/api/nda/generate/streaming/`
- **Chat Messages**: `/api/chat/streaming/`
- **Document Analysis**: `/api/redlining/analyze/streaming/`

### **Testing Streaming:**
```bash
cd backend
python test_all_streaming.py
```

## 🔒 **Security Notes**

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Set up billing alerts** for OpenAI usage
4. **Monitor API usage** regularly

## 📞 **Support**

If you're still having issues:

1. Run the diagnostic script: `python test_ai_service.py`
2. Check the logs: `backend/logs/nda_errors.log`
3. Verify your `.env` file configuration
4. Ensure all dependencies are installed: `pip install -r requirements.txt`

---

**Next Steps:** Once AI is working, you can test the NDA generation feature with the loading animations and Word document download! 