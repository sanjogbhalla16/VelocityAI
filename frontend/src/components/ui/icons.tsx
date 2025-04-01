"use client"; //This tells Next.js that this component should run on the client side.

import { cn } from "@/lib/utils";

//Allows passing custom styles.
//Captures any other attributes passed to the <svg> tag.
function IconLogo({ className, ...props }: React.ComponentProps<"svg">) {
  return (
    <svg
      fill="currentColor"
      viewBox="0 0 256 256"
      role="img"
      xmlns="http://www.w3.org/2000/svg"
      className={cn("h-4 w-4", className)}
      {...props}
    >
      <circle cx="128" cy="128" r="128" fill="black"></circle>
      <circle cx="102" cy="128" r="18" fill="white"></circle>
      <circle cx="154" cy="128" r="18" fill="white"></circle>
    </svg>
  );
}

export { IconLogo };
