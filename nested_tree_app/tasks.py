# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import signature, chain, group, shared_task
from nested_tree_app.models import Category
import requests
from lxml import html, etree
from itertools import permutations, izip_longest
from django.db.utils import IntegrityError
from django import db
import pdb
import time


@shared_task
def reverse(string):
    return string[::-1]

@shared_task
def add(x, y):
    return x + y



def create_new_category(name, desc, parent=None):
    # db.connections.close_all
    try:
        new_category = Category(name=name, description=desc, parent=parent)
        new_category.save()
        return new_category
    except IntegrityError:
        print parent, name, desc
    # new_category, created = Category.objects.get_or_create(name=name,
    #                                                    description=desc,
    #                                                    parent=parent,)
    # return new_category, created

# @shared_task
def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)
#
# @shared_task
# def make_requests(*args):
#     # Create a set of unsent Requests:
#     rqs = (grequests.get(u) for u in args)
#     # Send them all at the same time:
#     resps = grequests.map(rqs)
    # [<Response [200]>, <Response [200]>, <Response [200]>, <Response [200]>, None, <Response [200]>]
#     result = []
#     for i in resps:
#         resp = i.content
#         result.append(resp)
#     return result
@shared_task
def make_request(url):
    resp = requests.get(url)
    return resp.content

# @shared_task
# def parse_response(resps):
#     result = []
#     for i in resps:
#         tree = html.fromstring(i.content)
#         text = tree.xpath('//div[@class="referats__text"]//text()')
#         del text[0]
#         del text[0]
#         text = "".join(text)
#         # text = text.split(".")
#         result.append(text)
#     # print result
#     return result

@shared_task
def parse_response(resp):
    tree = html.fromstring(resp)
    text = tree.xpath('//div[@class="referats__text"]//text()')
    del text[0]
    del text[0]
    text = "".join(text)
    # text = text.split(".")
    return text

# @shared_task
# def parse_response(url):
#     resp = requests.get(url)
#     tree = html.fromstring(resp.content)
#     text = tree.xpath('//div[@class="referats__text"]//text()')
#     del text[0]
#     del text[0]
#     text = "".join(text)
#     return text


@shared_task
def ps120(text):
    # 6*5*4 = 120 permutations with given arguments(text[:6], 3)
    # Texts are going to be used for 1st and 2nd level categories descriptions
    sentences = text.split(".")
    ps1_2 = permutations(sentences[:6], 3)
    ps1_2_list = list(ps1_2)

    # Divide the ps1__2_list:
    # 60 permutations for 1st level categories and 60 permutations for 2nd level categories
    # ps1_2_list = zip(ps1_list[::2], ps1_list[1::2])
    ps_1_2_groupped = grouper(ps1_2_list, 2)
    ps1_2 = list(ps_1_2_groupped)

    return ps1_2

@shared_task
def ps336(text):
    # 8*7*6 = 336 permutations with given arguments(text[:8], 3)
    # Texts are going to be used for 3rd and 4th level categories descriptions
    sentences = text.split(".")
    ps3_4 = permutations(sentences[:8], 3)
    ps3_4_list = list(ps3_4)

    # Split in 60 chunks
    divisor = len(ps3_4_list) // 60
    ps3_4_groupped = grouper(ps3_4_list, divisor)
    ps3_4 = list(ps3_4_groupped)

    return ps3_4

@shared_task
def populate_1_2_3_4(ps1_2, ps_3, ps_4):
    for n, first_second in enumerate(ps1_2):
        chain(populate_1_level.s(first_second[0]), populate_2_level.s(first_second[1]),
              populate_3_4_level.s(ps_3[n], ps_4[n]))()

        # desc1 = ".".join(first_second[0])
        # first_level_category = create_new_category(name="1st level category", desc=desc1)
        # if first_level_category:
        #     desc2 = ".".join(first_second[1])
        #     second_level_category = create_new_category(
        #         name="2nd level category", desc=desc2, parent=first_level_category)
        #     if second_level_category:
        #         for i in xrange(5):
        #             desc3 = ".".join(ps_3[n][i])
        #             third_level_category = create_new_category(
        #                 name="3rd level category", desc=desc3, parent=second_level_category
        #             )
        #             if third_level_category:
        #                 desc4 = ".".join(ps_4[n][i])
        #                 fourth_level_category = create_new_category(
        #                     name="4th level category", desc=desc4, parent=third_level_category
        #                 )
@shared_task
def populate_1_level(text):
    desc1 = ".".join(text)
    first_level_category = create_new_category(name="1st level category", desc=desc1)
    if first_level_category:
        return first_level_category.pk

@shared_task
def populate_2_level(parent_pk, text):
    desc2 = ".".join(text)
    second_level_category = create_new_category(
        name="2nd level category", desc=desc2, parent=Category.objects.get(pk=parent_pk))
    if second_level_category:
        return second_level_category.pk

@shared_task
def populate_3_4_level(parent_pk, texts3, texts4):
    for i in xrange(5):
        desc3 = ".".join(texts3[i])
        third_level_category = create_new_category(
            name="3rd level category", desc=desc3, parent=Category.objects.get(pk=parent_pk)
        )
        if third_level_category:
            desc4 = ".".join(texts4[i])
            fourth_level_category = create_new_category(
                name="4th level category", desc=desc4, parent=third_level_category
            )

