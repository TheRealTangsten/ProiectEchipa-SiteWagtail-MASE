document.addEventListener("DOMContentLoaded", function () {
    const checkbox = document.getElementById("legal-person-checkbox");
    const companyField = document.getElementById("company-name-field");

    checkbox.addEventListener("change", function () {
        if (checkbox.checked) {
            companyField.style.display = "block";
        } else {
            companyField.style.display = "none";
        }
    });
});
