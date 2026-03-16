import { Chat, Message } from "../types"

// ------------------------------
// SESSION HANDLING (RAG CONTEXT)
// ------------------------------
let sessionId: string | null = null

// ------------------------------
// CHAT HELPERS
// ------------------------------
export const generateChatTitle = (firstMessage: string): string => {
  const words = firstMessage.trim().split(" ").slice(0, 4)
  if (words.length === 0) return "New Chat"
  const title = words.join(" ")
  return title.charAt(0).toUpperCase() + title.slice(1)
}

export const updateChatTitle = (
  chats: Chat[],
  chatId: string,
  newTitle: string
): Chat[] => {
  return chats.map(chat =>
    chat.id === chatId ? { ...chat, title: newTitle } : chat
  )
}

export const addMessageToChat = (
  chats: Chat[],
  chatId: string,
  message: Message
): Chat[] => {
  return chats.map(chat =>
    chat.id === chatId
      ? { ...chat, messages: [...chat.messages, message] }
      : chat
  )
}

export const createNewChat = (): Chat => {
  return {
    id: Date.now().toString(),
    title: "New Chat",
    messages: [],
    createdAt: new Date(),
  }
}

export const formatRelativeTime = (date: Date): string => {
  const now = new Date()
  const diffInMs = now.getTime() - date.getTime()
  const diffInMinutes = Math.floor(diffInMs / (1000 * 60))
  const diffInHours = Math.floor(diffInMs / (1000 * 60 * 60))
  const diffInDays = Math.floor(diffInMs / (1000 * 60 * 60 * 24))

  if (diffInMinutes < 1) return "Just now"
  if (diffInMinutes < 60) return `${diffInMinutes}m ago`
  if (diffInHours < 24) return `${diffInHours}h ago`
  if (diffInDays < 7) return `${diffInDays}d ago`
  return date.toLocaleDateString()
}

export const validateMessage = (content: string): boolean => {
  return content.trim().length > 0 && content.trim().length <= 2000
}

export const truncateMessage = (
  content: string,
  maxLength: number = 100
): string => {
  if (content.length <= maxLength) return content
  return content.substring(0, maxLength) + "..."
}

// ------------------------------
// BACKEND CONNECTOR (RAG)
// ------------------------------
export const sendMessageToBackend = async (
  userMessage: string,
  resetSession: boolean = false
) => {
  try {
    // ✅ NEW: clear local session when user requests reset
    if (resetSession) {
      sessionId = null
    }

    const response = await fetch("http://localhost:8000/rag/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: userMessage,        // ✅ backend expects `query`
        session_id: sessionId,     // ✅ reuse or reset session
        reset_session: resetSession // ✅ NEW
      }),
    })

    if (!response.ok) {
      throw new Error(`Backend error: ${response.status}`)
    }

    const data = await response.json()

    // 🔑 Persist session for follow-ups
    if (data.session_id) {
      sessionId = data.session_id
    }

    return {
      answer: data.answer,
      article_id: data.article_id || "",
      intent: data.intent,
      session_id: data.session_id,
    }
  } catch (error) {
    console.error("Error calling backend:", error)
    return {
      answer: "Error: Could not reach backend",
      article_id: "",
      intent: "TEXT",
      session_id: sessionId,
    }
  }
}
1