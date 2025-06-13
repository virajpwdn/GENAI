import { config } from "dotenv";
config();

import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_KEY });

async function main() {
    const chat = ai.chats.create({
      model: "gemini-2.0-flash",
      history: [
        {
          role: "user",
          parts: [{ text: "Hello" }],
        },
        {
          role: "model",
          parts: [{ text: "Great to meet you. What would you like to know?" }],
        },
      ],
    });
  
    const response1 = await chat.sendMessage({
      message: "I have 2 dogs in my house.",
    });
    console.log("Chat response 1:", response1.text);
  
    const response2 = await chat.sendMessage({
      message: "How many paws are in my house?",
    });
    console.log("Chat response 2:", response2.text);
  }
  
  await main();