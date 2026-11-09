import crypto from "node:crypto";
import path from "node:path";

import { Injectable } from "@nestjs/common";
import { ConfigService } from "@nestjs/config";
import { BlobSASPermissions, BlobServiceClient, type ContainerClient } from "@azure/storage-blob";

// Blob name prefix per upload source - purely a naming convention (Azure containers are
// flat), but it's what makes the Portal/Storage Explorer show these as separate folders.
export type BlobPrefix = "resources" | "listings";

/** Wraps Azure Blob Storage access as an injectable provider. */
@Injectable()
export class AzureBlobService {
  private readonly containerClient: ContainerClient;

  constructor(configService: ConfigService) {
    const blobServiceClient = BlobServiceClient.fromConnectionString(
      configService.getOrThrow<string>("AZURE_STORAGE_CONNECTION_STRING"),
    );

    this.containerClient = blobServiceClient.getContainerClient(
      configService.getOrThrow<string>("AZURE_STORAGE_CONTAINER"),
    );
  }

  generateBlobName(originalName: string, prefix: BlobPrefix): string {
    const ext = path.extname(originalName);
    return `${prefix}/${crypto.randomUUID()}${ext}`;
  }

  async upload(buffer: Buffer, blobName: string, mimeType: string): Promise<string> {
    const blockBlob = this.containerClient.getBlockBlobClient(blobName);

    await blockBlob.uploadData(buffer, {
      blobHTTPHeaders: { blobContentType: mimeType },
    });

    return blockBlob.url;
  }

  async delete(blobName: string): Promise<void> {
    const blockBlob = this.containerClient.getBlockBlobClient(blobName);
    await blockBlob.deleteIfExists();
  }

  // Cross-origin blob URL ignores the HTML `download` attribute, so inline-vs-attachment is controlled via `contentDisposition` instead.
  async generateSasUrl(
    blobName: string,
    options: { expiresInMinutes?: number; contentDisposition?: string } = {},
  ): Promise<string> {
    const { expiresInMinutes = 15, contentDisposition } = options;
    const blockBlob = this.containerClient.getBlockBlobClient(blobName);

    return blockBlob.generateSasUrl({
      permissions: BlobSASPermissions.parse("r"),
      expiresOn: new Date(Date.now() + expiresInMinutes * 60 * 1000),
      ...(contentDisposition ? { contentDisposition } : {}),
    });
  }
}
