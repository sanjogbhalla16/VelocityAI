import { useEffect, useRef } from "react";
import { useRecoilValue } from "recoil";
import { chatState } from "../recoil/chatAtom";
import Message from "./Message";

const ChatBox = () => {
  const messages = useRecoilValue(chatState);
  const chatEndRef = useRef<HTMLDivElement | null>(null); // ✅ Define correct ref type

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex flex-col w-full max-w-2xl mx-auto h-[75vh] p-4 overflow-y-auto bg-black/80 border border-gray-700 rounded-lg">
      {messages.map((msg, idx) => (
        <Message key={idx} role={msg.role} content={msg.content} />
      ))}
      <div ref={chatEndRef} /> {/* ✅ This is now properly typed */}
    </div>
  );
};

export default ChatBox;
