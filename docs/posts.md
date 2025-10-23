---
layout: default
title: All Posts
permalink: /posts/
---

# All Posts

Browse through all the AI vibe coding adventures and automated posts.

<div class="posts-list">
  {% for post in site.posts %}
    {% comment %}
      Determine post type for visual differentiation
    {% endcomment %}
    {% assign post_type = "default" %}
    {% if post.tags contains "ollama" or post.tags contains "daily-pulse" or post.persona %}
      {% assign post_type = "ollama-pulse" %}
    {% elsif post.tags contains "research" or post.tags contains "ai-research" or post.categories contains "ai-research" %}
      {% assign post_type = "ai-research" %}
    {% endif %}

    <article class="post-summary post-{{ post_type }}">
      <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
      <p class="post-meta">
        {{ post.date | date: "%B %d, %Y" }}
        {% if post.author %} • <span class="post-author">{{ post.author }}</span>{% endif %}
        {% if post_type == "ollama-pulse" %}
          <span class="post-type-badge" style="background: rgba(255, 165, 0, 0.2); color: #FFB733; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; margin-left: 8px;">💡 Ollama Pulse</span>
        {% elsif post_type == "ai-research" %}
          <span class="post-type-badge" style="background: rgba(220, 20, 60, 0.2); color: #E94B6B; padding: 4px 10px; border-radius: 12px; font-size: 0.75rem; margin-left: 8px;">📚 AI Research</span>
        {% endif %}
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
