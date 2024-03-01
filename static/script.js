class BoggleGame {
	constructor(seconds = 5) {
		this.score = 0;
		this.seconds = seconds;
		this.gameClock = setInterval(this.tick.bind(this), 1000);

		$('#guess-form').on('submit', this.handleSubmit.bind(this));
	}

	handleSubmit(evt) {
		evt.preventDefault();

		if (this.seconds <= 0) {
			$('.msg').text('Time is up! No more guesses.');
			return;
		}

		const guess = $('#guess-input').val();

		axios.get('/guess', { params: { guess } }).then(response => {
			const result = response.data.result;
			this.showMsg(guess, result);
			$('#guess-input').val('')
		});

	}

	tick() {
		this.seconds -= 1;
		this.showTimer();

		if (this.seconds == 0) {
			clearInterval(this.gameClock);
			this.endGame()
		}
	}

	showTimer() {
		$('.game-clock').text(`Time: ${this.seconds}`);
	}

	showMsg(word, result) {
		word = word.toUpperCase();
		if (result == 'ok') {
			$('.msg').text(`Added ${word}!`);
			this.showScore(word);
		} else if (result == 'not-on-board') {
			$('.msg').text(`${word} is not on the board!`);
		} else {
			$('.msg').text(`${word} is not a valid word!`);
		}
	}

	showScore(word) {
		this.score += word.length;
		$('.score').text(`Score: ${this.score}`);
	}

	async endGame() {
		await axios.post('/end-game', {'score': this.score})
	}
}
