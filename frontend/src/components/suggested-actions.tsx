"use client";
//this is providing predefined actions to us
import { motion } from "framer-motion";
import { Button } from "./ui/button";
import { memo } from "react";
import { Message } from "@/lib/types";
import { generateUUID } from "@/lib/utils";
import { Overview } from "./overview";

interface SuggestedActionsProps {
  chatId: string;
  appendAndTrigger: (message: Message) => Promise<void>;
}

function PureSuggestedActions({
  chatId,
  appendAndTrigger,
}: SuggestedActionsProps) {
  const suggestedActions = [
    {
      title: "Who won the last race?",
      label: "Latest Formula 1 results",
      action: "Who won the last Formula 1 race?",
    },
    {
      title: "Tell me about",
      label: "Max Verstappen's racing stats",
      action: "Tell me about Max Verstappen's racing stats.",
    },
    {
      title: "What are the key strategies",
      label: "for a Formula 1 pit stop?",
      action: "What are the key strategies for a Formula 1 pit stop?",
    },
    {
      title: "Explain DRS",
      label: "and how it works in F1",
      action: "Explain DRS and how it works in F1.",
    },
    {
      title: "Show me the upcoming races",
      label: "for this season",
      action: "Show me the upcoming Formula 1 races for this season.",
    },
  ];

  return (
    <div className="flex flex-col items-center gap-2 w-full max-w-3xl mx-auto p-4">
      {/* Overview Section */}
      <Overview />
      <div className="grid sm:grid-cols-2 gap-2 w-full">
        {suggestedActions.map((suggestedAction, index) => (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ delay: 0.05 * index }}
            key={`suggested-action-${suggestedAction.title}-${index}`}
            className={index > 1 ? "hidden sm:block" : "block"}
          >
            <Button
              variant="ghost"
              onClick={async () => {
                window.history.replaceState({}, "", `/chat/${chatId}`);

                appendAndTrigger({
                  id: generateUUID(),
                  role: "user",
                  content: suggestedAction.action,
                });
              }}
              className="text-left border rounded-xl px-4 py-3.5 text-sm flex-1 gap-1 sm:flex-col w-full h-auto justify-start items-start"
            >
              <span className="font-medium">{suggestedAction.title}</span>
              <span className="text-muted-foreground">
                {suggestedAction.label}
              </span>
            </Button>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

export const SuggestedActions = memo(PureSuggestedActions, () => true);
