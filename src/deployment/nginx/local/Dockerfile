FROM nginx:1.23-alpine
COPY deployment/nginx/local/default.conf /etc/nginx/templates/default.conf.template
COPY frontend/dist /usr/share/nginx/html/
RUN apk update && apk add bash
