FROM node:22-alpine

WORKDIR /app

# Create non-root user for security
RUN adduser -D -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

COPY --chown=appuser:appuser package.json ./
RUN npm install --legacy-peer-deps

COPY --chown=appuser:appuser . .

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=development

EXPOSE 3000

CMD ["npm", "run", "dev"]
