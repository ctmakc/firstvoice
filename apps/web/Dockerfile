FROM node:22-alpine

WORKDIR /app

# Use existing 'node' user (uid 1000) instead of creating a new one
RUN chown -R node:node /app
USER node

COPY --chown=node:node package.json ./
RUN npm install --legacy-peer-deps

COPY --chown=node:node . .

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=development

EXPOSE 3000

CMD ["npm", "run", "dev"]
