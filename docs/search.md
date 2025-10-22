---
layout: default
title: Search
permalink: /search/
---

# Semantic Search

Find content across all posts and experiments with intelligent search.

<div id="search-container">
  <input type="text" id="search-input" placeholder="Search posts and experiments..." />
  <div id="search-results"></div>
</div>

<script>
// Simple client-side search implementation
(function() {
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  
  // Gather all searchable content
  const content = [
    {% for post in site.posts %}
    {
      title: "{{ post.title | escape }}",
      url: "{{ post.url | relative_url }}",
      excerpt: "{{ post.excerpt | strip_html | escape }}",
      date: "{{ post.date | date: '%B %d, %Y' }}",
      type: "Post",
      tags: [{% for tag in post.tags %}"{{ tag }}"{% unless forloop.last %},{% endunless %}{% endfor %}]
    }{% unless forloop.last %},{% endunless %}
    {% endfor %}
    {% if site.posts.size > 0 and site.experiments.size > 0 %},{% endif %}
    {% for experiment in site.experiments %}
    {
      title: "{{ experiment.title | escape }}",
      url: "{{ experiment.url | relative_url }}",
      excerpt: "{{ experiment.description | default: experiment.excerpt | strip_html | escape }}",
      date: "{{ experiment.date | date: '%B %d, %Y' }}",
      type: "Experiment"
    }{% unless forloop.last %},{% endunless %}
    {% endfor %}
  ];

  searchInput.addEventListener('input', function(e) {
    const query = e.target.value.toLowerCase().trim();
    
    if (query.length < 2) {
      searchResults.innerHTML = '';
      return;
    }

    // Semantic search: match title, excerpt, tags
    const results = content.filter(item => {
      const titleMatch = item.title.toLowerCase().includes(query);
      const excerptMatch = item.excerpt.toLowerCase().includes(query);
      const tagsMatch = item.tags && item.tags.some(tag => tag.toLowerCase().includes(query));
      return titleMatch || excerptMatch || tagsMatch;
    });

    if (results.length === 0) {
      searchResults.innerHTML = '<p class="no-results">No results found for "' + query + '"</p>';
      return;
    }

    let html = '<div class="search-results-list">';
    results.forEach(item => {
      html += '<article class="search-result">';
      html += '<h3><a href="' + item.url + '">' + item.title + '</a></h3>';
      html += '<p class="result-meta">' + item.type + ' • ' + item.date + '</p>';
      html += '<p>' + item.excerpt + '</p>';
      html += '</article>';
    });
    html += '</div>';
    
    searchResults.innerHTML = html;
  });
})();
</script>

<style>
#search-container {
  margin: 20px 0;
}

#search-input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 2px solid #333;
  border-radius: 4px;
  background-color: #1a1a1a;
  color: #fff;
}

#search-input:focus {
  outline: none;
  border-color: #63c0f5;
}

.search-results-list {
  margin-top: 20px;
}

.search-result {
  padding: 20px;
  margin: 15px 0;
  background-color: #1a1a1a;
  border-left: 3px solid #63c0f5;
}

.search-result h3 {
  margin-top: 0;
}

.result-meta {
  color: #888;
  font-size: 0.9em;
  margin: 5px 0;
}

.no-results {
  color: #888;
  font-style: italic;
  margin-top: 20px;
}
</style>
