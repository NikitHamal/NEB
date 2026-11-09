module.exports = {
    apps: [
        {
            name: "ioe-drive-server",
            script: "dist/main.js",
            node_args: "-r dotenv/config",
            cwd: "./",
            env: {
                NODE_ENV: "development",
            },
            env_production: {
                NODE_ENV: "production",
            },
            env_test: {
                NODE_ENV: "test",
            },
        },
    ],
};
