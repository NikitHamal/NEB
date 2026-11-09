import { Global, Module } from "@nestjs/common";
import { ConfigModule } from "@nestjs/config";

import { AzureBlobService } from "./azure-blob.service";

@Global()
@Module({
  imports: [ConfigModule],
  providers: [AzureBlobService],
  exports: [AzureBlobService],
})
export class AzureBlobModule {}
