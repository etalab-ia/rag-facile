import { LiteParse } from "@llamaindex/liteparse";
import type { MastraDBMessage } from "@mastra/core/agent";
import type { ProcessInputArgs, Processor } from "@mastra/core/processors";

/**
 * Input processor that converts PDF file parts to text before they reach the LLM.
 *
 * When a user uploads a PDF via Mastra Studio's file upload button, it arrives
 * as a `file` part with `mimeType: 'application/pdf'`. Most OpenAI-compatible
 * LLMs (including Albert API) don't support binary PDF media types, causing:
 *
 *   AI_UnsupportedFunctionalityError: 'file part media type application/pdf' functionality not supported
 *
 * This processor intercepts those file parts, extracts text using LiteParse,
 * and replaces them with plain `text` parts the LLM can process.
 */
export class PdfToTextProcessor implements Processor {
  readonly id = "pdf-to-text";
  readonly name = "PDF to Text Converter";

  private parser: LiteParse;

  constructor() {
    this.parser = new LiteParse({ ocrEnabled: false });
  }

  async processInput({ messages }: ProcessInputArgs) {
    const processedMessages: MastraDBMessage[] = [];

    for (const message of messages) {
      if (message.role !== "user" || !message.content?.parts) {
        processedMessages.push(message);
        continue;
      }

      let hasPdf = false;
      const newParts = [...message.content.parts];

      for (let i = 0; i < newParts.length; i++) {
        const part = newParts[i];
        if (part.type === "file" && part.mimeType === "application/pdf") {
          hasPdf = true;
          const pdfText = await this.extractTextFromPdfPart(part);
          newParts[i] = {
            type: "text",
            text: pdfText,
          };
        }
      }

      if (hasPdf) {
        processedMessages.push({
          ...message,
          content: {
            ...message.content,
            parts: newParts,
          },
        });
      } else {
        processedMessages.push(message);
      }
    }

    return processedMessages;
  }

  private async extractTextFromPdfPart(part: {
    data: string | URL | Uint8Array;
    mimeType: string;
  }): Promise<string> {
    try {
      let buffer: Uint8Array;

      if (part.data instanceof URL) {
        // Fetch the PDF from URL
        const response = await fetch(part.data.toString());
        const arrayBuffer = await response.arrayBuffer();
        buffer = new Uint8Array(arrayBuffer);
      } else if (typeof part.data === "string") {
        // Base64-encoded string
        buffer = Uint8Array.from(atob(part.data), (c) => c.charCodeAt(0));
      } else {
        // Already Uint8Array
        buffer = part.data;
      }

      const result = await this.parser.parse(buffer, true);

      if (!result.text || result.text.trim().length === 0) {
        return "[PDF uploaded but no text could be extracted. The document may be image-based or empty.]";
      }

      // Add page markers for citation support
      const pagesWithMarkers = result.pages
        .map((page) => `--- Page ${page.pageNum} ---\n${page.text}`)
        .join("\n\n");

      return `[PDF document content]\n\n${pagesWithMarkers}`;
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return `[PDF upload failed to process: ${message}]`;
    }
  }
}
