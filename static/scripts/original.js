function pressButton() {

    var width = 1000;
    var height = 800;
    var left = (window.innerWidth / 2) - (width / 2);
    var top = (window.innerHeight / 2) - (height / 2);


    var newW = window.open('', "Batafsil ma'lumot", `width=${width},height=${height},top=${top},left=${left}`);

    newW.document.write('<img src="images/nature.jpg" alt="Image 1" width="100%">'
                          + '<p> Some text should be here </p>')
}

document.getElementById("toggle-btn").addEventListener("click", function() {

    let navbar = document.querySelector(".navbar");
    let box = document.querySelector(".box");

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

    } else {
        navbar.classList.toggle("hidden");
    }
});

document.getElementById("topbar-btn").addEventListener("click", function() {
    document.getElementById("popover").classList.toggle("show");
});

//=============================================================================

/**
 * The code below is made for profile.html
 */

function openModalImg() {
    document.getElementById("imgModal").style.display = "flex";
}

function saveChangesImg() {
    let successMessage = document.getElementById("successMessage");
    let errorrMessage = document.getElementById("errorrMessage");

    let fileIn = document.getElementById("fileInput");
    if (fileIn.files.length === 0) {
        errorrMessage.style.display = "block";
        return;
    }

    closeModalImg();
    successMessage.style.display = "block";
    setTimeout(() => {
        successMessage.style.display = "none";
    }, 2000);
}

function openModal() {
    document.getElementById("profileModal").style.display = "flex";
}

function closeModalImg() {
    document.getElementById("imgModal").style.display = "none";
    document.getElementById("fileInput").value = "";
    document.getElementById("errorrMessage").style.display = "none";
}

function closeModal() {
    document.getElementById("profileModal").style.display = "none";
    document.getElementById("currentPassword").value = "";
    document.getElementById("newPassword").value = "";
    document.getElementById("confirmPassword").value = "";
    document.getElementById("errorMessage").style.display = "none";
}

function saveChanges() {
    let currentPassword = document.getElementById("currentPassword").value;
    let newPassword = document.getElementById("newPassword").value;
    let confirmPassword = document.getElementById("confirmPassword").value;
    let successMessage = document.getElementById("successMessage");
    let errorMessage = document.getElementById("errorMessage");

    if (newPassword !== confirmPassword) {
        errorMessage.style.display = "block";
        return;
    }

    if (currentPassword === "") {
        document.getElementById("error").textContent = "✖ Hozirgi parol bo'sh bo'la olmaydi!";
        errorMessage.style.display = "block";
        return;
    }

    if (newPassword === "") {
        document.getElementById("error").textContent = "✖ Yangi parol bo'sh bo'la olmaydi!";
        errorMessage.style.display = "block";
        return;
    }

    if (confirmPassword === "") {
        document.getElementById("error").textContent = "✖ Tasdiqlovchi parol bo'sh bo'la olmaydi!";
        errorMessage.style.display = "block";
        return;
    }

    closeModal();
    successMessage.style.display = "block";
    setTimeout(() => {
        successMessage.style.display = "none";
    }, 2000);
}