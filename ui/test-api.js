// Simple test script to verify your backend API
// Run this with: node test-api.js

const API_BASE_URL = 'http://localhost:8000/api';

async function testAPI() {
  console.log('🧪 Testing API endpoints...\n');

  try {
    // Test health check
    console.log('1. Testing health check...');
    const healthResponse = await fetch(`${API_BASE_URL}/health`);
    if (healthResponse.ok) {
      const healthData = await healthResponse.json();
      console.log('✅ Health check passed:', healthData);
    } else {
      console.log('❌ Health check failed:', healthResponse.status);
    }

    // Test send message
    console.log('\n2. Testing send message...');
    const messageResponse = await fetch(`${API_BASE_URL}/chat/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: 'Hello, this is a test message!',
        chatId: 'test-chat-123'
      })
    });

    if (messageResponse.ok) {
      const messageData = await messageResponse.json();
      console.log('✅ Send message passed:', messageData);
    } else {
      const errorText = await messageResponse.text();
      console.log('❌ Send message failed:', messageResponse.status, errorText);
    }

  } catch (error) {
    console.log('❌ API test failed:', error.message);
    console.log('\n💡 Make sure your backend server is running on port 8000');
    console.log('💡 Check that CORS is properly configured');
  }
}

// Run the test
testAPI();
