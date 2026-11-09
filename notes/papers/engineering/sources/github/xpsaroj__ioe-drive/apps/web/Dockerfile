FROM node:24-alpine

WORKDIR /app

# Run as the image's built-in non-root "node" user (uid/gid 1000), matching the typical
# host user on a single-user Linux dev machine. Since ./apps/web is bind-mounted into
# this container for local dev, anything the process writes (e.g. Next.js's .next
# cache) would otherwise end up root-owned on the host and break subsequent host-side
# commands (npm run build, git, editors, etc).
RUN chown -R node:node /app
USER node

COPY --chown=node:node package*.json .

RUN npm install

COPY --chown=node:node . .

EXPOSE 3000

CMD ["npm", "run", "dev"]