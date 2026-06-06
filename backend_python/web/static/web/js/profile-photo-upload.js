(function () {
  function getPhotoInput(trigger) {
    if (!trigger) return null;
    var inputId = trigger.getAttribute('data-photo-input-id') || trigger.getAttribute('aria-controls');
    if (!inputId) return null;
    return document.getElementById(inputId);
  }

  function notify(message) {
    if (typeof window.showSnackbar === 'function') {
      window.showSnackbar(message);
    }
  }

  function cleanUrl(url) {
    if (typeof window.safeClientUrl === 'function') return window.safeClientUrl(url);
    return String(url || '').trim();
  }

  function getCsrfToken() {
    if (typeof CSRF_TOKEN !== 'undefined') return CSRF_TOKEN;
    var tokenInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
    return tokenInput ? tokenInput.value : '';
  }

  function setProfileAvatar(url) {
    var avatar = document.getElementById('profilePageAvatar');
    var safeUrl = cleanUrl(url);
    if (avatar && safeUrl) {
      avatar.innerHTML = '<img src="' + safeUrl.replace(/"/g, '&quot;') + '" alt="Profile">';
    }
  }

  function closePhotoModal() {
    var modal = document.getElementById('photoHistoryModal');
    if (modal) modal.classList.remove('active');
  }

  function openNativePicker(input) {
    if (!input) return;
    input.value = '';
    if (typeof input.showPicker === 'function') {
      try {
        input.showPicker();
        return;
      } catch (err) {
        // Browser can reject showPicker for hidden inputs or older engines.
      }
    }
    input.click();
  }

  async function uploadPhotoFile(input) {
    if (!input || !input.files || !input.files[0]) return;
    var endpoint = input.getAttribute('data-upload-url') || '/ajax/photos/';
    var file = input.files[0];
    var formData = new FormData();
    formData.append('file', file);

    var triggers = document.querySelectorAll('[data-photo-input-id="' + input.id + '"]');
    triggers.forEach(function (trigger) { trigger.disabled = true; trigger.setAttribute('aria-busy', 'true'); });

    try {
      var response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'X-CSRFToken': getCsrfToken() },
        body: formData,
        credentials: 'same-origin'
      });
      var data = await response.json().catch(function () { return {}; });
      if (response.status === 401) {
        window.location.href = '/login/';
        return;
      }
      if (!response.ok || !data.url) {
        notify(data.error || 'Failed to upload profile picture.');
        return;
      }
      input.value = '';
      setProfileAvatar(data.url);
      closePhotoModal();
      notify('Profile picture uploaded.');
    } catch (err) {
      notify('Error uploading profile picture.');
    } finally {
      triggers.forEach(function (trigger) { trigger.disabled = false; trigger.removeAttribute('aria-busy'); });
    }
  }

  document.addEventListener('click', function (event) {
    var trigger = event.target.closest('[data-action="trigger-photo-upload"][data-photo-input-id]');
    if (!trigger) return;
    var input = getPhotoInput(trigger);
    if (!input) return;
    event.preventDefault();
    event.stopPropagation();
    openNativePicker(input);
  }, true);

  document.addEventListener('keydown', function (event) {
    if (event.key !== 'Enter' && event.key !== ' ') return;
    var trigger = event.target.closest('[data-action="trigger-photo-upload"][data-photo-input-id]');
    if (!trigger) return;
    var input = getPhotoInput(trigger);
    if (!input) return;
    event.preventDefault();
    event.stopPropagation();
    openNativePicker(input);
  }, true);

  document.addEventListener('change', function (event) {
    var input = event.target;
    if (!input || input.id !== 'modal_photo_file') return;
    event.stopPropagation();
    uploadPhotoFile(input);
  }, true);
})();
