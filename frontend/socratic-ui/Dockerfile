# Stage 1: Build Stage
FROM node:18-alpine AS build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json for dependency install caching
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy source files
COPY . .

# Build the React app (produces the build/ directory by default)
RUN npm run build

# # Stage 2: Production Stage
# FROM nginx:alpine

# # Copy the build output to Nginx's default html directory
# COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for access
EXPOSE 5173

# Start Nginx server
# CMD ["nginx", "-g", "daemon off;"]
CMD [ "npm", "start" ]
