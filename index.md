---
layout: default
title: 首頁
---

<div class="home">
  <h1>KUNI's Blog</h1>
  <p class="description">KUNI's Blog</p>

  <h2>所有文章</h2>
  
  <div class="post-list">
    {% assign posts_by_year = site.posts | group_by_exp: "post", "post.date | date: '%Y'" %}
    {% for year in posts_by_year %}
      <h3 class="year-header">{{ year.name }} 年</h3>
      <ul class="posts">
        {% for post in year.items %}
          <li>
            <span class="post-date">{{ post.date | date: "%m月%d日" }}</span>
            <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
            {% if post.categories.size > 0 %}
              <span class="post-category">· {{ post.categories | join: ", " }}</span>
            {% endif %}
          </li>
        {% endfor %}
      </ul>
    {% endfor %}
  </div>
  
  <p class="post-count">總共 {{ site.posts.size }} 篇文章</p>
</div>

<style>
.home h1 {
  margin-bottom: 0.5em;
}

.home .description {
  color: #666;
  margin-bottom: 2em;
  font-size: 1.1em;
}

.post-list {
  margin-top: 2em;
}

.year-header {
  color: #333;
  border-bottom: 2px solid #e8e8e8;
  padding-bottom: 0.3em;
  margin-top: 2em;
  margin-bottom: 1em;
}

.posts {
  list-style: none;
  padding-left: 0;
}

.posts li {
  margin-bottom: 0.8em;
  padding: 0.5em 0;
  border-bottom: 1px solid #f0f0f0;
}

.posts li:hover {
  background-color: #f9f9f9;
  padding-left: 0.5em;
  margin-left: -0.5em;
}

.post-date {
  color: #828282;
  font-size: 0.9em;
  margin-right: 1em;
  font-family: monospace;
  min-width: 60px;
  display: inline-block;
}

.post-category {
  color: #999;
  font-size: 0.85em;
  margin-left: 0.5em;
}

.post-count {
  margin-top: 3em;
  text-align: center;
  color: #666;
  font-style: italic;
}
</style>
