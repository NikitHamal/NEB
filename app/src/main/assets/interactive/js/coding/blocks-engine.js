export const BLOCK_DEFS = {
  'move-forward': { label: 'Move forward', icon: 'arrow_upward', cls: 'bx-kind-move' },
  'turn-left': { label: 'Turn left', icon: 'rotate_left', cls: 'bx-kind-turn' },
  'turn-right': { label: 'Turn right', icon: 'rotate_right', cls: 'bx-kind-turn' },
  'repeat': { label: 'Repeat', icon: 'repeat', cls: 'bx-kind-repeat', container: true, hasCount: true },
  'if-path': { label: 'If path ahead', icon: 'alt_route', cls: 'bx-kind-if', container: true },
};

let idSeq = 1;

function makeNode(type) {
  const def = BLOCK_DEFS[type];
  const node = { id: 'b' + (idSeq++), type };
  if (def.hasCount) node.count = 3;
  if (def.container) node.children = [];
  return node;
}

export function countBlocks(list) {
  let n = 0;
  for (const node of list) {
    n += 1;
    if (node.children) n += countBlocks(node.children);
  }
  return n;
}

const delay = (ms) => new Promise((r) => setTimeout(r, ms));

export async function executeProgram(program, world, opts = {}) {
  const gate = opts.gate || (() => delay(opts.stepDelay || 380));
  const onBlock = opts.onBlock || (() => {});
  const ctl = opts.control || { stopped: false };
  let steps = 0;

  async function runList(list) {
    for (const node of list) {
      if (ctl.stopped) return false;
      if (++steps > 600) throw new Error('step-limit');
      if (node.type === 'repeat') {
        onBlock(node);
        for (let i = 0; i < (node.count || 1); i++) {
          if (!(await runList(node.children))) return false;
          if (ctl.stopped) return false;
        }
      } else if (node.type === 'if-path') {
        onBlock(node);
        await gate(node);
        if (ctl.stopped) return false;
        if (world.isPathAhead()) {
          if (!(await runList(node.children))) return false;
        }
      } else {
        onBlock(node);
        await gate(node);
        if (ctl.stopped) return false;
        if (node.type === 'move-forward') {
          if (!(await world.moveForward())) return false;
        } else if (node.type === 'turn-left') {
          await world.turnLeft();
        } else if (node.type === 'turn-right') {
          await world.turnRight();
        }
      }
    }
    return true;
  }

  return runList(program);
}

export function createBlocksEngine(host, opts = {}) {
  const paletteTypes = opts.palette || ['move-forward', 'turn-left', 'turn-right'];
  let program = [];
  let locked = false;
  const nodeEls = new Map();
  const onChange = opts.onChange || (() => {});

  const root = document.createElement('div');
  root.className = 'bx-workspace';
  root.innerHTML =
    '<div class="bx-palette-wrap"><div class="bx-panel-label">Blocks <span class="bx-hint-label">tap or drag</span></div><div class="bx-palette"></div></div>' +
    '<div class="bx-tray-wrap"><div class="bx-panel-label">Program <span class="bx-count"></span></div><div class="bx-tray-list" data-bx-drop="1"></div></div>';
  host.appendChild(root);

  const paletteEl = root.querySelector('.bx-palette');
  const trayList = root.querySelector('.bx-tray-list');
  const countEl = root.querySelector('.bx-count');
  const indicator = document.createElement('div');
  indicator.className = 'bx-drop-indicator';

  function buildBlockEl(node, inTray) {
    const def = BLOCK_DEFS[node.type];
    const el = document.createElement('div');
    el.className = 'bx-block ' + def.cls + (def.container ? ' bx-container' : '');
    const head = document.createElement('div');
    head.className = 'bx-block-head';
    head.innerHTML =
      '<span class="material-symbols-outlined bx-block-icon">' + def.icon + '</span>' +
      '<span class="bx-block-label">' + def.label + '</span>';
    el.appendChild(head);
    if (def.hasCount && inTray) {
      const ctr = document.createElement('span');
      ctr.className = 'bx-counter';
      ctr.innerHTML =
        '<button type="button" class="bx-counter-btn" data-d="-1" aria-label="Less">−</button>' +
        '<span class="bx-counter-val">' + node.count + '</span>' +
        '<button type="button" class="bx-counter-btn" data-d="1" aria-label="More">+</button>';
      ctr.querySelectorAll('.bx-counter-btn').forEach((b) => {
        b.addEventListener('pointerdown', (e) => e.stopPropagation());
        b.addEventListener('click', (e) => {
          e.stopPropagation();
          if (locked) return;
          node.count = Math.min(9, Math.max(2, node.count + parseInt(b.dataset.d, 10)));
          ctr.querySelector('.bx-counter-val').textContent = node.count;
          onChange();
        });
      });
      head.appendChild(ctr);
    } else if (def.hasCount) {
      const v = document.createElement('span');
      v.className = 'bx-counter-val bx-counter-static';
      v.textContent = node.count;
      head.appendChild(v);
    }
    if (inTray) {
      const rm = document.createElement('button');
      rm.type = 'button';
      rm.className = 'bx-remove';
      rm.setAttribute('aria-label', 'Remove block');
      rm.innerHTML = '<span class="material-symbols-outlined">close</span>';
      rm.addEventListener('pointerdown', (e) => e.stopPropagation());
      rm.addEventListener('click', (e) => {
        e.stopPropagation();
        if (locked) return;
        removeNode(node);
        render();
        onChange();
      });
      head.appendChild(rm);
    }
    if (def.container && inTray) {
      const slot = document.createElement('div');
      slot.className = 'bx-slot-list';
      slot.dataset.bxDrop = '1';
      slot.dataset.bxNode = node.id;
      node.children.forEach((child) => slot.appendChild(buildBlockEl(child, true)));
      if (!node.children.length) {
        const ph = document.createElement('div');
        ph.className = 'bx-slot-empty';
        ph.textContent = 'drop blocks here';
        slot.appendChild(ph);
      }
      el.appendChild(slot);
    }
    el.dataset.bxId = node.id;
    if (inTray) {
      nodeEls.set(node.id, el);
      attachTrayDrag(head, node);
    }
    return el;
  }

  function findList(listId) {
    if (!listId) return program;
    const walk = (list) => {
      for (const n of list) {
        if (n.id === listId) return n.children;
        if (n.children) {
          const f = walk(n.children);
          if (f) return f;
        }
      }
      return null;
    };
    return walk(program) || program;
  }

  function removeNode(target) {
    const walk = (list) => {
      const i = list.indexOf(target);
      if (i >= 0) { list.splice(i, 1); return true; }
      return list.some((n) => n.children && walk(n.children));
    };
    walk(program);
  }

  function render() {
    nodeEls.clear();
    trayList.innerHTML = '';
    program.forEach((node) => trayList.appendChild(buildBlockEl(node, true)));
    if (!program.length) {
      const ph = document.createElement('div');
      ph.className = 'bx-tray-empty';
      ph.innerHTML = '<span class="material-symbols-outlined">touch_app</span>Tap a block to add it, or drag it here';
      trayList.appendChild(ph);
    }
    countEl.textContent = countBlocks(program) + ' block' + (countBlocks(program) === 1 ? '' : 's');
  }

  let drag = null;

  function startDrag(node, e, sourceEl, width) {
    const ghost = sourceEl.cloneNode(true);
    ghost.classList.add('bx-ghost');
    ghost.style.width = (width || sourceEl.offsetWidth || 160) + 'px';
    document.body.appendChild(ghost);
    drag = { node, ghost, target: null, index: 0 };
    document.body.classList.add('bx-dragging');
    moveDrag(e);
  }

  function dropTargets() {
    return [trayList, ...trayList.querySelectorAll('.bx-slot-list')];
  }

  function moveDrag(e) {
    drag.ghost.style.left = e.clientX + 'px';
    drag.ghost.style.top = e.clientY + 'px';
    let target = null;
    const els = document.elementsFromPoint(e.clientX, e.clientY);
    for (const el of els) {
      if (el.dataset && el.dataset.bxDrop) { target = el; break; }
      if (el === trayList.parentElement) { target = trayList; break; }
    }
    dropTargets().forEach((t) => t.classList.toggle('bx-drop-active', t === target));
    if (!target) {
      indicator.remove();
      drag.target = null;
      return;
    }
    const kids = [...target.children].filter((c) => c.classList.contains('bx-block'));
    let index = kids.length;
    for (let i = 0; i < kids.length; i++) {
      const r = kids[i].getBoundingClientRect();
      if (e.clientY < r.top + r.height / 2) { index = i; break; }
    }
    drag.target = target;
    drag.index = index;
    if (index >= kids.length) target.appendChild(indicator);
    else target.insertBefore(indicator, kids[index]);
  }

  function endDrag() {
    if (!drag) return;
    drag.ghost.remove();
    indicator.remove();
    document.body.classList.remove('bx-dragging');
    dropTargets().forEach((t) => t.classList.remove('bx-drop-active'));
    if (drag.target) {
      const listId = drag.target.dataset.bxNode || null;
      const list = findList(listId);
      list.splice(Math.min(drag.index, list.length), 0, drag.node);
    }
    drag = null;
    render();
    onChange();
  }

  let activeDetach = null;

  function attachPointer(el, node, opts2) {
    el.addEventListener('pointerdown', (e) => {
      if (locked || e.button > 0) return;
      const startX = e.clientX;
      const startY = e.clientY;
      const pid = e.pointerId;
      let started = false;
      const ghostSrc = opts2.ghostSource();
      const ghostWidth = ghostSrc.offsetWidth;
      const onMove = (ev) => {
        if (ev.pointerId !== pid) return;
        if (!started && Math.hypot(ev.clientX - startX, ev.clientY - startY) > 8) {
          started = true;
          if (ev.cancelable) ev.preventDefault();
          const dragNode = opts2.getNode();
          if (opts2.removeOnDrag) {
            removeNode(dragNode);
            render();
          } else {
            try { el.setPointerCapture(pid); } catch (err) {}
          }
          startDrag(dragNode, ev, ghostSrc, ghostWidth);
        } else if (started) {
          moveDrag(ev);
        }
      };
      const onUp = (ev) => {
        if (ev.pointerId !== pid) return;
        detach();
        if (started) endDrag();
        else if (ev.type === 'pointerup' && opts2.onTap) opts2.onTap();
      };
      const detach = () => {
        window.removeEventListener('pointermove', onMove);
        window.removeEventListener('pointerup', onUp);
        window.removeEventListener('pointercancel', onUp);
        if (activeDetach === detach) activeDetach = null;
      };
      activeDetach = detach;
      window.addEventListener('pointermove', onMove);
      window.addEventListener('pointerup', onUp);
      window.addEventListener('pointercancel', onUp);
    });
  }

  function attachTrayDrag(headEl, node) {
    attachPointer(headEl, node, {
      getNode: () => node,
      removeOnDrag: true,
      ghostSource: () => headEl.parentElement,
      onTap: null,
    });
  }

  paletteTypes.forEach((type) => {
    const sample = makeNode(type);
    const el = buildBlockEl(sample, false);
    el.classList.add('bx-palette-block');
    paletteEl.appendChild(el);
    attachPointer(el, null, {
      getNode: () => makeNode(type),
      removeOnDrag: false,
      ghostSource: () => el,
      onTap: () => {
        const node = makeNode(type);
        program.push(node);
        render();
        onChange();
        const added = nodeEls.get(node.id);
        if (added) {
          added.classList.add('bx-pop-in');
          added.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
        }
      },
    });
  });

  render();

  return {
    el: root,
    getProgram: () => program,
    blockCount: () => countBlocks(program),
    clear() { program = []; render(); onChange(); },
    setLocked(v) { locked = v; root.classList.toggle('bx-locked', v); },
    highlight(node) {
      nodeEls.forEach((el) => el.classList.remove('bx-active'));
      const el = nodeEls.get(node && node.id);
      if (el) {
        el.classList.add('bx-active');
        el.scrollIntoView({ block: 'nearest', behavior: 'smooth' });
      }
    },
    clearHighlight() { nodeEls.forEach((el) => el.classList.remove('bx-active')); },
    dispose() {
      if (activeDetach) activeDetach();
      if (drag) {
        drag.ghost.remove();
        drag = null;
      }
      document.body.classList.remove('bx-dragging');
      root.remove();
      indicator.remove();
    },
  };
}
