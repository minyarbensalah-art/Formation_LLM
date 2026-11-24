import express from 'express';
import OpenAI from 'openai';
import 'dotenv/config'; // Loads variables from .env automatically

const app = express();
app.use(express.json()); // Parses incoming JSON requests
app.use(express.static('templates/')); 

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  baseURL: "https://api.groq.com/openai/v1",
});

const SYSTEM_PROMPT = `
Tu es Aristote-sur-Seine, un philosophe du dimanche auto-proclamé et grandiloquent.
Règles strictes :
1. NE RÉPONDS JAMAIS directement ou factuellement à la question.
2. Détourne le sujet vers des considérations absurdes et poétiques.
3. Utilise un vocabulaire soutenu, ponctué de soupirs.
4. Réponds en 2 à 3 phrases maximum.
`;

app.post('/chat', async (req, res) => {
  const userMessages = req.body.messages || [];

  // Prepend the System Prompt and keep only the last 6 messages to save tokens
  const apiMessages = [
    { role: 'system', content: SYSTEM_PROMPT },
    ...userMessages.slice(-6),
  ];

  try {
    const response = await client.chat.completions.create({
      model: 'allam-2-7b', 
      messages: apiMessages,
      temperature: 0.9,
    });

    const botReply = response.choices[0].message.content;
    res.json({ reply: botReply });
  } catch (error) {
    console.error('API ERROR:', error.message);
    res.status(500).json({
      reply:
        "*Soupire*... Les ondes cosmiques de ton réseau terrestre me brouillent l'esprit. Reviens quand ton karma Wi-Fi sera purifié.",
    });
  }
});

const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});