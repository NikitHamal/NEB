import { ArgumentsHost, Catch, ExceptionFilter, HttpException, HttpStatus, Logger } from "@nestjs/common";
import type { Response } from "express";
import { MulterError } from "multer";

// Shapes every error into { success: false, error } - HttpException, Multer errors, and anything unrecognized.
@Catch()
export class HttpExceptionFilter implements ExceptionFilter {
  private readonly logger = new Logger(HttpExceptionFilter.name);

  catch(exception: unknown, host: ArgumentsHost): void {
    const response = host.switchToHttp().getResponse<Response>();

    if (exception instanceof HttpException) {
      const status = exception.getStatus();

      if (status >= 500) {
        this.logger.error(exception);
      }

      response.status(status).json({ success: false, error: this.extractMessage(exception) });
      return;
    }

    if (exception instanceof MulterError) {
      response.status(HttpStatus.BAD_REQUEST).json({ success: false, error: this.formatMulterError(exception) });
      return;
    }

    // Unknown / unexpected error
    this.logger.error(exception);

    response.status(HttpStatus.INTERNAL_SERVER_ERROR).json({
      success: false,
      error:
        process.env.NODE_ENV === "production"
          ? "Internal Server Error"
          : exception instanceof Error
            ? exception.message
            : "Unknown error",
    });
  }

  private extractMessage(exception: HttpException): string {
    const body = exception.getResponse();

    if (typeof body === "string") return body;

    const { message } = body as { message?: string | string[] };

    if (Array.isArray(message)) return message.join("; ");
    return message ?? exception.message;
  }

  private formatMulterError(error: MulterError): string {
    switch (error.code) {
      case "LIMIT_FILE_SIZE":
        return "File size exceeds the maximum limit.";
      case "LIMIT_FILE_COUNT":
        return "File count exceeds the maximum limit.";
      case "LIMIT_UNEXPECTED_FILE":
        return "Unexpected file field.";
      default:
        return error.message;
    }
  }
}
