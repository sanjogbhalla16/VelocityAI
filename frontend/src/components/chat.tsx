"use client"; //This line ensures the component runs only on the client-side in Next.js.
//Next.js defaults to server-side rendering, but interactive UI components (like this chat) need to run in the browser. Means client is browser

export function Chat({ id }: { id: string }) {
  return (
    <div className="flex flex-col w-full max-w-3xl pt-14 pb-60 mx-auto stretch">
      <h1>Welcome To Velocity AI </h1>
      <p> Chat ID: {id}</p>
    </div>
  );
}
