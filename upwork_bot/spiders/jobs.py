# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    # upwork does not allow bots with default user_agent
    user_agent = 'Mozilla/5.1'

    def start_requests(self):
        yield SplashRequest('https://www.upwork.com/i/job-categories/')

    # parse categories page looping through all subcategories
    def parse(self, response):
        for page in response.xpath("//ul[@class='plain-list']/li/a[contains(@href,'/sc/')]/@href").getall():
            yield SplashRequest(
                response.urljoin(page),
                callback=self.parse_page
            )

    # parse jobs page
    def parse_page(self, response):
        for job in response.css('section.air-card.air-card-hover.job-tile-responsive[id]'):
            yield {
                'title': job.css('a.job-title-link up-c-line-clamp::text').get(),
                'tags': job.css('span.js-skill.d-inline-block a.o-tag-skill span::text').getall(),
                'description': job.xpath('normalize-space(.//div[@class="description break"]/div)').get()
            }

        next_page = response.css('li.next > a::attr(href)').get()
        if next_page:
            yield SplashRequest(
                'https://www.upwork.com'+next_page,
                callback=self.parse_page
            )

