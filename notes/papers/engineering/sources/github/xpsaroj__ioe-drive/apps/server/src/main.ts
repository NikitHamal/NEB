import "reflect-metadata";

import { Logger, RequestMethod, ValidationPipe } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { NestFactory } from "@nestjs/core";
import type { NestExpressApplication } from "@nestjs/platform-express";

import { AppModule } from "./app.module";
import { ConfiguredSocketIoAdapter } from "./common/adapters/socket-io.adapter";
import { HttpExceptionFilter } from "./common/filters/http-exception.filter";
import { ResponseInterceptor } from "./common/interceptors/response.interceptor";

async function bootstrap() {
  // rawBody:true stashes the untouched Buffer on req.rawBody, needed by the Clerk webhook route.
  const app = await NestFactory.create<NestExpressApplication>(AppModule, {
    rawBody: true,
  });

  const configService = app.get(ConfigService);
  const logger = new Logger("Bootstrap");

  if (configService.get<string>("NODE_ENV") === "production") {
    // The prod reverse proxy requires trusting the first hop for correct client IP detection.
    app.set("trust proxy", 1);
  }

  const allowedOrigins = configService
    .getOrThrow<string>("ALLOWED_ORIGINS")
    .split(",")
    .map((origin) => origin.trim());

  app.enableCors({
    origin: allowedOrigins,
    methods: ["GET", "POST", "PUT", "DELETE", "PATCH"],
    allowedHeaders: ["Content-Type", "Authorization"],
  });

  // Binds socket.io onto the same HTTP server/port - no new infrastructure needed.
  app.useWebSocketAdapter(new ConfiguredSocketIoAdapter(app, allowedOrigins));

  // /health stays unprefixed - liveness checks shouldn't depend on API versioning.
  app.setGlobalPrefix("api", {
    exclude: [{ path: "health", method: RequestMethod.ALL }],
  });

  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  app.useGlobalFilters(new HttpExceptionFilter());
  app.useGlobalInterceptors(new ResponseInterceptor());

  app.enableShutdownHooks();

  const port = configService.getOrThrow<number>("PORT");
  await app.listen(port);

  logger.log(`Server running on port: ${port}`);
  logger.log(`Environment: ${configService.get<string>("NODE_ENV")}`);
}

bootstrap();
