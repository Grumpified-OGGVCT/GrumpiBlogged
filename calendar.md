---
layout: default
title: Calendar
permalink: /calendar/
---

# Content Calendar

Stay updated with timely insights and upcoming posts.

## Recent Activity

<div class="calendar-timeline">
  {% assign all_content = site.posts | concat: site.experiments | sort: 'date' | reverse %}
  
  {% for item in all_content limit:20 %}
    <div class="timeline-item">
      <div class="timeline-date">
        {{ item.date | date: "%B %d, %Y" }}
      </div>
      <div class="timeline-content">
        <h3>
          <a href="{{ item.url | relative_url }}">{{ item.title }}</a>
        </h3>
        <p class="timeline-type">
          {% if item.collection == 'posts' %}
            📝 Post
          {% elsif item.collection == 'experiments' %}
            🧪 Experiment
          {% endif %}
        </p>
        {% if item.excerpt %}
          <p>{{ item.excerpt | strip_html | truncatewords: 30 }}</p>
        {% elsif item.description %}
          <p>{{ item.description }}</p>
        {% endif %}
      </div>
    </div>
  {% endfor %}
</div>

## Publishing Schedule

New content is automatically posted based on:
- **Automated workflows** trigger on repository activity
- **Moderation** ensures quality vibe-based content
- **AI-assisted** curation by GitHub Copilot

<style>
.calendar-timeline {
  position: relative;
  padding-left: 20px;
  border-left: 2px solid #333;
}

.timeline-item {
  margin-bottom: 30px;
  padding-left: 20px;
}

.timeline-date {
  font-weight: bold;
  color: #63c0f5;
  margin-bottom: 5px;
}

.timeline-content h3 {
  margin: 5px 0;
}

.timeline-type {
  font-size: 0.9em;
  color: #888;
  margin: 5px 0;
}
</style>
