import React, { useState, useEffect, useRef } from 'react'
import { Plus, MessageSquare, User, Settings, Bot, MoreVertical, Menu, X, LogOut, Trash2, Sun, Moon, Monitor, Search } from 'lucide-react'
import { Chat } from '../types'

interface SidebarProps {
  chats: Chat[]
  currentChatId: string
  onChatSelect: (chatId: string) => void
  onCreateNewChat: () => void
  onUpdateChatTitle: (chatId: string, title: string) => void
  isOpen: boolean
  onClose: () => void
  onToggle: () => void
  isCollapsed?: boolean
}

const Sidebar: React.FC<SidebarProps> = ({
  chats,
  currentChatId,
  onChatSelect,
  onCreateNewChat,
  onUpdateChatTitle,
  isOpen,
  onClose,
  onToggle,
  isCollapsed = false
}) => {
  const [editingChatId, setEditingChatId] = useState<string | null>(null)
  const [editingTitle, setEditingTitle] = useState('')
  const [menuOpenChatId, setMenuOpenChatId] = useState<string | null>(null)
  const [isSettingsOpen, setIsSettingsOpen] = useState(false)
  const [theme, setTheme] = useState<'light' | 'dark' | 'system'>('light')
  const [searchQuery, setSearchQuery] = useState('')
  const settingsRef = useRef<HTMLDivElement>(null)

  const handleEditTitle = (chat: Chat) => {
    setEditingChatId(chat.id)
    setEditingTitle(chat.title)
  }

  const handleSaveTitle = (chatId: string) => {
    if (editingTitle.trim()) {
      onUpdateChatTitle(chatId, editingTitle.trim())
    }
    setEditingChatId(null)
    setEditingTitle('')
  }

  const handleCancelEdit = () => {
    setEditingChatId(null)
    setEditingTitle('')
  }

  const handleThemeChange = (newTheme: 'light' | 'dark' | 'system') => {
    setTheme(newTheme)
    
    // Apply theme to document
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark')
      document.documentElement.classList.remove('light')
    } else if (newTheme === 'light') {
      document.documentElement.classList.add('light')
      document.documentElement.classList.remove('dark')
    } else {
      // System theme
      if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.add('dark')
        document.documentElement.classList.remove('light')
      } else {
        document.documentElement.classList.add('light')
        document.documentElement.classList.remove('dark')
      }
    }
  }

  // Close settings dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (settingsRef.current && !settingsRef.current.contains(event.target as Node)) {
        setIsSettingsOpen(false)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const formatDate = (date: Date) => {
    const now = new Date()
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60)
    
    if (diffInHours < 1) return 'Just now'
    if (diffInHours < 24) return `${Math.floor(diffInHours)}h ago`
    if (diffInHours < 48) return 'Yesterday'
    return date.toLocaleDateString()
  }

  // Filter chats based on search query
  const filteredChats = chats.filter(chat => 
    chat.title.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <>
      {/* Mobile overlay */}
      {isOpen && (
        <div 
          className="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={onClose}
        />
      )}

             {/* Sidebar */}
       <div className={`
         fixed lg:static inset-y-0 left-0 z-50
         bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-600
         transform transition-all duration-300 ease-in-out
         flex flex-col
         ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
         ${isCollapsed ? 'lg:w-20' : 'lg:w-80'}
         w-80
       `}>
                 {/* Header */}
         <div className={`border-b border-gray-200 dark:border-gray-600 flex-shrink-0 ${isCollapsed ? 'lg:p-4' : 'p-6'}`}>
          <div className={`flex items-center ${isCollapsed ? 'lg:justify-center' : 'justify-between'} mb-4`}>
            <div className={`flex items-center ${isCollapsed ? 'lg:justify-center' : 'gap-3'}`}>
              <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-xl flex items-center justify-center">
                <Bot className="w-6 h-6 text-white" />
              </div>
              {!isCollapsed && (
                <div>
                  <h1 className="text-xl font-bold text-gray-900 dark:text-gray-100">AI Chatbot</h1>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Powered by AI</p>
                </div>
              )}
            </div>
            
                         {/* Sidebar Toggle Button (Desktop) */}
             {!isCollapsed && (
               <button
                 onClick={onToggle}
                 className="hidden lg:flex p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                 title="Collapse Sidebar"
               >
                 <Menu className="w-5 h-5" />
               </button>
             )}
             
             {/* Expand Sidebar Button (Desktop - when collapsed) */}
             {isCollapsed && (
               <button
                 onClick={onToggle}
                 className="hidden lg:flex p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                 title="Expand Sidebar"
               >
                 <Menu className="w-5 h-5" />
               </button>
             )}
             
             {/* Close Sidebar Button (Mobile) */}
             <button
               onClick={onClose}
               className="lg:hidden p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
             >
               <X className="w-5 h-5" />
             </button>
          </div>
          
                                                                 {!isCollapsed && (
              <>
                <button
                  onClick={onCreateNewChat}
                  className="w-full bg-primary-500 hover:bg-primary-600 text-white py-3 px-4 rounded-xl font-medium transition-colors duration-200 flex items-center justify-center gap-2 mb-3"
                >
                  <Plus className="w-5 h-5" />
                  New Chat
                </button>
                
                {/* Search Chat Input */}
                <div className="relative">
                                     <input
                     type="text"
                     placeholder="Search chats..."
                     value={searchQuery}
                     onChange={(e) => setSearchQuery(e.target.value)}
                     className="w-full px-3 py-2 pl-9 text-sm bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-500 rounded-lg text-gray-900 dark:text-gray-100 placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary-200 focus:border-primary-400 transition-colors"
                   />
                                     <Search className="absolute left-3 top-2.5 w-4 h-4 text-gray-500 dark:text-gray-400" />
                </div>
              </>
            )}
        </div>

                {/* Chat History */}
        <div className={`flex-1 overflow-y-auto ${isCollapsed ? 'lg:p-2' : 'p-4'}`}>
                     {!isCollapsed && (
                                          <h3 className="text-sm font-semibold text-gray-500 dark:text-gray-300 uppercase tracking-wider mb-3">
                 Recent Chats
               </h3>
           )}
          
                     <div className="space-y-2">
             {filteredChats.length === 0 && searchQuery ? (
                                                <div className="text-center py-4">
                   <p className="text-sm text-gray-500 dark:text-gray-300">No chats found</p>
                 </div>
             ) : (
               filteredChats.map((chat) => (
              <div
                key={chat.id}
                className={`
                  sidebar-item ${chat.id === currentChatId ? 'sidebar-item-active' : ''}
                  ${isCollapsed ? 'lg:justify-center lg:px-2' : ''}
                `}
                onClick={() => onChatSelect(chat.id)}
                title={isCollapsed ? chat.title : undefined}
              >
                                 <MessageSquare className="w-5 h-5 text-gray-500 dark:text-gray-400" />
                
                {!isCollapsed && editingChatId === chat.id ? (
                  <div className="flex-1 flex items-center gap-2">
                                                                  <input
                           type="text"
                           value={editingTitle}
                           onChange={(e) => setEditingTitle(e.target.value)}
                           onKeyDown={(e) => {
                             if (e.key === 'Enter') handleSaveTitle(chat.id)
                             if (e.key === 'Escape') handleCancelEdit()
                           }}
                           className="flex-1 px-2 py-1 text-sm border border-gray-300 dark:border-gray-500 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded focus:outline-none focus:ring-1 focus:ring-primary-500"
                           autoFocus
                         />
                                         <button
                       onClick={() => handleSaveTitle(chat.id)}
                       className="text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 text-sm"
                     >
                       Save
                     </button>
                     <button
                       onClick={handleCancelEdit}
                       className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 text-sm"
                     >
                       Cancel
                     </button>
                  </div>
                ) : !isCollapsed ? (
                  <div className="flex-1 min-w-0">
                                         <div className="flex items-center justify-between">
                       <p className="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
                         {chat.title}
                       </p>
                                           <div className="relative">
                                               <button
                          onClick={(e) => {
                            e.stopPropagation()
                            setMenuOpenChatId(menuOpenChatId === chat.id ? null : chat.id)
                          }}
                          className="text-gray-400 dark:text-gray-500 hover:text-gray-600 dark:hover:text-gray-300 p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                        >
                          <MoreVertical className="w-4 h-4" />
                        </button>
                       
                                               {/* Dropdown Menu */}
                        {menuOpenChatId === chat.id && (
                                                     <div className="absolute right-0 top-8 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-500 rounded-lg shadow-lg py-1 min-w-[120px] z-10">
                                                           <button
                                 onClick={(e) => {
                                   e.stopPropagation()
                                   handleEditTitle(chat)
                                   setMenuOpenChatId(null)
                                 }}
                                 className="w-full px-3 py-2 text-left text-sm text-gray-700 dark:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                               >
                                 Edit
                               </button>
                               <button
                                 onClick={(e) => {
                                   e.stopPropagation()
                                   // Add delete functionality here if needed
                                   setMenuOpenChatId(null)
                                 }}
                                 className="w-full px-3 py-2 text-left text-sm text-red-400 hover:bg-red-900 dark:hover:bg-red-900 transition-colors"
                               >
                                 Delete
                               </button>
                            </div>
                          )}
                       </div>
                    </div>
                                         <p className="text-xs text-gray-500 dark:text-gray-400">
                       {formatDate(chat.createdAt)}
                     </p>
                  </div>
                                 ) : null}
               </div>
             ))
             )}
           </div>
        </div>

                 {/* Footer - Always at bottom */}
         <div className={`border-t border-gray-200 dark:border-gray-600 flex-shrink-0 mt-auto ${isCollapsed ? 'lg:p-2' : 'p-4'}`}>
          <div className="space-y-2">
            <div className="relative" ref={settingsRef}>
              <button 
                onClick={() => setIsSettingsOpen(!isSettingsOpen)}
                className={`sidebar-item w-full ${isCollapsed ? 'lg:justify-center lg:px-2' : 'justify-start'}`} 
                title={isCollapsed ? 'Settings' : undefined}
              >
                <Settings className="w-5 h-5" />
                {!isCollapsed && 'Settings'}
              </button>
              
                             {/* Settings Dropdown */}
               {isSettingsOpen && !isCollapsed && (
                                   <div className="absolute bottom-full left-0 mb-2 w-64 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-500 rounded-xl shadow-lg py-2 z-50">
                  {/* Account Section */}
                                     <div className="px-4 py-2">
                                           <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase tracking-wider mb-2">Account</h3>
                                           <button className="w-full flex items-center gap-3 px-3 py-2 text-left text-gray-200 dark:text-gray-200 hover:bg-gray-700 dark:hover:bg-gray-700 rounded-lg transition-colors duration-150">
                        <LogOut className="w-4 h-4 text-red-400" />
                        <span className="text-sm font-medium text-red-400">Logout</span>
                      </button>
                      <button className="w-full flex items-center gap-3 px-3 py-2 text-left text-gray-200 dark:text-gray-200 hover:bg-gray-700 dark:hover:bg-gray-700 rounded-lg transition-colors duration-150">
                        <Trash2 className="w-4 h-4 text-red-400" />
                        <span className="text-sm font-medium text-red-400">Delete Account</span>
                      </button>
                   </div>
                  
                                     <div className="border-t border-gray-100 dark:border-gray-600 my-1"></div>
                   
                   {/* Theme Section */}
                   <div className="px-4 py-2">
                                           <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase tracking-wider mb-2">Theme</h3>
                     <button 
                       onClick={() => handleThemeChange('light')}
                       className={`w-full flex items-center gap-3 px-3 py-2 text-left rounded-lg transition-colors duration-150 ${
                         theme === 'light' 
                           ? 'bg-primary-50 dark:bg-primary-900 text-primary-700 dark:text-primary-300' 
                           : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                       }`}
                     >
                       <Sun className="w-4 h-4" />
                       <span className="text-sm font-medium">Light</span>
                     </button>
                     <button 
                       onClick={() => handleThemeChange('dark')}
                       className={`w-full flex items-center gap-3 px-3 py-2 text-left rounded-lg transition-colors duration-150 ${
                         theme === 'dark' 
                           ? 'bg-primary-50 dark:bg-primary-900 text-primary-700 dark:text-primary-300' 
                           : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                       }`}
                     >
                       <Moon className="w-4 h-4" />
                       <span className="text-sm font-medium">Dark</span>
                     </button>
                     <button 
                       onClick={() => handleThemeChange('system')}
                       className={`w-full flex items-center gap-3 px-3 py-2 text-left rounded-lg transition-colors duration-150 ${
                         theme === 'system' 
                           ? 'bg-primary-50 dark:bg-primary-900 text-primary-700 dark:text-primary-300' 
                           : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'
                       }`}
                     >
                       <Monitor className="w-4 h-4" />
                       <span className="text-sm font-medium">System Default</span>
                     </button>
                   </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default Sidebar
