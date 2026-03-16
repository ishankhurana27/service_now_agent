export interface Message {
  id: string
  content: string
  sender: 'user' | 'ai'
  timestamp: Date
}

export interface Chat {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
}

export interface User {
  id: string
  name: string
  email: string
  avatar?: string
}
