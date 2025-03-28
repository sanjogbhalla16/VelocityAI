import { atom } from "recoil";

export interface Message {
    role: "user" | "bot";
    content: string;
}

export const chatState = atom<Message[]>({
    key: "chatState",
    default: [],
});