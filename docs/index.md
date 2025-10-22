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
    <article class="post">
      <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
      <p class="post-meta">{{ post.date | date: "%B %d, %Y" }}</p>
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
