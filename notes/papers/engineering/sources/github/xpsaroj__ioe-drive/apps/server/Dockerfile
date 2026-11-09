FROM node:24-alpine

WORKDIR /app

# Run as the image's built-in non-root "node" user (uid/gid 1000), matching the typical
# host user on a single-user Linux dev machine. Since ./apps/server is bind-mounted into
# this container for live editing, anything the process writes would otherwise end up
# root-owned on the host and break subsequent host-side commands.
RUN chown -R node:node /app
USER node

COPY --chown=node:node package*.json .

RUN npm install

COPY --chown=node:node . .

EXPOSE 4000

CMD ["npm", "run", "start:dev"]
