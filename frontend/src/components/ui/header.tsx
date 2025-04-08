"use client";

import React from "react";
import { HomeIcon } from "lucide-react";
import Link from "next/link";

export const Header: React.FC = () => {
  return (
    <header className="fixed w-full p-2 flex justify-between items-center z-10 backdrop-blur md:backdrop-blur-none bg-background/80 md:bg-transparent">
      <div>
        <Link href="/" className="flex items-center gap-2">
          <HomeIcon size={16} />
          <span className="sr-only">Sanjog Bhalla</span>
        </Link>
      </div>
    </header>
  );
};

export default Header;
