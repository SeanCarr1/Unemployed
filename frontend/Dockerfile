FROM oven/bun:latest

WORKDIR /app


# Only copy package manifests first for dependency caching

# Only copy package manifests first for dependency caching
COPY package.json bun.lockb ./
RUN bun install

# Copy the rest of the source code (excluding node_modules)
COPY . .

EXPOSE 5173

CMD ["bun", "run", "dev"]