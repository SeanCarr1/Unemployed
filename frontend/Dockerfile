# --- Bun multi-stage build for Vite frontend ---

FROM oven/bun:latest

WORKDIR /app

# COPY package.json bun.lock ./
COPY package.json ./
RUN bun install

COPY . .

EXPOSE 5173
CMD ["bun", "run", "dev"]


# FROM oven/bun:alpine AS base
# WORKDIR /app

# COPY package.json ./
# RUN bun install


# # Install dev dependencies (for development and build)
# FROM base AS install
# RUN mkdir -p /temp/dev
# COPY package.json bun.lock /temp/dev/
# RUN cd /temp/dev && bun install --frozen-lockfile

# # Install production dependencies only (for final image)
# FROM base AS prodinstall
# RUN mkdir -p /temp/prod
# COPY package.json bun.lock /temp/prod/
# RUN cd /temp/prod && bun install --frozen-lockfile --production

# # Copy node_modules and source for build/test
# FROM base AS prerelease
# COPY --from=install /temp/dev/node_modules node_modules
# COPY . .

# # [optional] run tests & build
# # ENV NODE_ENV=production
# # RUN bun test
# # RUN bun run build

# # Final image: only production deps and source
# FROM base AS release
# WORKDIR /usr/src/app
# COPY --from=prodinstall /temp/prod/node_modules node_modules
# COPY --from=prerelease /usr/src/app/ .

# EXPOSE 5173
# CMD ["bun", "x", "vite", "--host", "0.0.0.0"]