import React, { useState, useRef, useEffect } from 'react'
import { Send, Paperclip, Bot, User, Menu, LogOut } from 'lucide-react'
import { Chat } from '../types'
import MessageBubble from './MessageBubble'
import { sendMessageToBackend } from "../utils/chatUtils"

interface ChatAreaProps {
  chat: Chat | undefined
  onSendMessage: (content: string) => void
  onReceiveMessage: (content: string) => void
  onToggleSidebar?: () => void
}

const ChatArea: React.FC<ChatAreaProps> = ({
  chat,
  onSendMessage,
  onReceiveMessage,
  onToggleSidebar
}) => {
  const [inputValue, setInputValue] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const [isProfileOpen, setIsProfileOpen] = useState(false)

  // ✅ NEW: reset-session flag
  const [resetSession, setResetSession] = useState(false)

  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const profileRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [chat?.messages])

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (profileRef.current && !profileRef.current.contains(event.target as Node)) {
        setIsProfileOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return

    const messageContent = inputValue.trim()
    setInputValue('')

    onSendMessage(messageContent)
    setIsTyping(true)

    try {
      // ✅ CHANGED: pass resetSession flag
      const data = await sendMessageToBackend(messageContent, resetSession)

      // reset flag AFTER sending
      setResetSession(false)

      const articleHeader = data.article_id
        ? `📄 **Locked Article:** ${data.article_id}\n\n`
        : ""

      onReceiveMessage(articleHeader + data.answer)
    } catch (error) {
      onReceiveMessage("Error: could not reach backend")
    } finally {
      setIsTyping(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value)
    const textarea = e.target
    textarea.style.height = 'auto'
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px'
  }

  if (!chat) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <Bot className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-xl font-medium text-gray-500 mb-2">No chat selected</h3>
          <p className="text-gray-400">Select a chat from the sidebar or create a new one</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 flex flex-col h-full">

      {/* Header */}
      <div className="bg-white border-b px-6 py-4">
        <div className="flex items-center gap-3">
          <button onClick={onToggleSidebar} className="lg:hidden">
            <Menu />
          </button>
          <Bot />
          <h2 className="font-semibold">{chat.title}</h2>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4 bg-gray-50">
        {chat.messages.map((message) => (
          <MessageBubble key={message.id} message={message} />
        ))}

        {isTyping && (
          <div className="text-gray-400 text-sm">AI is typing...</div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* ✅ NEW: Reset session controls */}
      <div className="px-6 pb-2 text-sm text-gray-600 flex items-center gap-3">
        <span>Start a new session?</span>
        <button
          className="px-2 py-1 bg-green-600 text-white rounded"
          onClick={() => setResetSession(true)}
        >
          Yes
        </button>
        <button
          className="px-2 py-1 bg-gray-400 text-white rounded"
          onClick={() => setResetSession(false)}
        >
          No
        </button>
      </div>

      {/* Input */}
      <div className="p-6 bg-white">
        <textarea
          ref={inputRef}
          value={inputValue}
          onChange={handleInputChange}
          onKeyPress={handleKeyPress}
          placeholder="Type your message here..."
          className="w-full border rounded-xl p-4"
          rows={1}
        />
        {inputValue.trim() && (
          <button onClick={handleSendMessage} className="mt-2">
            <Send />
          </button>
        )}
      </div>
    </div>
  )
}

export default ChatArea
