import { Mastra } from "@mastra/core/mastra";
import { LibSQLStore } from "@mastra/libsql";
import { PinoLogger } from "@mastra/loggers";
import { pdfChatAgent } from "./agents/pdf-chat-agent";
import { vectorStore } from "./lib/vector-store";
import { indexPdfWorkflow } from "./workflows/index-pdf";

export const mastra = new Mastra({
  workflows: { indexPdfWorkflow },
  agents: { pdfChatAgent },
  vectors: { vectorStore },
  storage: new LibSQLStore({
    id: "mastra-storage",
    url: "file:./mastra.db",
  }),
  logger: new PinoLogger({
    name: "Mastra",
    level: "info",
  }),
});
