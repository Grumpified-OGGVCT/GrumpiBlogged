---
layout: default
title: Experiments
permalink: /experiments/
---

# Vibe-Based Coding Experiments

Explore the collection of coding experiments, prototypes, and real-world AI adventures.

<div class="experiments-list">
  {% for experiment in site.experiments %}
    <article class="experiment-summary">
      <h2><a href="{{ experiment.url | relative_url }}">{{ experiment.title }}</a></h2>
      {% if experiment.date %}
        <p class="experiment-meta">{{ experiment.date | date: "%B %d, %Y" }}
        {% if experiment.status %} • <span class="status {{ experiment.status }}">{{ experiment.status }}</span>{% endif %}
        </p>
      {% endif %}
      {% if experiment.description %}
        <p>{{ experiment.description }}</p>
      {% endif %}
      <p><a href="{{ experiment.url | relative_url }}">View experiment →</a></p>
    </article>
    <hr>
  {% endfor %}
</div>

{% if site.experiments.size == 0 %}
  <p>No experiments yet. Coming soon!</p>
{% endif %}
