import { ArgumentsHost, Catch, ExceptionFilter, HttpException, Logger } from "@nestjs/common";
import type { Socket } from "socket.io";

// WS equivalent of HttpExceptionFilter - the HTTP one assumes an Express Response object, which a
// gateway handler doesn't have; this emits an "error" event back to the client socket instead.
@Catch()
export class WsExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger(WsExceptionFilter.name);

  catch(exception: unknown, host: ArgumentsHost): void {
    const client = host.switchToWs().getClient<Socket>();

    if (exception instanceof HttpException) {
      const status = exception.getStatus();

      if (status >= 500) {
        this.logger.error(exception);
      }

      client.emit("error", { message: this.extractMessage(exception) });
      return;
    }

    this.logger.error(exception);
    client.emit("error", { message: exception instanceof Error ? exception.message : "Unknown error" });
  }

  private extractMessage(exception: HttpException): string {
    const body = exception.getResponse();

    if (typeof body === "string") return body;

    const { message } = body as { message?: string | string[] };

    if (Array.isArray(message)) return message.join("; ");
    return message ?? exception.message;
  }
}
