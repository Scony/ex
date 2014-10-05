$(function () {

    renderPopular();

    $('#commandsb').click(function () {
	renderCommands();
    });

    $('#examplesb').click(function () {
	renderExamples();
    });

    $('#searchb').click(function () {
	renderCommand($('#searchi').val());
    });
});
