import { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
    const { query } = req.body;
    res.status(200).json({ text: `You asked: ${query}. Here's some F1 knowledge!` });
}
