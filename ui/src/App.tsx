import React, { useState } from 'react'
import Sidebar from './components/Sidebar'
import ChatArea from './components/ChatArea'
import AuthWrapper from './components/AuthWrapper'
import { Chat, Message } from './types'

function App() {
  const [chats, setChats] = useState<Chat[]>([
    {
      id: '1',
      title: 'General Chat',
      messages: [
        {
          id: '1',
          content: 'Hello! How can I help you today?',
          sender: 'ai',
          timestamp: new Date(Date.now() - 60000)
        }
      ],
      createdAt: new Date(Date.now() - 300000)
    }
  ])
  
  const [currentChatId, setCurrentChatId] = useState<string>('1')
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false)

  const currentChat = chats.find(chat => chat.id === currentChatId)

  const createNewChat = () => {
    const newChat: Chat = {
      id: Date.now().toString(),
      title: 'New Chat',
      messages: [],
      createdAt: new Date()
    }
    setChats(prev => [newChat, ...prev])
    setCurrentChatId(newChat.id)
  }

  const addMessage = (content: string, sender: 'user' | 'ai') => {
    if (!currentChat) return

    const newMessage: Message = {
      id: Date.now().toString(),
      content,
      sender,
      timestamp: new Date()
    }

    setChats(prev => prev.map(chat => 
      chat.id === currentChatId 
        ? { ...chat, messages: [...chat.messages, newMessage] }
        : chat
    ))
  }

  const updateChatTitle = (chatId: string, title: string) => {
    setChats(prev => prev.map(chat => 
      chat.id === chatId ? { ...chat, title } : chat
    ))
  }

  return (
    <AuthWrapper>
      <div className="flex h-screen bg-gray-50">
        {/* Mobile sidebar toggle */}
        <button
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          className="lg:hidden fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-md"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        {/* Sidebar */}
        <Sidebar
          chats={chats}
          currentChatId={currentChatId}
          onChatSelect={setCurrentChatId}
          onCreateNewChat={createNewChat}
          onUpdateChatTitle={updateChatTitle}
          isOpen={isSidebarOpen}
          onClose={() => setIsSidebarOpen(false)}
          onToggle={() => {
            if (window.innerWidth >= 1024) {
              // Desktop: toggle collapsed state
              setIsSidebarCollapsed(!isSidebarCollapsed)
            } else {
              // Mobile: toggle open/close state
              setIsSidebarOpen(!isSidebarOpen)
            }
          }}
          isCollapsed={isSidebarCollapsed}
        />

        {/* Main Chat Area */}
        <div className="flex-1 flex flex-col">
          <ChatArea
            chat={currentChat}
            onSendMessage={(content) => addMessage(content, 'user')}
            onReceiveMessage={(content) => addMessage(content, 'ai')}
            onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
            onLogout={() => {
              // This will be handled by AuthWrapper
            }}
          />
        </div>
      </div>
    </AuthWrapper>
  )
}

export default App
