import { INestApplicationContext } from "@nestjs/common";
import { IoAdapter } from "@nestjs/platform-socket.io";
import type { ServerOptions } from "socket.io";

// @WebSocketGateway()'s own options are static (evaluated before DI is available), so CORS for every
// gateway/namespace is configured here instead, where ConfigService is already resolved.
export class ConfiguredSocketIoAdapter extends IoAdapter {
  constructor(
    app: INestApplicationContext,
    private readonly allowedOrigins: string[],
  ) {
    super(app);
  }

  createIOServer(port: number, options?: ServerOptions) {
    return super.createIOServer(port, {
      ...options,
      cors: { origin: this.allowedOrigins, credentials: true },
    });
  }
}
