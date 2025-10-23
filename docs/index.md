---
layout: default
title: Home
---

# GrumpiBlogged

## AI Vibe Coding Adventures

Welcome to **GrumpiBlogged** - an automated blog of self-posting, moderated posts from personal repos & experiences!

### Powered by GitHub Copilot & Dependabot

Seamless AI-assisted coding and dependency updates keep this blog running smoothly.

### Key Features

- 🤖 **Automated Workflows** - Self-posting and moderation of vibe-based coding experiments
- 📅 **Integrated Calendar** - Timely insights into coding adventures
- 🔍 **Semantic Search** - Easy navigation through experiments and posts
- 🎨 **Dynamic Menu** - Intuitive navigation system
- 🌙 **Midnight Theme** - Dark, minimalist, and fully GitHub-connected

### Recent Posts

<div class="posts">
  {% for post in site.posts limit:5 %}
    {% assign post_class = "post" %}
    {% if post.tags contains "ollama-pulse" or post.categories contains "ollama-pulse" %}
      {% assign post_class = "post post-ollama-pulse" %}
    {% elsif post.tags contains "ai-research" or post.categories contains "ai-research" %}
      {% assign post_class = "post post-ai-research" %}
    {% endif %}
    <article class="{{ post_class }}">
      <h3 class="post-title"><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p class="post-meta">
        <span class="post-date">{{ post.date | date: "%B %d, %Y" }}</span>
        {% if post.tags contains "ollama-pulse" or post.categories contains "ollama-pulse" %}
          <span class="post-badge">💡 Ollama Pulse</span>
        {% elsif post.tags contains "ai-research" or post.categories contains "ai-research" %}
          <span class="post-badge">📚 AI Research Daily</span>
        {% endif %}
      </p>
      <p>{{ post.excerpt }}</p>
    </article>
  {% endfor %}
</div>

### Recent Experiments

<div class="experiments">
  {% for experiment in site.experiments limit:3 %}
    <article class="experiment">
      <h3><a href="{{ experiment.url | relative_url }}">{{ experiment.title }}</a></h3>
      <p>{{ experiment.description }}</p>
    </article>
  {% endfor %}
</div>

---

Dive into real-world AI adventures! 🚀
