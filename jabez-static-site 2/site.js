(() => {
  const publications = window.PUBLICATIONS || [];
  const projects = window.PROJECTS || [];

  const esc = (s = "") =>
    String(s).replace(/[&<>"']/g, ch => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;"
    })[ch]);

  const linksHTML = links =>
    (links || [])
      .map(link => `<a href="${esc(link.href)}">${esc(link.label)}</a>`)
      .join("");

  const selected = publications.filter(p => p.selected);
  document.getElementById("selected-publications").innerHTML = selected
    .map(p => `
      <article class="research-item ${p.thumbnail ? "" : "no-thumb"}">
        ${p.thumbnail ? `<img class="paper-thumb" src="${esc(p.thumbnail)}" alt="">` : ""}
        <div>
          <h3 class="research-title">
            <a href="${esc((p.links && p.links[0]?.href) || "#")}">${esc(p.title)}</a>
            ${p.badge ? `<span class="badge">${esc(p.badge)}</span>` : ""}
          </h3>
          <p class="authors">${esc(p.authors)}</p>
          <p class="venue">${esc(p.venue)}</p>
          ${p.summary ? `<p class="summary">${esc(p.summary)}</p>` : ""}
          <div class="item-links">${linksHTML(p.links)}</div>
        </div>
      </article>
    `)
    .join("");

  document.getElementById("projects-list").innerHTML = projects
    .map(project => `
      <article class="project-row">
        <div class="project-year">${esc(project.year)}</div>
        <div>
          <h3 class="project-title">${esc(project.title)}</h3>
          <p class="project-description">${esc(project.description)}</p>
          <div class="project-tags">${esc((project.tags || []).join(" · "))}</div>
          ${project.links?.length
            ? `<div class="item-links" style="margin-top:6px">${linksHTML(project.links)}</div>`
            : ""}
        </div>
      </article>
    `)
    .join("");

  const byYear = publications.reduce((acc, p) => {
    (acc[p.year] ||= []).push(p);
    return acc;
  }, {});

  const years = Object.keys(byYear).sort((a, b) =>
    String(b).localeCompare(String(a), undefined, { numeric: true })
  );

  document.getElementById("publication-list").innerHTML = years
    .map(year => `
      <section class="publication-year">
        <div class="year-label">${esc(year)}</div>
        <div>
          ${byYear[year].map(p => `
            <article class="pub-row">
              <h3 class="pub-title">${esc(p.title)}</h3>
              <div class="authors">${esc(p.authors)}</div>
              <div class="venue">${esc(p.venue)}</div>
              <div class="item-links">${linksHTML(p.links)}</div>
            </article>
          `).join("")}
        </div>
      </section>
    `)
    .join("");

  document.getElementById("year").textContent = new Date().getFullYear();
})();
