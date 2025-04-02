import { clsx, type ClassValue } from "clsx" //to conditionally apply class names.
import { twMerge } from "tailwind-merge" //to merge and remove duplicate or conflicting Tailwind classes.
import { Message, TextUIPart } from "./types";

//It simplifies managing and merging Tailwind CSS class names dynamically.
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

//Generates a random UUID (Universally Unique Identifier).
//Useful for creating unique keys for components, messages, etc.
export function generateUUID(): string {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

export function fillMessageParts(messages: Message[]): Message[] {
  return messages.map(message => ({
    ...message,
    parts: getMessageParts(message),
  }));
}

export function getMessageParts(message: Message): (TextUIPart)[] {
  return (
    message.parts ?? [...(message.content ? [{ type: 'text' as const, text: message.content }] : []),]
  );
}