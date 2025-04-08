import axios from "axios";
import { Message } from "./types";
import { v4 as uuidv4 } from "uuid";

// Create the client for Axios
export const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    headers: {
        "Content-Type": "application/json",
    },
});

// ✅ 1. Fixed: Flatten the request body instead of wrapping in { message }
export const sendChatMessage = async (message: Message) => {
    console.log("Sending message to backend:", {
        id: message.id,
        role: message.role,
        content: message.content,
    });
    try {
        const response = await apiClient.post("/chat", {
            id: message.id,
            role: message.role,
            content: message.content,
        });
        return response.data; // { text: "...", source: "..." }
    } catch (error) {
        console.log("Error in sendChatMessage", error);
        throw error;
    }
};


// ✅ 2. Remove chatId from fetchMessages – backend doesn't need it
export const fetchMessages = async (): Promise<Message[]> => {
    const response = await apiClient.get<Message[]>("/chat"); // Only if supported by backend
    return response.data;
};

// ✅ 3. Remove chatId from saveMessage – and flatten message
export const saveMessage = async (message: Message): Promise<void> => {
    await apiClient.post("/chat", message);
};
