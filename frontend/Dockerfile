# Base image with Node.js
FROM node:20

# set working directory inside container
WORKDIR /app

# copy package.json and lock file first for caching
COPY package*.json ./

# install dependencies
RUN npm install
# copy the rest of your vue project
COPY . .

EXPOSE 5173

# Run vite dev server
CMD ["npm", "run", "dev"]