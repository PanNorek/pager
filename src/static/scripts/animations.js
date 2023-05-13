window.addEventListener("DOMContentLoaded", function () {
	document.querySelectorAll(".dropbtn").forEach(function (btn) {
		btn.addEventListener("click", function (e) {
			e.preventDefault();
			var target = this.getAttribute("href");
			window.scrollTo({
				top: document.querySelector(target).offsetTop - 80,
				behavior: "smooth",
			});
		});
	});
});
