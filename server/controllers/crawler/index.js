const Router = require('koa-router');
const router = new Router();
const rp = require('request-promise');
const cheerio = require("cheerio");
const crawler = require("../../libs/crawler/moneyUdn");

/**
 * API block
 */

router.get('/searching', async (ctx) => {
  const resp = ctx.response;
  crawler.SEARCH_UDN('特力,淘寶,hoi,taobao,何采容,新零售,智慧門店');
  resp.status = 200;
  resp.body = 'Ok';
});

module.exports = router;
