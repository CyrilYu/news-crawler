const rp = require('request-promise');
const cheerio = require("cheerio");
const logger = require("tracer").colorConsole();
const crawlerConfig = require('../../config/crawler');

const SEARCH_UDN = function (params) {
  let baseUrl = crawlerConfig.ReproduceNews.moneyUdn;
  const keywords = params.split(',');
  keywords.forEach(function(e) {
    baseUrl = `${baseUrl}${e}%20`;
  })
  
  let options = {
      uri: encodeURI(baseUrl),
      method: 'GET'
  }
  rp(options)
    .then(resp => {
      let $ = cheerio.load(resp);
      let newsTitle = [];
      let newsLinks = [];
      const searchContentHtml = $('div#search_content').html();
      const searchResult = cheerio.load(searchContentHtml)
      const titles = searchResult('h3');
      const links = searchResult('a');
      for(let i=0;i<links.length;i++) {
        newsLinks.push(searchResult(links[i]).attr('href'));
      }
      for(let i=0;i<titles.length;i++) {
        newsTitle.push(searchResult(titles[i]).text())
      }
      for(let i=0;i<newsTitle.length;i++) {
        logger.info(newsTitle[i]);
        logger.info(newsLinks[i]);
      }
      return true;
    })
    .catch(err => {
      logger.warn(err);
      return false;
    })
}

module.exports = {
  SEARCH_UDN: SEARCH_UDN
}