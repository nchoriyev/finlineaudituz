document.getElementById("toggle-btn").addEventListener("click", function() {

    let navbar = document.querySelector(".navbar");
    let box = document.querySelector(".box");
    let backdrop = document.querySelector(".navbar-backdrop");

    if (window.innerWidth > 1080) {

        if (box.classList.contains("expand")) {
            box.classList.remove("expand");
            box.classList.add("shrink");
          } else {
            box.classList.remove("shrink");
            box.classList.add("expand");
        }

        box.classList.toggle("thick");
        navbar.classList.toggle("thin");

    } else if (window.innerWidth <= 1080) {
        navbar.classList.toggle("hidden");
        backdrop.classList.toggle("visible");
    }
});

document.getElementById("topbar-btn").addEventListener("click", function() {
    document.getElementById("popover").classList.toggle("show");
});


/**
 * The code below is for video
 */

document.querySelector('.video-js').addEventListener('contextmenu', function(e) {
    e.preventDefault(); // Disable right-click
});

// Fullscreen toggle on 'f' key press
document.addEventListener('keydown', function(event) {
    const video = document.querySelector('.video-js');

    if (event.key === 'f') {
        if (document.fullscreenElement) {
            document.exitFullscreen();  // Exit fullscreen
        } else {
            video.requestFullscreen();  // Enter fullscreen
        }
    }
});

async function loadVideo() {
            let videoId = "9f687ef086b14b2da53f484de8e4a534";  // O'zingizning video ID-ingizni kiriting
            let response = await fetch(`/video-otp/${videoId}/`);
            let data = await response.json();

            if (data.otp && data.playbackInfo) {
                document.getElementById("vdo-player").src =
                    `https://player.vdocipher.com/v2/?otp=${data.otp}&playbackInfo=${data.playbackInfo}`;
            } else {
                console.error("OTP olishda xatolik:", data);
            }
        }
        window.onload = loadVideo;