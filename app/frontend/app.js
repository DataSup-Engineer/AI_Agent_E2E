const keywordsInput = document.getElementById('keywords');
const generateBtn = document.getElementById('generate-btn');
const statusBar = document.getElementById('status-bar');
const statusText = document.getElementById('status-text');
const storyDisplay = document.getElementById('story-display');
const scenesContainer = document.getElementById('scenes-container');
const charactersDiv = document.getElementById('characters');

let socket;

generateBtn.addEventListener('click', () => {
    const keywords = keywordsInput.value.trim();
    if (!keywords) return;

    // Reset UI
    scenesContainer.innerHTML = '';
    charactersDiv.innerHTML = '';
    storyDisplay.classList.add('hidden');
    statusBar.classList.remove('hidden');
    statusText.innerText = 'Connecting to magical server...';

    // Connect to WebSocket
    socket = new WebSocket(`ws://${window.location.host}/ws/generate`);

    socket.onopen = () => {
        statusText.innerText = 'Sharing your ideas with the AI...';
        socket.send(keywords);
    };

    socket.onmessage = (event) => {
        const msg = JSON.parse(event.data);

        switch (msg.status) {
            case 'starting':
                statusText.innerText = msg.message;
                break;
            case 'story_done':
                renderStory(msg.data);
                statusText.innerText = 'Story written! Now painting the pictures...';
                break;
            case 'generating_image':
                statusText.innerText = `Painting scene ${msg.scene}...`;
                break;
            case 'image_done':
                updateSceneImage(msg.scene, msg.image_url, msg.error);
                break;
            case 'complete':
                statusText.innerText = 'Adventure complete!';
                setTimeout(() => statusBar.classList.add('hidden'), 3000);
                break;
            case 'error':
                statusText.innerText = `Error: ${msg.message}`;
                break;
        }
    };

    socket.onclose = () => {
        console.log('Connection closed');
    };
});

function renderStory(data) {
    storyDisplay.classList.remove('hidden');
    
    // Render Characters
    data.main_characters.forEach(char => {
        const tag = document.createElement('span');
        tag.className = 'character-tag';
        tag.innerText = char.name;
        tag.title = char.description;
        charactersDiv.appendChild(tag);
    });

    // Render Scenes (Initial)
    data.scenes.forEach(scene => {
        const card = document.createElement('div');
        card.className = 'scene-card';
        card.id = `scene-${scene.index}`;
        card.innerHTML = `
            <div class="image-placeholder" style="height: 400px; background: #334155; display: flex; align-items: center; justify-content: center;">
                <p>Waiting for magic brush...</p>
            </div>
            <div class="scene-content">
                <h3>Scene ${scene.index}: ${scene.title}</h3>
                <p class="scene-text">${scene.text}</p>
            </div>
        `;
        scenesContainer.appendChild(card);
    });
}

function updateSceneImage(index, url, error) {
    const sceneCard = document.getElementById(`scene-${index}`);
    if (!sceneCard) return;

    const placeholder = sceneCard.querySelector('.image-placeholder');
    if (error) {
        placeholder.innerHTML = `<p style="color: #ef4444">Failed to paint: ${error}</p>`;
        return;
    }

    if (url) {
        const img = document.createElement('img');
        img.className = 'scene-image';
        img.src = url;
        img.alt = `Scene ${index}`;
        sceneCard.replaceChild(img, placeholder);
    }
}
