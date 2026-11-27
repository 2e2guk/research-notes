---
layout: reading
permalink: /blog/
title: 전체 글
heading: 전체 글
description: 모든 기록을 게시 날짜순으로 모았습니다.
nav: true
nav_order: 2
pagination:
  enabled: false
---

<nav class="reading-quicklinks" aria-label="기록 탐색"><a href="{{ '/' | relative_url }}">주제별 목차</a><a href="{{ '/tags/' | relative_url }}">태그로 찾아보기</a></nav>
{% if site.posts.size > 0 %}
<ul class="reading-all-posts">
  {% for entry in site.posts %}
  <li>
    <time datetime="{{ entry.date | date_to_xmlschema }}">{{ entry.date | date: '%Y.%m.%d' }}</time>
    <a class="reading-post-title" href="{{ entry.url | relative_url }}">{{ entry.title | escape }}</a>
    {% if entry.description %}<p class="reading-post-description">{{ entry.description | escape }}</p>{% endif %}
    <div class="reading-post-tags">
      {% for tag in entry.tags %}
      <a href="{{ tag | slugify | prepend: '/blog/tag/' | append: '/' | relative_url }}">#{{ tag | escape }}</a>
      {% endfor %}
    </div>
  </li>
  {% endfor %}
</ul>
{% else %}
<p class="reading-empty reading-empty-panel">아직 공개한 글이 없습니다. 주제별 목차에서 관심 있는 연구 주제를 살펴보세요.</p>
{% endif %}
