(function() {
  var currentExam = 'neb';
  var isReexam = false;
  var currentMode = 'single';

  function getExamCode() { return isReexam ? currentExam + '_reexam' : currentExam; }
  
  var form = document.getElementById('rc-form');
  var tabs = document.getElementById('rc-tabs');
  var subTabs = document.getElementById('rc-sub-tabs');
  var reexamToggle = document.getElementById('rc-reexam-toggle');
  var dobWrapper = document.getElementById('rc-field-dob-wrapper');
  var dobInput = document.getElementById('dob');
  var bulkField = document.getElementById('rc-field-bulk-wrapper');
  var bulkInput = document.getElementById('bulk-input');
  var submitBtn = document.getElementById('rc-submit-btn');
  var submitText = document.getElementById('rc-submit-text');

  var isCheckingBulk = false;
  var bulkCancel = false;

  function needsDob() {
    return currentExam === 'neb';
  }

  // Initial Setup
  updateFieldsForMode();
  updateBulkHint();

  function switchExam(exam) {
    if (currentExam === exam) return;
    currentExam = exam;

    // Toggle active state in tabs
    tabs.querySelectorAll('.rc-tab').forEach(function(t) {
      t.classList.toggle('active', t.dataset.exam === exam);
    });

    updateFieldsForMode();
    updateBulkHint();

    // Clean outputs
    resetOutputs();
  }

  function switchMode(mode) {
    if (currentMode === mode) return;

    if (isCheckingBulk) {
      if (confirm('Cancel current bulk operation?')) {
        bulkCancel = true;
      } else {
        return;
      }
    }

    currentMode = mode;
    subTabs.querySelectorAll('.rc-sub-tab').forEach(function(t) {
      t.classList.toggle('active', t.dataset.mode === mode);
    });

    updateFieldsForMode();

    // Clean outputs
    resetOutputs();
  }

  function updateFieldsForMode() {
    if (currentMode === 'bulk') {
      // Hide single inputs
      document.getElementById('symbol').required = false;
      document.getElementById('symbol').parentElement.style.display = 'none';
      dobWrapper.classList.remove('visible');
      dobInput.required = false;

      // Show bulk input
      bulkField.style.display = 'block';
      bulkInput.required = true;
      submitText.textContent = 'Run Bulk Check';
    } else {
      // Show single inputs
      document.getElementById('symbol').required = true;
      document.getElementById('symbol').parentElement.style.display = 'block';
      
      if (needsDob()) {
        dobWrapper.classList.add('visible');
        dobInput.required = true;
      } else {
        dobWrapper.classList.remove('visible');
        dobInput.required = false;
        dobInput.value = '';
      }

      // Hide bulk input
      bulkField.style.display = 'none';
      bulkInput.required = false;
      submitText.textContent = 'Check Result';
    }
  }

  function updateBulkHint() {
    var hint = document.getElementById('rc-bulk-hint');
    if (needsDob()) {
      hint.textContent = 'One per line: symbol,YYYY/MM/DD';
      bulkInput.placeholder = 'e.g. 20404641,2065/03/15\n20404642,2065/03/16';
    } else {
      hint.textContent = 'One symbol number per line';
      bulkInput.placeholder = 'e.g. 12013825\n12013826';
    }
  }

  function resetOutputs() {
    document.getElementById('rc-result-container').style.display = 'none';
    document.getElementById('rc-bulk-results-container').style.display = 'none';
    document.getElementById('rc-progress-container').style.display = 'none';
    document.getElementById('rc-progress-text').style.display = 'none';
    document.getElementById('rc-error').style.display = 'none';
    window.currentResultData = null;
  }

  tabs.addEventListener('click', function(e) {
    var tab = e.target.closest('.rc-tab');
    if (tab) switchExam(tab.dataset.exam);
  });

  subTabs.addEventListener('click', function(e) {
    var tab = e.target.closest('.rc-sub-tab');
    if (tab) switchMode(tab.dataset.mode);
  });

  reexamToggle.addEventListener('change', function(e) {
    isReexam = e.target.value === 'reexam';
    updateFieldsForMode();
    updateBulkHint();
    resetOutputs();
  });

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    var batch = document.getElementById('batch').value;

    if (currentMode === 'bulk') {
      var text = bulkInput.value.trim();
      if (!text) return;
      var lines = text.split('\n').map(function(l) { return l.trim(); }).filter(function(l) { return l.length > 0; });
      if (!lines.length) return;
      
      runBulkCheck(lines, batch);
    } else {
      var symbol = document.getElementById('symbol').value.trim();
      var dob = dobInput.value.trim();

      if (!symbol) return;
      if (needsDob() && !dob) {
        dobInput.focus();
        return;
      }

      var errorDiv = document.getElementById('rc-error');
      var resultContainer = document.getElementById('rc-result-container');

      submitBtn.disabled = true;
      submitBtn.classList.add('loading');
      errorDiv.style.display = 'none';
      resultContainer.style.display = 'none';

      var csrf = document.querySelector('[name=csrfmiddlewaretoken]');
      var headers = { 'Content-Type': 'application/json' };
      if (csrf) headers['X-CSRFToken'] = csrf.value;

      fetch('/ajax/results/check/', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ exam: getExamCode(), symbol: symbol, dob: dob, batch: batch })
      })
      .then(function(r) { return r.json(); })
      .then(function(resp) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');

        if (!resp.success) {
          document.getElementById('rc-error-msg').textContent = resp.error || 'Failed to check result.';
          errorDiv.style.display = 'flex';
          return;
        }

        window.currentResultData = resp.data;
        showResult(resp.data, resp.cached);
      })
      .catch(function(err) {
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
        document.getElementById('rc-error-msg').textContent = 'Network error. Please try again later.';
        errorDiv.style.display = 'flex';
      });
    }
  });

  function showResult(data, cached) {
    var container = document.getElementById('rc-result-container');
    container.style.display = 'block';

    // No status badge shown in app

    var gpa = data.gpa || '·';
    document.getElementById('rc-gpa-num').textContent = gpa;
    document.getElementById('rc-grade').textContent = data.grade ? 'Grade: ' + data.grade : '·';

    var gpaCard = document.getElementById('rc-gpa-card');
    gpaCard.className = 'rc-gpa-card';
    if (gpa !== '·' && !isNaN(parseFloat(gpa))) {
      var score = parseFloat(gpa);
      if (score >= 3.2) {
        gpaCard.classList.add('gpa-high');
      } else if (score >= 2.0) {
        gpaCard.classList.add('gpa-mid');
      } else {
        gpaCard.classList.add('gpa-low');
      }
    }

    document.getElementById('rc-name').textContent = data.student_name || '·';
    document.getElementById('rc-exam').textContent = data.exam || '·';
    document.getElementById('rc-batch').textContent = data.batch || document.getElementById('batch').value;
    document.getElementById('rc-symbol').textContent = data.symbol || '·';
    document.getElementById('rc-school').textContent = data.school || '·';

    var tbody = document.getElementById('rc-subjects-body');
    tbody.innerHTML = '';
    
    if (data.subjects && data.subjects.length) {
      data.subjects.forEach(function(s) {
        var tr = document.createElement('tr');
        var gradeVal = s.grade || '';
        var clean = gradeVal.replace('+', 'plus');
        
        tr.innerHTML = 
          '<td>' +
            '<div class="subject-name">' + escapeHtml(s.name) + '</div>' +
            (s.code ? '<div class="subject-code">' + escapeHtml(s.code) + '</div>' : '') +
          '</td>' +
          '<td>' + escapeHtml(s.credit_hour || '·') + '</td>' +
          '<td><span class="grade-badge ' + clean + '">' + escapeHtml(gradeVal || '·') + '</span></td>' +
          '<td>' + escapeHtml(s.grade_point || '·') + '</td>';
          
        tbody.appendChild(tr);
      });
    } else {
      tbody.innerHTML = '<tr><td colspan="4" class="rc-none">No subjects listed.</td></tr>';
    }

    var link = document.getElementById('rc-official-link');
    if (data.source) {
      link.href = 'https://' + data.source + '/';
      link.textContent = data.source;
    } else {
      link.href = 'https://neb.ntc.net.np/';
      link.textContent = 'neb.ntc.net.np';
    }
  }

  function runBulkCheck(lines, batch) {
    var tbody = document.getElementById('rc-bulk-results-body');
    tbody.innerHTML = '';
    
    var container = document.getElementById('rc-bulk-results-container');
    container.style.display = 'block';
    
    var progressContainer = document.getElementById('rc-progress-container');
    var progressBar = document.getElementById('rc-progress-bar');
    var progressText = document.getElementById('rc-progress-text');
    var exportBtn = document.getElementById('rc-btn-export');

    progressContainer.style.display = 'block';
    progressText.style.display = 'block';
    progressBar.style.width = '0%';
    exportBtn.disabled = true;
    exportBtn.style.opacity = '0.5';

    var resultsData = [];
    var total = lines.length;
    var completed = 0;
    
    isCheckingBulk = true;
    bulkCancel = false;

    submitBtn.disabled = true;
    submitBtn.classList.add('loading');

    function checkNext(index) {
      if (index >= total || bulkCancel) {
        isCheckingBulk = false;
        submitBtn.disabled = false;
        submitBtn.classList.remove('loading');
        exportBtn.disabled = false;
        exportBtn.style.opacity = '1';
        progressText.textContent = bulkCancel ? 'Bulk check cancelled.' : 'Done. ' + completed + ' checked.';
        return;
      }

      var line = lines[index].trim();
      if (!line) {
        completed++;
        updateProgress();
        checkNext(index + 1);
        return;
      }

      var symbol = '';
      var dob = '';

      if (needsDob()) {
        var parts = line.split(',');
        symbol = parts[0].trim();
        if (parts[1]) dob = parts[1].trim();
      } else {
        symbol = line;
      }

      if (!symbol) {
        completed++;
        updateProgress();
        checkNext(index + 1);
        return;
      }

      // Add loading state row in bulk table
      var tr = document.createElement('tr');
      tr.id = 'bulk-row-' + index;
      tr.innerHTML = 
        '<td>' + escapeHtml(symbol) + '</td>' +
        '<td class="bulk-name" style="opacity: 0.5;">Checking...</td>' +
        '<td class="bulk-gpa">-</td>' +
        '<td class="bulk-grade">-</td>';
      tbody.appendChild(tr);

      var csrf = document.querySelector('[name=csrfmiddlewaretoken]');
      var headers = { 'Content-Type': 'application/json' };
      if (csrf) headers['X-CSRFToken'] = csrf.value;

      fetch('/ajax/results/check/', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ exam: getExamCode(), symbol: symbol, dob: dob, batch: batch })
      })
      .then(function(r) { return r.json(); })
      .then(function(resp) {
        completed++;
        updateProgress();
        
        var row = document.getElementById('bulk-row-' + index);
        if (!row) return;

        if (resp.success) {
          var d = resp.data;
          resultsData.push({
            symbol: symbol,
            name: d.student_name || '·',
            gpa: d.gpa || '·',
            grade: d.grade || '·',
            status: resp.cached ? 'Cached' : 'Fresh'
          });
          
          row.querySelector('.bulk-name').textContent = d.student_name || '·';
          row.querySelector('.bulk-name').style.opacity = '1';
          row.querySelector('.bulk-gpa').textContent = d.gpa || '·';
          row.querySelector('.bulk-gpa').classList.remove('is-failed');
          row.querySelector('.bulk-grade').textContent = d.grade || '·';
        } else {
          resultsData.push({
            symbol: symbol,
            name: '·',
            gpa: '·',
            grade: '·',
            status: resp.error || 'Failed'
          });
          row.querySelector('.bulk-name').textContent = '·';
          row.querySelector('.bulk-name').style.opacity = '1';
          row.querySelector('.bulk-gpa').textContent = resp.error || 'Failed';
          row.querySelector('.bulk-gpa').classList.add('is-failed');
          row.querySelector('.bulk-grade').textContent = '·';
        }

        var delay = resp.cached ? 0 : 500;
        setTimeout(function() {
          checkNext(index + 1);
        }, delay);
      })
      .catch(function(err) {
        completed++;
        updateProgress();
        resultsData.push({
          symbol: symbol,
          name: '·',
          gpa: '·',
          grade: '·',
          status: 'Error'
        });
        
        var row = document.getElementById('bulk-row-' + index);
        if (row) {
          row.querySelector('.bulk-name').textContent = '·';
          row.querySelector('.bulk-gpa').textContent = 'Error';
          row.querySelector('.bulk-gpa').classList.add('is-failed');
          row.querySelector('.bulk-grade').textContent = '·';
        }
        setTimeout(function() {
          checkNext(index + 1);
        }, 500);
      });
    }

    function updateProgress() {
      var pct = Math.round((completed / total) * 100);
      progressBar.style.width = pct + '%';
      progressText.textContent = completed + ' of ' + total;
    }

    checkNext(0);

    exportBtn.onclick = function() {
      var csv = 'Symbol Number,Student Name,GPA,Grade\n';
      resultsData.forEach(function(row) {
        csv += '"' + row.symbol.replace(/"/g, '""') + '",' +
               '"' + row.name.replace(/"/g, '""') + '",' +
               '"' + row.gpa.replace(/"/g, '""') + '",' +
               '"' + row.grade.replace(/"/g, '""') + '"\n';
      });
      var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      var link = document.createElement("a");
      var url = URL.createObjectURL(blob);
      link.setAttribute("href", url);
      link.setAttribute("download", "Result_Export_" + getExamCode() + "_" + batch + ".csv");
      link.style.visibility = 'hidden';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };
  }

  /* The two dialogs. Opening, closing, the backdrop, Escape, the focus trap
     and the scroll lock are NebUI's; the buttons below are all that is left. */
  var shareBtn = document.getElementById('rc-share-btn');
  var downloadCardBtn = document.getElementById('rc-download-card-btn');
  var previewImg = document.getElementById('rc-share-preview-img');
  var gradesheetBtn = document.getElementById('rc-gradesheet-btn');
  var printGradesheetBtn = document.getElementById('rc-print-gradesheet-btn');

  shareBtn.addEventListener('click', function() {
    if (window.currentResultData) {
      generateAndShowCard(window.currentResultData);
    }
  });

  gradesheetBtn.addEventListener('click', function() {
    if (window.currentResultData) {
      populateAndShowGradesheet(window.currentResultData);
    }
  });

  printGradesheetBtn.addEventListener('click', function() {
    window.print();
  });

  var saveImageBtn = document.getElementById('rc-save-image-btn');

  saveImageBtn.addEventListener('click', function() {
    var el = document.getElementById('rc-printable-gradesheet');
    if (!el) return;

    saveImageBtn.disabled = true;
    saveImageBtn.innerHTML = '<span class="material-symbols-outlined">hourglass_top</span> Rendering...';

    var oldTransform = el.style.transform;
    var oldTransformOrigin = el.style.transformOrigin;
    var oldMargin = el.style.margin;
    var wrapper = document.querySelector('.rc-gradesheet-paper-wrapper');
    var oldWrapperHeight = wrapper ? wrapper.style.height : '';
    var oldWrapperOverflowX = wrapper ? wrapper.style.overflowX : '';

    if (wrapper) {
      el.style.transform = 'none';
      el.style.transformOrigin = '';
      el.style.margin = '0';
      wrapper.style.height = '';
      wrapper.style.overflowX = 'auto';
    }

    void el.offsetWidth;

    html2canvas(el, {
      scale: 2,
      backgroundColor: '#ffffff',
      useCORS: true,
      logging: false,
      width: el.scrollWidth,
      height: el.scrollHeight
    }).then(function(canvas) {
      var link = document.createElement('a');
      var name = document.getElementById('gs-student-name').textContent;
      if (!name || name === '·') name = 'Gradesheet';
      link.download = 'NEBians_Gradesheet_' + name.replace(/\s+/g, '_') + '.jpg';
      link.href = canvas.toDataURL('image/jpeg', 0.88);
      link.click();

      if (wrapper) {
        el.style.transform = oldTransform;
        el.style.transformOrigin = oldTransformOrigin;
        el.style.margin = oldMargin;
        wrapper.style.height = oldWrapperHeight;
        wrapper.style.overflowX = oldWrapperOverflowX;
      }

      saveImageBtn.disabled = false;
      saveImageBtn.innerHTML = '<span class="material-symbols-outlined">photo_camera</span> Save as Image';
    }).catch(function(err) {
      console.error('html2canvas error:', err);
      if (wrapper) {
        el.style.transform = oldTransform;
        el.style.transformOrigin = oldTransformOrigin;
        el.style.margin = oldMargin;
        wrapper.style.height = oldWrapperHeight;
        wrapper.style.overflowX = oldWrapperOverflowX;
      }
      saveImageBtn.disabled = false;
      saveImageBtn.innerHTML = '<span class="material-symbols-outlined">photo_camera</span> Save as Image';
    });
  });

  function populateAndShowGradesheet(data) {
    var isSee = currentExam === 'see';
    
    var officeName = document.getElementById('gs-office-name');
    var examTypeDesc = document.getElementById('gs-exam-type-desc');
    
    if (isSee) {
      officeName.textContent = 'UNOFFICIAL SEE RESULT' + (isReexam ? ' (SUPPLEMENTARY)' : '');
      examTypeDesc.textContent = 'SECONDARY EDUCATION EXAMINATION (GRADE X)' + (isReexam ? ': SUPPLEMENTARY' : '');
      document.getElementById('gs-th-credit-hour').style.display = 'none';
    } else {
      officeName.textContent = 'UNOFFICIAL CLASS 12 RESULT' + (isReexam ? ' (RE-EXAM)' : '');
      examTypeDesc.textContent = 'SCHOOL LEAVING CERTIFICATE EXAMINATION (GRADE XII)' + (isReexam ? ': RE-EXAM' : '');
      document.getElementById('gs-th-credit-hour').style.display = '';
    }

    // Populate student metadata
    document.getElementById('gs-student-name').textContent = (data.student_name || '·').toUpperCase();
    document.getElementById('gs-student-symbol').textContent = data.symbol || '·';
    document.getElementById('gs-student-school').textContent = (data.school || '·').toUpperCase();
    
    var regNo = data.registration_no;
    if (!regNo) {
      var symbolInt = parseInt(data.symbol) || 12345678;
      var seedPart1 = (symbolInt % 90 + 10);
      var seedPart2 = (symbolInt % 900000 + 100000);
      var seedPart3 = (symbolInt % 90 + 10);
      regNo = seedPart1 + '-' + seedPart2 + '-' + seedPart3;
    }
    document.getElementById('gs-student-reg').textContent = regNo;

    var dobVal = dobInput.value.trim();
    if (!dobVal && data.dob) {
      dobVal = data.dob;
    }
    document.getElementById('gs-student-dob').textContent = dobVal || '·';
    
    var batchVal = data.batch || document.getElementById('batch').value;
    document.getElementById('gs-student-batch').textContent = batchVal + ' BS';
    document.getElementById('gs-exam-year').textContent = batchVal;
    document.getElementById('gs-issue-date').textContent = batchVal + '/04/15 BS';

    // Populate overall GPA and final grade
    document.getElementById('gs-final-gpa').textContent = data.gpa || '·';
    document.getElementById('gs-final-grade').textContent = data.grade || '·';

    // Populate subject rows
    var tbody = document.getElementById('gs-grades-body');
    tbody.innerHTML = '';

    if (data.subjects && data.subjects.length) {
      data.subjects.forEach(function(s, index) {
        var tr = document.createElement('tr');
        
        var tdSn = document.createElement('td');
        tdSn.textContent = index + 1;
        tr.appendChild(tdSn);

        var tdCode = document.createElement('td');
        tdCode.textContent = s.code || '·';
        tr.appendChild(tdCode);

        var tdName = document.createElement('td');
        tdName.textContent = s.name || '·';
        tr.appendChild(tdName);

        var tdCredit = document.createElement('td');
        tdCredit.textContent = s.credit_hour || '·';
        if (isSee) {
          tdCredit.style.display = 'none';
        } else {
          tdCredit.style.display = '';
        }
        tr.appendChild(tdCredit);

        var tdGrade = document.createElement('td');
        tdGrade.textContent = s.grade || '·';
        tdGrade.style.fontWeight = '700';
        tr.appendChild(tdGrade);

        var tdGp = document.createElement('td');
        tdGp.textContent = s.grade_point || '·';
        tr.appendChild(tdGp);

        tbody.appendChild(tr);
      });
    } else {
      var tr = document.createElement('tr');
      var colspan = isSee ? 5 : 6;
      tr.innerHTML = '<td colspan="' + colspan + '" style="text-align:center;padding:24px;color:#78716c">No subject-wise details available.</td>';
      tbody.appendChild(tr);
    }

    NebUI.open('rc-gradesheet-modal');
    setTimeout(scaleGradesheet, 50);
  }

  function generateAndShowCard(data) {
    var canvas = document.getElementById('rc-share-canvas');
    var ctx = canvas.getContext('2d');
    
    var svg = document.querySelector('.topbar-logo');
    if (!svg) {
      drawCardWithLogoImage(null, data, canvas, ctx);
      return;
    }
    
    var svgString = new XMLSerializer().serializeToString(svg);
    var svgBlob = new Blob([svgString], {type: 'image/svg+xml;charset=utf-8'});
    var URL = window.URL || window.webkitURL || window;
    var blobURL = URL.createObjectURL(svgBlob);
    
    var image = new Image();
    image.onload = function() {
      drawCardWithLogoImage(image, data, canvas, ctx);
      URL.revokeObjectURL(blobURL);
    };
    image.onerror = function() {
      drawCardWithLogoImage(null, data, canvas, ctx);
      URL.revokeObjectURL(blobURL);
    };
    image.src = blobURL;
  }

  function drawCardWithLogoImage(logoImg, data, canvas, ctx) {
    ctx.clearRect(0, 0, 1080, 1080);

    ctx.fillStyle = '#f6f8ff';
    ctx.fillRect(0, 0, 1080, 1080);

    ctx.fillStyle = '#ffffff';
    ctx.strokeStyle = '#c6d0ea';
    ctx.lineWidth = 2;
    drawRoundedRect(ctx, 40, 40, 1000, 1000, 44);
    ctx.fill();
    ctx.stroke();

    if (logoImg) {
      ctx.drawImage(logoImg, 492, 100, 96, 96);
    } else {
      ctx.save();
      ctx.beginPath();
      ctx.arc(540, 148, 48, 0, Math.PI * 2);
      ctx.fillStyle = '#0058df';
      ctx.fill();
      ctx.restore();
    }

    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 22px "Poppins", sans-serif';
    ctx.textAlign = 'center';
    ctx.letterSpacing = '3px';
    ctx.fillText('NEBIANS', 540, 230);

    ctx.fillStyle = '#64748b';
    ctx.font = '500 13px "Poppins", sans-serif';
    ctx.letterSpacing = '0px';
    ctx.fillText('nebians.consica.com.np', 540, 252);

    ctx.fillStyle = '#0f172a';
    ctx.font = 'bold 44px "Poppins", sans-serif';
    ctx.letterSpacing = '0px';
    ctx.fillText((data.student_name || 'STUDENT RESULT').toUpperCase(), 540, 355);

    ctx.save();
    ctx.fillStyle = '#e9eefb';
    drawRoundedRect(ctx, 100, 420, 880, 360, 32);
    ctx.fill();
    ctx.restore();

    var labels = ['Symbol Number', 'Exam / Batch', 'School / College'];
    var values = [
      data.symbol || '·',
      (data.exam || '12') + '  •  ' + (data.batch || document.getElementById('batch').value) + ' BS',
      data.school || '·'
    ];
    
    ctx.textAlign = 'left';
    for (var i = 0; i < labels.length; i++) {
      var yOffset = 485 + i * 95;
      
      ctx.fillStyle = '#64748b';
      ctx.font = 'bold 12px "Poppins", sans-serif';
      ctx.letterSpacing = '1.5px';
      ctx.fillText(labels[i].toUpperCase(), 150, yOffset);
      
      ctx.fillStyle = '#0f172a';
      ctx.font = '600 20px "Poppins", sans-serif';
      ctx.letterSpacing = '0px';
      
      var val = values[i];
      if (i === 2 && val.length > 38) {
        ctx.font = '600 16px "Poppins", sans-serif';
      }
      ctx.fillText(val, 150, yOffset + 28);
    }

    var gpa = parseFloat(data.gpa) || 0.0;
    var gpaColor = gpa < 2.0 ? '#ba1a1a' : '#0058df';
    var gradeLabel = data.grade || 'A+';

    var cx = 760;
    var cy = 600;

    ctx.fillStyle = gpaColor;
    drawRoundedRect(ctx, cx - 112, cy - 112, 224, 224, 72);
    ctx.fill();

    ctx.textAlign = 'center';
    ctx.fillStyle = '#dbe4ff';
    ctx.font = 'bold 13px "Poppins", sans-serif';
    ctx.letterSpacing = '1.5px';
    ctx.fillText('GPA', cx, cy - 52);

    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 60px "Poppins", sans-serif';
    ctx.letterSpacing = '0px';
    ctx.fillText(data.gpa || '·', cx, cy + 10);

    ctx.fillStyle = '#dbe4ff';
    drawRoundedRect(ctx, cx - 42, cy + 34, 84, 30, 15);
    ctx.fill();
    ctx.fillStyle = '#001a52';
    ctx.font = 'bold 14px "Poppins", sans-serif';
    ctx.fillText(gradeLabel, cx, cy + 55);

    ctx.textAlign = 'center';
    ctx.fillStyle = '#64748b';
    ctx.font = '500 13px "Poppins", sans-serif';
    ctx.fillText('Verify result online at nebians.consica.com.np/app/results/check  •  NEBians Study Community', 540, 920);

    var imgUrl = canvas.toDataURL('image/png');
    previewImg.src = imgUrl;

    NebUI.open('rc-share-modal');

    downloadCardBtn.onclick = function() {
      var link = document.createElement('a');
      link.download = 'NEBians_Result_' + (data.student_name || 'Student').replace(/\s+/g, '_') + '.png';
      link.href = imgUrl;
      link.click();
    };
  }

  function drawRoundedRect(ctx, x, y, width, height, radius) {
    ctx.beginPath();
    ctx.moveTo(x + radius, y);
    ctx.lineTo(x + width - radius, y);
    ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
    ctx.lineTo(x + width, y + height - radius);
    ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
    ctx.lineTo(x + radius, y + height);
    ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
    ctx.lineTo(x, y + radius);
    ctx.quadraticCurveTo(x, y, x + radius, y);
    ctx.closePath();
  }

  function scaleGradesheet() {
    var wrapper = document.querySelector('.rc-gradesheet-paper-wrapper');
    var paper = document.getElementById('rc-printable-gradesheet');
    if (!wrapper || !paper) return;
    
    paper.style.transform = '';
    paper.style.transformOrigin = '';
    wrapper.style.height = '';
    
    var wrapperWidth = wrapper.getBoundingClientRect().width;
    var style = window.getComputedStyle(wrapper);
    var paddingLeft = parseFloat(style.paddingLeft) || 20;
    var paddingRight = parseFloat(style.paddingRight) || 20;
    var padding = paddingLeft + paddingRight;
    
    var availableWidth = wrapperWidth - padding;
    var paperWidth = paper.offsetWidth || 794;
    var paperHeight = paper.offsetHeight || 1123;
    
    if (availableWidth < paperWidth) {
      var scale = availableWidth / paperWidth;
      paper.style.transform = 'scale(' + scale + ')';
      paper.style.transformOrigin = 'top center';
      wrapper.style.height = (paperHeight * scale + padding) + 'px';
      wrapper.style.overflowX = 'hidden';
    } else {
      wrapper.style.overflowX = 'auto';
    }
  }

  window.addEventListener('resize', scaleGradesheet);

  function escapeHtml(str) {
    if (!str) return '';
    var d = document.createElement('div');
    d.textContent = str;
    return d.innerHTML;
  }
})();
