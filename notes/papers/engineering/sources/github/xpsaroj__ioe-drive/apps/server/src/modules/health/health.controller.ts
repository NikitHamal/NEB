import { Controller, Get } from "@nestjs/common";
import { SkipThrottle } from "@nestjs/throttler";

import { ApiResponse } from "../../common/dto/api-response";

@Controller("health")
@SkipThrottle()
export class HealthController {
  /** GET /health - liveness check, mounted outside /api and outside the throttler. */
  @Get()
  check() {
    return ApiResponse.of(
      { status: "ok", timestamp: new Date().toISOString() },
      "Server up and running.",
    );
  }
}
