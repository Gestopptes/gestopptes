FROM node:16-alpine

# RUN npm install -g yarn
RUN apk add git
WORKDIR /browser
RUN git clone https://github.com/neo4j/neo4j-browser . &&  git fetch -ap && git checkout release-5.12.0 && yarn install
RUN yarn build --production
CMD yarn start-prod

