---
layout: default
title: All Posts
permalink: /posts/
---

# All Posts

Browse through all the AI vibe coding adventures and automated posts.

<div class="posts-list">
  {% for post in site.posts %}
    <article class="post-summary">
      <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
      <p class="post-meta">
        {{ post.date | date: "%B %d, %Y" }}
        {% if post.author %} • {{ post.author }}{% endif %}
      </p>
      <p>{{ post.excerpt }}</p>
      {% if post.tags %}
        <p class="tags">
          {% for tag in post.tags %}
            <span class="tag">{{ tag }}</span>
          {% endfor %}
        </p>
      {% endif %}
      <p><a href="{{ post.url | relative_url }}">Read more →</a></p>
    </article>
    <hr>
  {% endfor %}
</div>

{% if site.posts.size == 0 %}
  <p>No posts yet. Stay tuned for automated vibe-based coding adventures!</p>
{% endif %}
