const $guessForm = $('#guess');
const $guessInput = $('#guess input');

$guessForm.on('submit', function (evt) {
    evt.preventDefault()

	guess = $guessInput.val();
	console.log('Here');

	axios.post('/guess', { guess: guess });
});
