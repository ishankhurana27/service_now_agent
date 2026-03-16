import { Message, Chat, User } from '../types'

// API Configuration
const API_BASE_URL = "http://localhost:8000/"

// API Response Types
interface ApiResponse<T> {
  data: T
  message?: string
  success: boolean
}

// API Service Class
class ApiService {
  private baseURL: string
  private authToken: string | null = null

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
    // Get token from localStorage if available
    this.authToken = localStorage.getItem('authToken')
  }

  // Set authentication token
  setAuthToken(token: string) {
    this.authToken = token
    localStorage.setItem('authToken', token)
  }

  // Clear authentication token
  clearAuthToken() {
    this.authToken = null
    localStorage.removeItem('authToken')
  }

  // Generic request method
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    // Add auth token if available
    if (this.authToken) {
      headers.Authorization = `Bearer ${this.authToken}`
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // Chat API Methods
  async sendMessage(message: string, chatId?: string): Promise<Message> {
    const response = await this.request<Message>('/chat/send', {
      method: 'POST',
      body: JSON.stringify({
        message,
        chatId,
      }),
    })
    return response.data
  }

  async getChatHistory(chatId: string): Promise<Message[]> {
    const response = await this.request<Message[]>(`/chat/${chatId}/history`)
    return response.data
  }

  async createNewChat(): Promise<Chat> {
    const response = await this.request<Chat>('/chat/create', {
      method: 'POST',
    })
    return response.data
  }

  async deleteChat(chatId: string): Promise<void> {
    await this.request<void>(`/chat/${chatId}`, {
      method: 'DELETE',
    })
  }

  // Authentication Methods
  async login(email: string, password: string): Promise<{ token: string; user: User }> {
    const response = await this.request<{ token: string; user: User }>('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    
    if (response.success) {
      this.setAuthToken(response.data.token)
    }
    
    return response.data
  }

  async register(email: string, password: string, name: string): Promise<{ token: string; user: User }> {
    const response = await this.request<{ token: string; user: User }>('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    })
    
    if (response.success) {
      this.setAuthToken(response.data.token)
    }
    
    return response.data
  }

  async logout(): Promise<void> {
    try {
      await this.request('/auth/logout', { method: 'POST' })
    } finally {
      this.clearAuthToken()
    }
  }

  // Health check
  async healthCheck(): Promise<boolean> {
    try {
      await this.request('/health')
      return true
    } catch {
      return false
    }
  }
}

// Create and export a singleton instance
export const apiService = new ApiService()

// Export the class for testing or custom instances
export default ApiService
