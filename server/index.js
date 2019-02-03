const Koa = require('koa');
const cors = require('koa2-cors');
const mount = require('koa-mount');

const app = new Koa();
const index = require('./controllers/crawler');
app.use(cors({ methods: ['GET', 'POST', 'PUT', 'PATCH'] }));

app
  .use(index.routes())
  .use(index.allowedMethods())
  .use(mount('/crawler', index.middleware()));

module.exports = app;