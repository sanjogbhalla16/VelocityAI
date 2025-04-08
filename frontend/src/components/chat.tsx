"use client";
import { ChatInput } from "@/components/chat-input";
import { Message } from "@/lib/types";
import { fillMessageParts, generateUUID } from "@/lib/utils";
import { useCallback, useEffect, useRef, useState } from "react";
import ChatMessage from "./chat-message";
import { streamChat } from "../lib/clients/streamChatClient";
import { sendChatMessage, fetchMessages, saveMessage } from "../lib/api";

export function Chat({ id }: { id: string }) {
  const initialInput = "";
  const [inputContent, setInputContent] = useState<string>(initialInput);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [messages, setMessagesState] = useState<Message[]>([]);

  // ✅ Removed the id from fetchMessages()
  useEffect(() => {
    const loadMessages = async () => {
      const fetched: Message[] = await fetchMessages(); // ✅ no id passed
      setMessagesState(fillMessageParts(fetched));
      messagesRef.current = fetched;
    };
    loadMessages();
  }, []);

  const messagesRef = useRef<Message[]>(messages || []);
  useEffect(() => {
    messagesRef.current = messages || [];
  }, [messages]);

  const setMessages = useCallback(
    (messages: Message[] | ((messages: Message[]) => Message[])) => {
      const newMessages =
        typeof messages === "function"
          ? messages(messagesRef.current)
          : messages;
      const messagesWithParts = fillMessageParts(newMessages);
      setMessagesState(messagesWithParts);
      messagesRef.current = messagesWithParts;
    },
    []
  );

  const append = useCallback(
    async (message: Message) => {
      await saveMessage(message); // ✅ removed id from saveMessage()

      return new Promise<string | null | undefined>((resolve) => {
        setMessages((draft) => {
          const lastMessage = draft[draft.length - 1];

          if (
            lastMessage?.role === "assistant" &&
            message.role === "assistant"
          ) {
            const updatedMessage = {
              ...lastMessage,
              content: lastMessage.content + message.content,
            };

            resolve(updatedMessage.content);
            return [...draft.slice(0, -1), updatedMessage];
          } else {
            resolve(message.content);
            return [...draft, message];
          }
        });
      });
    },
    [setMessages]
  );

  const appendAndTrigger = useCallback(
    async (message: Message) => {
      const inputContent: string = message.content;
      await append(message);
      await sendChatMessage(message); // optional
      return await streamChat({ inputContent, setIsLoading, append });
    },
    [setIsLoading, append]
  );

  const handleInputChange = (e: any) => {
    setInputContent(e.target.value);
  };

  const handleSubmit = useCallback(
    async (event?: { preventDefault?: () => void }) => {
      event?.preventDefault?.();

      if (!inputContent) return;

      const newMessage: Message = {
        id: generateUUID(),
        content: inputContent,
        role: "user",
      };
      append(newMessage);
      setInputContent("");
      await streamChat({ inputContent, setIsLoading, append });
    },
    [inputContent, setInputContent, setIsLoading, append]
  );

  const onSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    handleSubmit(e);
  };

  return (
    <div className="flex flex-col w-full max-w-3xl pt-14 pb-60 mx-auto stretch">
      <ChatMessage isLoading={isLoading} messages={messages} />

      <ChatInput
        userInput={inputContent}
        handleInputChange={handleInputChange}
        handleSubmit={onSubmit}
        isLoading={isLoading}
        messages={messages}
        appendAndTrigger={appendAndTrigger}
      />
    </div>
  );
}
