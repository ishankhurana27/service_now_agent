import { useState, useCallback } from 'react'
import { apiService } from '../services/api'

interface UseApiState<T> {
  data: T | null
  loading: boolean
  error: string | null
}

interface UseApiReturn<T> extends UseApiState<T> {
  execute: (...args: any[]) => Promise<T | null>
  reset: () => void
}

export function useApi<T>(
  apiFunction: (...args: any[]) => Promise<T>,
  initialData: T | null = null
): UseApiReturn<T> {
  const [state, setState] = useState<UseApiState<T>>({
    data: initialData,
    loading: false,
    error: null,
  })

  const execute = useCallback(
    async (...args: any[]) => {
      setState(prev => ({ ...prev, loading: true, error: null }))
      
      try {
        const result = await apiFunction(...args)
        setState({ data: result, loading: false, error: null })
        return result
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'An error occurred'
        setState(prev => ({ ...prev, loading: false, error: errorMessage }))
        return null
      }
    },
    [apiFunction]
  )

  const reset = useCallback(() => {
    setState({ data: initialData, loading: false, error: null })
  }, [initialData])

  return {
    ...state,
    execute,
    reset,
  }
}

// Specific hooks for common operations
export function useChatApi() {
  const sendMessage = useApi(apiService.sendMessage.bind(apiService))
  const getChatHistory = useApi(apiService.getChatHistory.bind(apiService))
  const createNewChat = useApi(apiService.createNewChat.bind(apiService))
  const deleteChat = useApi(apiService.deleteChat.bind(apiService))

  return {
    sendMessage,
    getChatHistory,
    createNewChat,
    deleteChat,
  }
}

export function useAuthApi() {
  const login = useApi(apiService.login.bind(apiService))
  const register = useApi(apiService.register.bind(apiService))
  const logout = useApi(apiService.logout.bind(apiService))

  return {
    login,
    register,
    logout,
  }
}
