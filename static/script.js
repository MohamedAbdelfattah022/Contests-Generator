document.addEventListener("DOMContentLoaded", function () {
	var modal = document.getElementById("errorModal");
	var closeBtn = document.querySelector(".modal .close");

	var errorMessage = modal.getAttribute("data-error-message");

	if (errorMessage) {
		document.getElementById("errorMessage").textContent = errorMessage;
		modal.style.display = "block";
	}

	closeBtn.onclick = function () {
		modal.style.display = "none";
	};

	window.onclick = function (event) {
		if (event.target === modal) {
			modal.style.display = "none";
		}
	};
});

// copy button
document.addEventListener("DOMContentLoaded", function () {
	const copyButton = document.getElementById("copyButton");
	const problemCodes = document.getElementById("problem_codes");

	async function copyToClipboard() {
		try {
			await navigator.clipboard.writeText(problemCodes.value);
			copyButton.innerHTML = "Copied";
			setTimeout(() => {
				copyButton.innerHTML = "Copy Codes";
			}, 3000);
		} catch (err) {
			alert("Failed to copy. Please try again.");
		}
	}
	copyButton.addEventListener("click", copyToClipboard);
});
