/**
 * dynamic field - JavaScript
 *
 * @link    https://joseflorez.co
 * @license For open source use: MIT
 * @author  Jose Florez https://joseflorez.co
 * @version 1.0.0
 *
 * See usage examples at https://joseflorez.co/en/backend/django-fields-dynamic/
 */


// Initialize all event handlers on page load
document.addEventListener('DOMContentLoaded', function () {
    // Initialize select fields choice handler
    const choiceSelects = document.querySelectorAll('.form-row select');
    for (let i = 0; i < choiceSelects.length; i++) {
        addEventFile(choiceSelects[i]);
        showHiddenSelect(choiceSelects[i]);
    }

    // Initialize checkbox fields handlers
    const checkboxHandlerInputs = document.querySelectorAll('.form-row input[type=checkbox]');
    for (let i = 0; i < checkboxHandlerInputs.length; i++) {
        addEventFile(checkboxHandlerInputs[i]);
        showHiddenCheckBox(checkboxHandlerInputs[i]);
    }
});

/**
 * Add event of field handler
 * @param target: field
 */
function addEventFile(target) {
    if (target.type === "checkbox") {
        target.addEventListener('click', function (event) {
            showHiddenCheckBox(event.target);
        })
    } else {
        target.addEventListener('change', function (event) {
            showHiddenSelect(event.target);
        })
    }
}

/**
 * Search field with pre j__ and show or hidden agree value of field element checkbox
 * @param target: field element
 */
function showHiddenCheckBox(target) {
    let els = document.querySelectorAll(`.j__${target.name}`);

    for (let i = 0; i < els.length; i++) {
        if (target.checked) {
            els[i].parentNode.parentNode.classList.remove('hidden');
        } else {
            els[i].parentNode.parentNode.classList.add('hidden');
        }
    }
}

/**
 * Search field with pre j__ and show or hidden agree value of field element select
 * @param target: field element
 */
function showHiddenSelect(target) {
    let cls = "j__" + target.value;
    let els = document.querySelectorAll(`.${target.name}`);
    for (let i = 0; i < els.length; i++) {
        if (els[i].classList.contains(cls)) {
            els[i].parentNode.parentNode.classList.remove('hidden');
        } else {
            els[i].parentNode.parentNode.classList.add('hidden');
        }
    }
}