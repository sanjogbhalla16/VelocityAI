import { useState } from "react";
import { useSetRecoilState } from "recoil";
import { chatState, Message } from "../recoil/chatAtom"; // Import Message type
import axios from "axios";

const InputBox = () => {
  const [input, setInput] = useState("");
  const setChat = useSetRecoilState(chatState);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage: Message = { role: "user", content: input };
    setChat((oldChat) => [...oldChat, userMessage]);

    try {
      const res = await axios.post("/api/chat", { query: input });
      const botMessage: Message = { role: "bot", content: res.data.text };
      setChat((oldChat) => [...oldChat, botMessage]);
    } catch (error) {
      setChat((oldChat) => [
        ...oldChat,
        { role: "bot", content: "Error fetching response!" },
      ]);
    }

    setInput("");
  };

  return (
    <div className="flex items-center w-full max-w-2xl mx-auto p-4 bg-black/80 border-t border-gray-700">
      <input
        className="w-full p-2 bg-gray-900 text-white rounded-md focus:outline-none"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        placeholder="Ask me anything about F1..."
      />
      <button
        className="ml-2 p-2 bg-blue-600 text-white rounded-md"
        onClick={sendMessage}
      >
        Send
      </button>
    </div>
  );
};

export default InputBox;
