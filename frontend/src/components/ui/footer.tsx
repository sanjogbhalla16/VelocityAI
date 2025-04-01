"use client";

import Link from "next/link"; //Client-side navigation using Next.js.
import React from "react";
import { SiGithub } from "react-icons/si";
import { Button } from "./button";

const Footer: React.FC = () => {
  return (
    <footer className="w-fit p-1 md:p-2 fixed bottom-0 right-0 hidden lg:block">
      <div className="flex justify-end">
        <Button
          variant={"ghost"}
          size={"icon"}
          className="text-muted-foreground/50"
        >
          <Link href="https://github.com/sanjogbhalla16" target="_blank">
            {" "}
            {/* this target enables the tab to open in new tab */}
            <SiGithub size={18} />
          </Link>
        </Button>
      </div>
    </footer>
  );
};

export default Footer;
