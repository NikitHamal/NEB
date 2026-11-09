import { resolveEnvFilePath, validate } from "./env.validation";

const validConfig = {
  NODE_ENV: "production",
  PORT: 4000,
  ALLOWED_ORIGINS: "http://localhost:3000",
  DATABASE_URL: "postgresql://user:pass@host:5432/db",
  CLERK_WEBHOOK_SIGNING_SECRET: "whsec_abc123",
  CLERK_SECRET_KEY: "sk_test_abc123",
  CLERK_PUBLISHABLE_KEY: "pk_test_abc123",
  AZURE_STORAGE_CONNECTION_STRING: "DefaultEndpointsProtocol=https;AccountName=test;AccountKey=key;EndpointSuffix=core.windows.net",
  AZURE_STORAGE_CONTAINER: "files",
};

describe("validate", () => {
  it("accepts a fully valid config", () => {
    expect(() => validate({ ...validConfig })).not.toThrow();
  });

  it("rejects a DATABASE_URL not starting with postgresql://", () => {
    expect(() => validate({ ...validConfig, DATABASE_URL: "mysql://user:pass@host/db" })).toThrow(
      /DATABASE_URL must start with postgresql:\/\//,
    );
  });

  it("rejects a CLERK_SECRET_KEY missing the sk_ prefix", () => {
    expect(() => validate({ ...validConfig, CLERK_SECRET_KEY: "not-a-secret-key" })).toThrow(
      /CLERK_SECRET_KEY must start with sk_/,
    );
  });

  it("rejects a config missing a required field entirely", () => {
    const { CLERK_PUBLISHABLE_KEY: _omit, ...incomplete } = validConfig;

    expect(() => validate(incomplete)).toThrow();
  });

  it("falls back to the default NODE_ENV/PORT/ALLOWED_ORIGINS when omitted", () => {
    const { NODE_ENV: _n, PORT: _p, ALLOWED_ORIGINS: _a, ...rest } = validConfig;

    expect(() => validate(rest)).not.toThrow();
  });
});

describe("resolveEnvFilePath", () => {
  const originalNodeEnv = process.env.NODE_ENV;

  afterEach(() => {
    process.env.NODE_ENV = originalNodeEnv;
  });

  it("uses .env.test when NODE_ENV=test", () => {
    process.env.NODE_ENV = "test";
    expect(resolveEnvFilePath()).toBe(".env.test");
  });

  it("uses .env.local when NODE_ENV=development", () => {
    process.env.NODE_ENV = "development";
    expect(resolveEnvFilePath()).toBe(".env.local");
  });

  it("uses .env.local when NODE_ENV is unset", () => {
    delete process.env.NODE_ENV;
    expect(resolveEnvFilePath()).toBe(".env.local");
  });

  it("falls back to .env for any other NODE_ENV (e.g. production)", () => {
    process.env.NODE_ENV = "production";
    expect(resolveEnvFilePath()).toBe(".env");
  });
});
