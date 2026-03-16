# Backend Integration Guide

This guide explains how to connect your React chatbot frontend with different types of backend APIs.

## Quick Start

1. **Copy the environment file:**
   ```bash
   cp env.example .env.local
   ```

2. **Update the API URL in `.env.local`:**
   ```env
   VITE_API_BASE_URL=http://your-backend-url.com/api
   ```

3. **Your frontend is now ready to connect to any backend!**

## Backend API Requirements

Your backend should implement these endpoints:

### Authentication Endpoints
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration  
- `POST /api/auth/logout` - User logout

### Chat Endpoints
- `POST /api/chat/send` - Send a message
- `GET /api/chat/{chatId}/history` - Get chat history
- `POST /api/chat/create` - Create new chat
- `DELETE /api/chat/{chatId}` - Delete chat

### Health Check
- `GET /api/health` - Backend health status

## Backend Examples

### 1. Python FastAPI Backend

```python
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageRequest(BaseModel):
    message: str
    chatId: str = None

class ChatResponse(BaseModel):
    id: str
    content: str
    timestamp: str

@app.post("/api/chat/send")
async def send_message(request: MessageRequest):
    # Your AI logic here
    ai_response = f"AI processed: {request.message}"
    
    return {
        "success": True,
        "data": {
            "id": "msg_123",
            "content": ai_response,
            "timestamp": "2024-01-01T12:00:00Z"
        }
    }

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. Node.js Express Backend

```javascript
const express = require('express');
const cors = require('cors');
const app = express();

app.use(cors({
  origin: 'http://localhost:3000' // Your React dev server
}));
app.use(express.json());

app.post('/api/chat/send', (req, res) => {
  const { message, chatId } = req.body;
  
  // Your AI logic here
  const aiResponse = `AI processed: ${message}`;
  
  res.json({
    success: true,
    data: {
      id: 'msg_123',
      content: aiResponse,
      timestamp: new Date().toISOString()
    }
  });
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.listen(8000, () => {
  console.log('Backend running on port 8000');
});
```

### 3. Azure Functions Backend

```typescript
import { AzureFunction, Context, HttpRequest } from "@azure/functions"

const httpTrigger: AzureFunction = async function (context: Context, req: HttpRequest): Promise<void> {
    const { message, chatId } = req.body;
    
    // Your AI logic here
    const aiResponse = `AI processed: ${message}`;
    
    context.res = {
        status: 200,
        body: {
            success: true,
            data: {
                id: 'msg_123',
                content: aiResponse,
                timestamp: new Date().toISOString()
            }
        }
    };
};

export default httpTrigger;
```

## Environment Variables

### Development
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### Production
```env
VITE_API_BASE_URL=https://your-production-api.com/api
```

### Azure Deployment
```env
VITE_API_BASE_URL=https://your-azure-function.azurewebsites.net/api
```

## CORS Configuration

Your backend must allow requests from your frontend domain:

### FastAPI
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Express
```javascript
app.use(cors({
  origin: ['https://yourdomain.com', 'http://localhost:3000'],
  credentials: true
}));
```

## Error Handling

The frontend automatically handles:
- Network errors
- HTTP status errors
- API response errors
- Authentication failures

## Testing Your Integration

1. **Start your backend server**
2. **Update `.env.local` with your backend URL**
3. **Start your React app:**
   ```bash
   npm run dev
   ```
4. **Send a message in the chat**
5. **Check browser console for API calls**

## Troubleshooting

### Common Issues:

1. **CORS Error**: Backend not allowing frontend domain
2. **404 Error**: API endpoints not matching expected paths
3. **Authentication Error**: Missing or invalid auth tokens
4. **Network Error**: Backend server not running or wrong URL

### Debug Steps:

1. Check browser Network tab for failed requests
2. Verify backend server is running
3. Confirm API endpoints match exactly
4. Check CORS configuration
5. Verify environment variables are loaded

## Security Considerations

1. **HTTPS in Production**: Always use HTTPS for production APIs
2. **Authentication**: Implement proper JWT or session-based auth
3. **Rate Limiting**: Add rate limiting to prevent abuse
4. **Input Validation**: Validate all incoming messages
5. **API Keys**: Use environment variables for sensitive data

## Next Steps

1. Choose your backend technology
2. Implement the required API endpoints
3. Test with the frontend
4. Deploy both frontend and backend
5. Monitor and optimize performance
