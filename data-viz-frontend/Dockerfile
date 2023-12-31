FROM node:18-alpine AS base

LABEL maintainer="Dai Nguyen Trong"

ARG NODE_ENV=production
ARG PORT=3000

WORKDIR /src

# Build
FROM base AS build

COPY package.json package-lock.json ./
RUN npm install --production=false

COPY . .

RUN npm run build
RUN npm prune

# Run
FROM base
ENV PORT=${PORT}

COPY --from=build /src/.output /src/.output
COPY --from=build /src/node_modules /src/node_modules

CMD ["node", ".output/server/index.mjs"]