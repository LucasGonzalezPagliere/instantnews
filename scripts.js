document.addEventListener("DOMContentLoaded", function () {
    fetchNews();
});

function fetchNews() {
    const apiUrl = "https://lucasthedev.pythonanywhere.com/get_news";

    fetch(apiUrl)
        .then((response) => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Could not fetch news data.');
            }
        })
        .then((newsItems) => {
            displayNewsItems(newsItems);
        })
        .catch((error) => {
            console.error('Error fetching news data:', error);
        });
}

function displayNewsItems(newsItems) {
    const newsContainer = document.getElementById("news-container");

    newsItems.forEach((newsItem) => {
        const newsDiv = document.createElement("div");
        newsDiv.className = "news-item";

        newsDiv.innerHTML = `
            <div class="news-summary">
                <h2>${newsItem.tweet}</h2>
            </div>
            <div class="news-details">
                <ul>
                    ${newsItem.bulletPoints.map((point) => `<li>${point}</li>`).join("")}
                </ul>
            </div>
        `;

        newsDiv.addEventListener("click", function () {
            this.classList.toggle("expanded");
        });

        newsContainer.appendChild(newsDiv);
    });
}