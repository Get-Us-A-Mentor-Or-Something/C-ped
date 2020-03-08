/* eslint-env es6, browser*/
/* eslint-disable no-console */

const socket = io();

function collectData() {
	return {};
}

function sendData() {
	let data = collectData();
	socket.emit("data", {data: data});
}

window.onload = function() {
};
