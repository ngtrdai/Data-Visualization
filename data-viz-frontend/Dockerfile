FROM node:18-alpine

WORKDIR /home/node/DATA-VISUALIZATION/data-viz-frontend

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

ENTRYPOINT ["sh", "../scripts/frontend-scripts.sh"]