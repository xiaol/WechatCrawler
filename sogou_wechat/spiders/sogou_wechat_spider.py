__author__ = 'wangzhen'
# !/usr/bin/env python
# -*- coding:utf-8 -*-

from lxml import etree
import xml.etree.ElementTree as ET

import scrapy
from scrapy import Request
from scrapy_redis.spiders import RedisSpider

import BeautifulSoup
from BeautifulSoup import BeautifulSoup as bs

from StringIO import StringIO
import sys
import uniout
import time
import requests
import json
import re
import random


class SogouWechatSpider(scrapy.Spider):
    name = 'sogou_wechat'
    web = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    # Cookies used to get article's url of the public account name which are returned by sogou server and located in the response object.
    cookies = dict(CXID="A31293CD64F23B857A8D2281E0AFAC75", SUID="E003C16F4E6C860A5607CD0E00063EF6", ssuid="5187232290", SUV="00E45544D3641F2356186B7FCA538567", pgv_pvi="7670036480", weixinIndexVisited="1", IPLOC="CN1100", pgv_si="s178981888", ABTEST="6|1454039911|v1", ad="8Zllllllll2Qb9sllllllVz$EdolllllToVXGyllllwlllll4qxlw@@@@@@@@@@@", SNUID="69DAA117C4C1EEB61AD6208DC5946118", usid="91Imx4qtFE1V5-9G", ld="Ekllllllll2QkC3flllllVzrw6GlllllbDpoyZllllwlllll4voll5@@@@@@@@@@", sct="63", wapsogou_qq_nickname="")
    base_url = "http://weixin.sogou.com"

    # The 2nd, 3rd page in Home page.
    mid_url = "/pcindex/pc/pc_0/"
    suffix_url = ".html"

    start_urls = [
        base_url
    ]

    def get_wechat_pb_article_parse(self, response):
        wechat_pb_article_page = response.body
        wechat_pb_article_parser = etree.HTMLParser()
        wechat_pb_artcile_tree = etree.parse(StringIO(wechat_pb_article_page), wechat_pb_article_parser)

        pass

    # We get wechat public account by requests package, and transfer it to wechat article parser.
    def get_wechat_pb_urls_parse(self, response):

        wechat_pb_url_page = response.body
        wechat_pb_url_parser = etree.HTMLParser()
        wechat_pb_url_tree = etree.parse(StringIO(wechat_pb_url_page), wechat_pb_url_parser)

        target_node_list = wechat_pb_url_tree.xpath('// li [@id]')
        for target_node in target_node_list:
            href_url_node = target_node.xpath('.//a [@href]')[0]
            wechat_pub_href_url = href_url_node.attrib['href']

            # urllib2.urlopen(wechat_pub_href_url).read()

    def parse(self, response):
        html_page = response.body

        sogou_home_page_parser = etree.HTMLParser()
        sogou_home_page_tree = etree.parse(StringIO(html_page), sogou_home_page_parser)

        # Home page, we get wechat public account identifier and related articles.
        target_node_list = sogou_home_page_tree.xpath('//li [@id]')
        for target_node in target_node_list:
            href_url_node = target_node.xpath('.//div [@class="pos-wxrw"]')[0].xpath('.//a [@href]')[0]
            wechat_pb_href_url = href_url_node.attrib['href']
            web_length = len(self.web)
            web_agent_index = random.randint(0, web_length - 1)
            headers = {'User-Agent': str(self.web[web_agent_index])}

            # We use the original url to get the public account name. This public account name is unique.
            wechat_pb_indirect_page = requests.get(wechat_pb_href_url).content
            wechat_pb_indirect_parser = etree.HTMLParser()
            wechat_pb_href_tree = etree.parse(StringIO(wechat_pb_indirect_page), wechat_pb_indirect_parser)
            wechat_pb_name_node = wechat_pb_href_tree.xpath('//label [@name ="em_weixinhao"]')[0]
            wechat_pb_name = wechat_pb_name_node.text

            # We modify the url to get the history articles cached by sogou.
            wechat_pb_href_js_url = wechat_pb_href_url.replace('weixin.sogou.com/gzh', 'weixin.sogou.com/gzhjs')
            wechat_pb_href_js_url += '&cb=sogou.weixin_gzhcb&page='
            # We only get first two sections of the articles of wechat public account.
            for index in xrange(1, 3):
                tmp_wechat_pb_href_js_url = wechat_pb_href_js_url
                tmp_wechat_pb_href_js_url += str(index)

                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'}
                wechat_pb_href_js_html = requests.get(tmp_wechat_pb_href_js_url, headers=headers, cookies =self.cookies).content

                # The page returned by sogou is not a normalized html format, we get these articles by section format.
                article_cache_item_xml_list = re.findall('<\?xml.*?DOCUMENT>"', wechat_pb_href_js_html)
                for article_cache_item_xml in article_cache_item_xml_list:
                    norm_article_cache_item_xml = article_cache_item_xml.replace("\\", "").strip('"')
                    xml_parser = etree.HTMLParser()
                    xml_tree = etree.parse(StringIO(norm_article_cache_item_xml), xml_parser)

                    data = bs(norm_article_cache_item_xml)
                    for cd in data.findAll(text=True):
                        if isinstance(cd, BeautifulSoup.CData):
                            text = cd.replace("<![CDATA[", "").replace("]]>", "")
                            if 'websearch' in text:
                                # The url address of real article of one wechat public account is returned by sogou which locates in the url section of response.
                                article_sogou_indirect_url = self.base_url + text
                                resp = requests.get(article_sogou_indirect_url, headers=headers, cookies=self.cookies)
                                # We get the url address of real article in wechat (Tetent com).
                                article_wechat_direct_url = resp.url

                                wechat_pb_article_resp = requests.get(article_wechat_direct_url, headers=headers)
                                wechat_pb_article_page = wechat_pb_article_resp.content

                                wechat_pb_article_parser = etree.HTMLParser()
                                wechat_pb_article_tree = etree.parse(StringIO(wechat_pb_article_page),
                                                                     wechat_pb_article_parser)

                                # We store the wechat content in a list with the same sequence of the original html.

                                wechat_content_list = []
                                wechat_pb_article_content_node = wechat_pb_article_tree.xpath('//div [@id="js_content"]')[0]
                                wechat_pb_article_content_paragraph_nodes = wechat_pb_article_content_node.xpath('.//p')
                                for wechat_pb_article_content_paragraph_node in wechat_pb_article_content_paragraph_nodes:
                                        if wechat_pb_article_content_paragraph_node.findall('.//img') != []:
                                            img_node = wechat_pb_article_content_paragraph_node.findall('.//img')[0]
                                            wechat_content_list.append(img_node.attrib['data-src'])
                                        else:
                                            text = "".join(wechat_pb_article_content_paragraph_node.itertext())
                                            wechat_content_list.append(text)

                                # We can get much valuable meta data from <script type="text/javascript">
                                article_javascript_etree_node = \
                                wechat_pb_article_tree.xpath('//script [@type="text/javascript"]')[-2]
                                value_information = article_javascript_etree_node.text

                                text_lines = StringIO(value_information).readlines()
                                for text_line in text_lines:
                                    if 'nickname' in text_line:
                                        nickname = text_line.split("=")[-1].strip().replace(";", "")
                                    elif 'msg_title' in text_line:
                                        msg_title  = text_line.split("=")[-1].strip().replace(";", "")
                                    elif 'msg_desc' in text_line:
                                        msg_desc = text_line.split("=")[-1].strip().replace(";", "")
                                    elif 'msg_link' in text_line:
                                        msg_link = text_line.replace("var msg_link =", "").strip().replace('";', '"')
                                    else:
                                        continue


                        pass

                pass

        # Two more in Home page, we get wechat public account identifier and related articles.
        for index in xrange(1, 3):
            more_page_url = self.base_url + self.mid_url + str(index) + self.suffix_url
            req = requests.get(more_page_url)
            html = req.content
            # This function will be replaced by scrapy.Request function.
