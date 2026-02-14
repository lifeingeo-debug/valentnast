/**
 * Dota 2 Hero Ranker - Python Backend Interface
 */

class Tournament {
    constructor() {
        this.state = null;
        this.initElements();
        this.bindEvents();
        this.fetchState();
    }

    initElements() {
        this.leftCard = document.getElementById('hero-left');
        this.rightCard = document.getElementById('hero-right');
        this.leftImg = document.getElementById('img-left');
        this.rightImg = document.getElementById('img-right');
        this.leftName = document.getElementById('name-left');
        this.rightName = document.getElementById('name-right');
        this.progressBar = document.getElementById('progress-bar');
        this.roundInfo = document.getElementById('round-info');
        this.resultScreen = document.getElementById('result-screen');
        this.winnerImg = document.getElementById('winner-img');
        this.winnerName = document.getElementById('winner-name');
        this.restartBtn = document.getElementById('restart-btn');
        this.mainContent = document.getElementById('main-content');
    }

    bindEvents() {
        this.leftCard.addEventListener('click', () => this.handleSelection('left'));
        this.rightCard.addEventListener('click', () => this.handleSelection('right'));
        this.restartBtn.addEventListener('click', () => this.restart());
    }

    async fetchState() {
        const response = await fetch('/state');
        const data = await response.json();
        this.updateUI(data);
    }

    updateUI(state) {
        this.state = state;

        if (state.finished) {
            this.showWinner(state.winner);
            return;
        }

        const heroA = state.hero_a;
        const heroB = state.hero_b;

        // Animate out
        this.mainContent.classList.add('transitioning');

        setTimeout(() => {
            this.leftImg.src = heroA.img;
            this.leftName.textContent = heroA.name;
            this.rightImg.src = heroB.img;
            this.rightName.textContent = heroB.name;

            this.roundInfo.textContent = `Battle ${state.match} of ${state.total}`;
            this.progressBar.style.width = `${state.progress}%`;

            this.mainContent.classList.remove('transitioning');
        }, 300);
    }

    async handleSelection(side) {
        if (this.mainContent.classList.contains('transitioning')) return;

        const winner = side === 'left' ? this.state.hero_a : this.state.hero_b;

        const response = await fetch('/vote', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ winner_id: winner.id })
        });

        const nextState = await response.json();
        this.updateUI(nextState);
    }

    showWinner(hero) {
        this.progressBar.style.width = '100%';
        this.winnerImg.src = hero.img;
        this.winnerName.textContent = hero.name;
        this.resultScreen.classList.remove('hidden');
    }

    async restart() {
        this.resultScreen.classList.add('hidden');
        const response = await fetch('/restart', { method: 'POST' });
        const nextState = await response.json();
        this.updateUI(nextState);
    }
}

// Initialize on load
window.addEventListener('DOMContentLoaded', () => {
    new Tournament();
});
