import axios from "axios";
import { Message } from "@/lib/types";
import { generateUUID } from "@/lib/utils";

const apiUrl = `${process.env.NEXT_PUBLIC_API_URL}/chat`;

export const streamChat = async ({
    inputContent,
    setIsLoading,
    append,
}: {
    inputContent: string;
    setIsLoading: (isLoading: boolean) => void;
    append: (message: Message) => void;
}) => {
    try {
        setIsLoading(true);

        const response = await axios.post<{ text: string; source: string }>(apiUrl, {
            id: generateUUID(),
            role: "user",
            content: inputContent,
        });

        const text = response.data.text;

        const content: Message = {
            id: generateUUID(),
            content: text,
            role: "assistant",
            parts: [{ type: "text", text }],
        };

        append(content);
    } catch (err) {
        console.error("Error in streamChat:", err);
    } finally {
        setIsLoading(false);
    }
};
