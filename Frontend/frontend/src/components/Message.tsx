import { motion } from "framer-motion";

interface MessageProps {
  role: "user" | "bot"; // Explicitly define allowed values
  content: string;
}

const Message: React.FC<MessageProps> = ({ role, content }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`p-3 my-2 rounded-lg max-w-[80%] ${
        role === "user"
          ? "bg-blue-600 text-white self-end"
          : "bg-gray-800 text-gray-300 self-start"
      }`}
    >
      {content}
    </motion.div>
  );
};

export default Message;
