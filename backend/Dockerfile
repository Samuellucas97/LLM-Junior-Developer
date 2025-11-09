
# Use a lightweight, stable Node Alpine image for production
FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

# Copy only package.json and package-lock.json for better caching
COPY package*.json ./

# Install dependencies (production only if desired)
RUN npm install --production

# Copy app source code
COPY . .

RUN npm run build

# Expose port your app listens on
EXPOSE 5001

# Start the app
CMD [ "npm", "start" ]
