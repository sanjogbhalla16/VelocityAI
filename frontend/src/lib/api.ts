import axios from "axios";
import { Message } from "./types"

//create the client for Axios
export const apiClient = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL,
    headers: {
        "Content-Type": "application/json",
    }
});

export const sendChatMessage = async (message: string) => {
    try {
        const response = await apiClient.post("/chat", {
            query: message
        });

        return response.data;
    }
    catch (error) {
        console.log("Error in sendChatMessage", error);
        throw error
    }
}

export const fetchMessages = async (chatId: string): Promise<Message[]> => {
    const response = await axios.get<Message[]>(`${process.env.NEXT_PUBLIC_API_URL}/${chatId}`);
    return response.data;
};

export const saveMessage = async (chatId: string, message: Message): Promise<void> => {
    await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/${chatId}`, message);
};
