import ChatBox from "../components/ChatBox";
import InputBox from "../components/InputBox";
import { RecoilRoot } from "recoil";

export default function Home() {
  return (
    <RecoilRoot>
      <div className="h-screen flex flex-col items-center justify-center bg-black text-white">
        <h1 className="text-2xl font-bold mb-4">Velocity AI - F1 Chatbot</h1>
        <ChatBox />
        <InputBox />
      </div>
    </RecoilRoot>
  );
}
