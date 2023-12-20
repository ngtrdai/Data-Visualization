FROM node:18-alpine

WORKDIR /home/node/DATA-VISUALIZATION/data-visualization-frontend

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

ENTRYPOINT ["sh", "entry.sh"]