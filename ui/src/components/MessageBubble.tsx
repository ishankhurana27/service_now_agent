import React, { useState } from 'react'
import { Bot, User, Copy, Edit, Check } from 'lucide-react'
import { Message } from '../types'

interface MessageBubbleProps {
  message: Message
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isUser = message.sender === 'user'
  const [copied, setCopied] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [editValue, setEditValue] = useState(message.content)
  
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy text: ', err)
    }
  }

  const handleEdit = () => {
    setIsEditing(true)
  }

  const handleSaveEdit = () => {
    // Here you would typically call a function to update the message
    // For now, we'll just close the edit mode
    setIsEditing(false)
  }

  const handleCancelEdit = () => {
    setEditValue(message.content)
    setIsEditing(false)
  }

  return (
    <div className={`flex items-start gap-3 animate-slide-up ${isUser ? 'justify-end' : 'justify-start'}`}>
      {/* Avatar */}
      {!isUser && (
        <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-full flex items-center justify-center flex-shrink-0">
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}
      
             {/* Message Bubble */}
       <div className={`max-w-xs lg:max-w-md ${isUser ? 'order-first' : ''}`}>
         {isEditing ? (
           <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-2xl p-3 shadow-sm">
             <textarea
               value={editValue}
               onChange={(e) => setEditValue(e.target.value)}
               className="w-full text-sm border-none outline-none resize-none bg-transparent text-gray-900 dark:text-gray-100"
               rows={Math.max(1, editValue.split('\n').length)}
             />
             <div className="flex gap-2 mt-2">
               <button
                 onClick={handleSaveEdit}
                 className="text-xs px-2 py-1 bg-primary-500 text-white rounded hover:bg-primary-600 transition-colors"
               >
                 Save
               </button>
               <button
                 onClick={handleCancelEdit}
                 className="text-xs px-2 py-1 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors"
               >
                 Cancel
               </button>
             </div>
           </div>
         ) : (
                       <div className="group">
              <div className={`
                chat-bubble ${isUser ? 'chat-bubble-user' : 'chat-bubble-ai'}
                ${isUser ? 'ml-auto' : ''}
              `}>
                <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">
                  {message.content}
                </p>
              </div>
              
              {/* Action Buttons - Below the message */}
              <div className={`flex gap-1 mt-2 ${isUser ? 'justify-end' : 'justify-start'} opacity-0 group-hover:opacity-100 transition-opacity duration-200`}>
                {/* Copy Button */}
                <button
                  onClick={handleCopy}
                  className="p-1 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-gray-100 rounded transition-colors text-xs"
                  title="Copy message"
                >
                  {copied ? <Check className="w-3 h-3 text-green-600" /> : <Copy className="w-3 h-3" />}
                </button>
                
                {/* Edit Button - Only for user messages */}
                {isUser && (
                  <button
                    onClick={handleEdit}
                    className="p-1 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-gray-100 rounded transition-colors text-xs"
                    title="Edit message"
                  >
                    <Edit className="w-3 h-3" />
                  </button>
                )}
              </div>
            </div>
         )}
         
         {/* Timestamp */}
         <div className={`text-xs text-gray-500 dark:text-gray-400 mt-1 ${isUser ? 'text-right' : 'text-left'}`}>
           {formatTime(message.timestamp)}
         </div>
       </div>
      

    </div>
  )
}

export default MessageBubble
