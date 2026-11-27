---
layout: reading
permalink: /tags/
title: 태그
heading: 태그로 찾아보기
description: 같은 개념을 다룬 논문과 설명을 함께 찾아보세요.
nav: true
nav_order: 1
---

<nav class="reading-quicklinks" aria-label="기록 탐색"><a href="{{ '/' | relative_url }}">주제별 목차</a><a href="{{ '/blog/' | relative_url }}">전체 글</a></nav>
{% assign sorted_tags = site.tags | sort %}
{% if sorted_tags.size > 0 %}
<ul class="reading-tag-index">
  {% for item in sorted_tags %}
  <li>
    <a data-tag-link="{{ item[0] | escape }}" href="{{ item[0] | slugify | prepend: '/blog/tag/' | append: '/' | relative_url }}">
      <span>#{{ item[0] | escape }}</span><span class="reading-count">{{ item[1].size }}편</span>
    </a>
  </li>
  {% endfor %}
</ul>
{% else %}
<p class="reading-empty reading-empty-panel">태그가 붙은 글은 아직 없습니다.</p>
{% endif %}
