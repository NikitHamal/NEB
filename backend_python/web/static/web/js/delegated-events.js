(function() {
  var actions = {};

  function getActionEl(el) {
    var current = el;
    while (current && current !== document.body) {
      if (current.dataset) {
        // data-action-stop must be checked first so modal/sheet cards can
        // prevent backdrop actions from intercepting nested links, radio
        // buttons, and follower cards.
        if (current.dataset.actionStop !== undefined) return null;
        if (current.dataset.action && current.tagName !== 'FORM') return current;
      }
      current = current.parentElement;
    }
    return null;
  }

  document.addEventListener('click', function(e) {
    var el = getActionEl(e.target);
    if (el && el.dataset.action && actions[el.dataset.action]) {
      e.preventDefault();
      actions[el.dataset.action](el, e);
      return;
    }
    var linkEl = e.target.closest('a[data-link-id]');
    if (linkEl && linkEl.dataset.trackClick !== 'false') {
      trackSocialLinkClick(linkEl);
    }
  });

  document.addEventListener('submit', function(e) {
    var form = e.target;
    if (form && form.dataset && form.dataset.action) {
      var action = form.dataset.action;
      if (actions[action]) {
        e.preventDefault();
        actions[action](form, e);
      }
    }
  });

  document.addEventListener('keydown', function(e) {
    var el = e.target;
    if (el && el.dataset && el.dataset.keydownAction) {
      var action = el.dataset.keydownAction;
      if (actions[action]) {
        actions[action](el, e);
      }
    }
  });

  document.addEventListener('change', function(e) {
    var el = e.target;
    if (el && el.dataset && el.dataset.changeAction) {
      var action = el.dataset.changeAction;
      if (actions[action]) {
        actions[action](el, e);
      }
    }
  });

  document.addEventListener('focusin', function(e) {
    var el = e.target;
    if (el && el.dataset && el.dataset.focusAction) {
      var action = el.dataset.focusAction;
      if (actions[action]) actions[action](el, e);
    }
  });

  document.addEventListener('focusout', function(e) {
    var el = e.target;
    if (el && el.dataset && el.dataset.blurAction) {
      var action = el.dataset.blurAction;
      if (actions[action]) actions[action](el, e);
    }
  });

  document.addEventListener('mousedown', function(e) {
    var el = getActionEl(e.target);
    if (!el) return;
    var action = el.dataset.mousedownAction;
    if (action && actions[action]) {
      actions[action](el, e);
    }
  });

  document.addEventListener('mouseover', function(e) {
    var el = e.target;
    if (el && el.dataset && el.dataset.hoverAction) {
      var action = el.dataset.hoverAction;
      if (actions[action]) actions[action](el, e);
    }
  });

  document.addEventListener('error', function(e) {
    var img = e.target;
    if (!img || img.tagName !== 'IMG') return;
    if (img.classList && img.classList.contains('resource-card-art-img')) {
      img.remove();
      return;
    }
    if (img.dataset.fallback) {
      img.style.display = 'none';
      var next = img.nextElementSibling;
      if (next) next.style.display = img.dataset.fallback || 'inline-flex';
      return;
    }
    if (img.dataset.hideOnError !== undefined) {
      img.style.display = 'none';
      return;
    }
  }, true);

  window.registerAction = function(name, fn) {
    actions[name] = fn;
  };

  window.registerActions = function(map) {
    for (var key in map) {
      if (map.hasOwnProperty(key)) actions[key] = map[key];
    }
  };

  window.trackSocialLinkClick = function(linkEl) {
    var payload = JSON.stringify({
      link_id: linkEl.dataset.linkId,
      user_id: linkEl.dataset.linkUserId,
      platform: linkEl.dataset.linkPlatform,
      url: linkEl.dataset.linkUrl,
    });
    navigator.sendBeacon('/ajax/social-links/track-click/', payload);
  };

  window.openImageLightbox = function(images, initialIndex) {
    if (!images) return;
    var imgList = Array.isArray(images) ? images : [images];
    if (imgList.length === 0) return;

    var idx = Math.max(0, Math.min(initialIndex || 0, imgList.length - 1));

    var existing = document.querySelector('.nebians-lightbox-overlay');
    if (existing) existing.remove();

    var overlay = document.createElement('div');
    overlay.className = 'nebians-lightbox-overlay';
    overlay.setAttribute('tabindex', '0');

    var topbar = document.createElement('div');
    topbar.className = 'nebians-lightbox-topbar';
    var counter = document.createElement('span');
    counter.className = 'nebians-lightbox-counter';
    counter.textContent = (idx + 1) + ' / ' + imgList.length;

    var closeBtn = document.createElement('button');
    closeBtn.className = 'nebians-lightbox-close';
    closeBtn.setAttribute('aria-label', 'Close');
    closeBtn.innerHTML = '<span class="material-symbols-outlined">close</span>';
    closeBtn.onclick = function() { overlay.remove(); };

    topbar.appendChild(counter);
    topbar.appendChild(closeBtn);

    var body = document.createElement('div');
    body.className = 'nebians-lightbox-body';

    var prevBtn = document.createElement('button');
    prevBtn.className = 'nebians-lightbox-nav prev';
    prevBtn.setAttribute('aria-label', 'Previous image');
    prevBtn.innerHTML = '<span class="material-symbols-outlined">chevron_left</span>';
    prevBtn.style.display = imgList.length > 1 ? 'flex' : 'none';

    var nextBtn = document.createElement('button');
    nextBtn.className = 'nebians-lightbox-nav next';
    nextBtn.setAttribute('aria-label', 'Next image');
    nextBtn.innerHTML = '<span class="material-symbols-outlined">chevron_right</span>';
    nextBtn.style.display = imgList.length > 1 ? 'flex' : 'none';

    var imgWrap = document.createElement('div');
    imgWrap.className = 'nebians-lightbox-img-wrap';
    var mainImg = document.createElement('img');
    mainImg.className = 'nebians-lightbox-img';
    mainImg.src = imgList[idx];
    imgWrap.appendChild(mainImg);

    body.appendChild(prevBtn);
    body.appendChild(imgWrap);
    body.appendChild(nextBtn);

    var thumbsDiv = document.createElement('div');
    thumbsDiv.className = 'nebians-lightbox-thumbs';
    if (imgList.length > 1) {
      imgList.forEach(function(src, i) {
        var thumb = document.createElement('img');
        thumb.className = 'nebians-lightbox-thumb' + (i === idx ? ' active' : '');
        thumb.src = src;
        thumb.onclick = function() { updateImage(i); };
        thumbsDiv.appendChild(thumb);
      });
    } else {
      thumbsDiv.style.display = 'none';
    }

    function updateImage(newIdx) {
      idx = (newIdx + imgList.length) % imgList.length;
      mainImg.src = imgList[idx];
      counter.textContent = (idx + 1) + ' / ' + imgList.length;
      var thumbs = thumbsDiv.querySelectorAll('.nebians-lightbox-thumb');
      thumbs.forEach(function(t, i) {
        if (i === idx) t.classList.add('active');
        else t.classList.remove('active');
      });
    }

    prevBtn.onclick = function(e) { e.stopPropagation(); updateImage(idx - 1); };
    nextBtn.onclick = function(e) { e.stopPropagation(); updateImage(idx + 1); };

    overlay.addEventListener('click', function(e) {
      if (e.target === overlay || e.target === imgWrap) overlay.remove();
    });

    overlay.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') overlay.remove();
      else if (e.key === 'ArrowLeft' && imgList.length > 1) updateImage(idx - 1);
      else if (e.key === 'ArrowRight' && imgList.length > 1) updateImage(idx + 1);
    });

    overlay.appendChild(topbar);
    overlay.appendChild(body);
    overlay.appendChild(thumbsDiv);

    document.body.appendChild(overlay);
    overlay.focus();
  };

  actions['open-image-lightbox'] = function(el, e) {
    var src = el.dataset.src || el.src;
    var allImagesAttr = el.dataset.allImages;
    var indexAttr = parseInt(el.dataset.index || '0', 10);

    var imagesList = [];
    if (allImagesAttr) {
      imagesList = allImagesAttr.split('|').filter(Boolean);
    } else {
      var container = el.closest('.post-card-media-grid, .post-card-images, .fp-post-images, .post-card');
      if (container) {
        var imgs = container.querySelectorAll('img[data-src], img.post-card-thumb, img');
        imgs.forEach(function(imgEl) {
          var s = imgEl.dataset.src || imgEl.src;
          if (s && imagesList.indexOf(s) === -1) imagesList.push(s);
        });
        indexAttr = imagesList.indexOf(src);
        if (indexAttr === -1) indexAttr = 0;
      }
    }

    if (imagesList.length === 0) imagesList = [src];
    window.openImageLightbox(imagesList, indexAttr);
  };


  actions['fp-slide-prev'] = function(el, e) {
    var container = el.closest('.fp-post-slider-container');
    if (!container) return;
    var slider = container.querySelector('.fp-post-images-slider');
    if (slider) slider.scrollBy({ left: -332, behavior: 'smooth' });
  };

  actions['fp-slide-next'] = function(el, e) {
    var container = el.closest('.fp-post-slider-container');
    if (!container) return;
    var slider = container.querySelector('.fp-post-images-slider');
    if (slider) slider.scrollBy({ left: 332, behavior: 'smooth' });
  };

  document.addEventListener('scroll', function(e) {
    if (e.target && e.target.classList && e.target.classList.contains('fp-post-images-slider')) {
      var slider = e.target;
      var container = slider.closest('.fp-post-slider-container');
      if (!container) return;
      var prev = container.querySelector('.fp-slider-prev');
      var next = container.querySelector('.fp-slider-next');
      if (prev) prev.style.display = slider.scrollLeft > 10 ? 'flex' : 'none';
      if (next) next.style.display = (slider.scrollLeft + slider.clientWidth) < (slider.scrollWidth - 10) ? 'flex' : 'none';
    }
  }, true);

})();
