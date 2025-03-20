import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

export default function Chatbot() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setMessages([...messages, { role: "user", content: question }]);
    
    try {
      const response = await fetch("http://localhost:8000/query/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await response.json();
      setMessages((prev) => [...prev, { role: "assistant", content: data.answer }]);
    } catch (error) {
      console.error("Error fetching response:", error);
    } finally {
      setLoading(false);
      setQuestion("");
    }
  };

  return (
    <div className="flex flex-col items-center p-4">
      <h1 className="text-xl font-bold mb-4">Healthcare Policy Chatbot</h1>
      <Card className="w-full max-w-lg p-4">
        <CardContent className="space-y-2">
          {messages.map((msg, index) => (
            <div key={index} className={`p-2 rounded-md ${msg.role === "user" ? "bg-blue-200" : "bg-gray-200"}`}>
              <strong>{msg.role === "user" ? "You" : "Chatbot"}:</strong> {msg.content}
            </div>
          ))}
          {loading && <p className="text-gray-500">Thinking...</p>}
        </CardContent>
      </Card>
      <div className="flex w-full max-w-lg mt-4">
        <Input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask about healthcare policies..."
          className="flex-grow"
        />
        <Button onClick={handleSendMessage} disabled={loading} className="ml-2">Send</Button>
      </div>
    </div>
  );
}
