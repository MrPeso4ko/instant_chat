FROM nginx:1.25.2 as production-stage

ARG API_HOST
ENV API_HOST $API_HOST

ARG API_PORT
ENV API_PORT $API_PORT

ARG NGINX_PORT
ENV NGINX_PORT $NGINX_PORT

COPY nginx/templates /etc/nginx/templates/

RUN rm -rf /usr/share/nginx/html/*
COPY /frontend /usr/share/nginx/html

EXPOSE ${NGINX_PORT}
CMD ["nginx", "-g", "daemon off;"]