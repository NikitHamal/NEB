import { seg } from '../engine/tl.js';
import { outExpo, inOutCubic, spring } from '../engine/ease.js';
import { place, icon } from '../engine/dom.js';
import { fitSize, graphemes, textWidth } from '../engine/text.js';
import { buildLogo } from '../engine/logo.js';
import { makeHills } from '../engine/hills.js';
import { drawBurst } from '../engine/burst.js';

export default {
  pre: 0.6,
  build(S, cfg, entry, root) {
    const { W, H } = S;
    const brand = S.spec.brand;
    const diag = Math.hypot(W, H);
    const wipe = S.mk('div', { style: { position: 'absolute', left: 0, top: 0, width: '100px', height: '100px', marginLeft: '-50px', marginTop: '-50px', borderRadius: '50%', background: S.c('blue') } });
    const hills = makeHills(S);
    const hillHost = S.mk('div', { class: 'fill' }, [hills.node]);

    const tileSize = S.portrait ? 150 : 190;
    const logo = buildLogo(S, S.assets.logoSvg, tileSize * 0.68);
    const logoBox = S.mk('div', { style: { position: 'absolute', left: `${(tileSize - logo.width) / 2}px`, top: `${tileSize * 0.16}px`, width: `${logo.width}px`, height: `${logo.height}px` } }, [logo.svg]);
    const tile = S.mk('div', { style: { position: 'absolute', left: 0, top: 0, width: `${tileSize}px`, height: `${tileSize}px`, borderRadius: `${tileSize * 0.26}px`, background: '#fff', boxShadow: '0 30px 70px rgba(0,20,80,.45)' } }, [logoBox]);
    const wordSize = tileSize * 0.78;
    const wordW = textWidth(brand.name, { weight: 800, size: wordSize, ls: -0.045 });
    const word = S.mk('div', { style: { position: 'absolute', left: 0, top: 0, height: `${wordSize * 1.3}px`, overflow: 'hidden', display: 'flex', alignItems: 'center', fontWeight: 800, letterSpacing: '-0.045em', fontSize: `${wordSize}px`, color: '#fff', whiteSpace: 'nowrap' } }, [S.mk('span', { text: brand.name, style: { display: 'inline-block', paddingRight: '0.05em' } })]);

    const liveSize = fitSize(cfg.live, { weight: 900, ls: -0.05, target: W * (S.portrait ? 0.86 : 0.5), max: S.portrait ? 200 : 250 });
    const liveLetters = graphemes(cfg.live).map((ch) => S.mk('span', { text: ch, style: { display: 'inline-block', whiteSpace: 'pre', paddingRight: ch === ' ' ? '0.16em' : '0' } }));
    const live = S.mk('div', { style: { position: 'absolute', left: 0, top: 0, display: 'flex', overflow: 'hidden', padding: '0.14em 0.1em 0.24em', margin: '-0.14em -0.1em -0.24em', fontWeight: 900, letterSpacing: '-0.05em', lineHeight: 1, fontSize: `${liveSize}px`, color: '#fff', whiteSpace: 'nowrap' } }, liveLetters);

    const pillSize = S.portrait ? 34 : 46;
    const pill = S.mk('div', { style: { position: 'absolute', left: 0, top: 0, display: 'flex', alignItems: 'center', gap: `${pillSize * 0.4}px`, padding: `${pillSize * 0.5}px ${pillSize * 0.95}px`, borderRadius: '999px', background: '#fff', color: S.c('blue'), fontWeight: 700, fontSize: `${pillSize}px`, letterSpacing: '-0.01em', whiteSpace: 'nowrap', boxShadow: '0 24px 60px rgba(0,20,80,.4)' } }, [S.mk('span', { text: brand.url }), icon('north_east', { style: { fontSize: `${pillSize * 1.1}px` } })]);
    const sub = S.mk('div', { text: brand.subline, style: { position: 'absolute', left: 0, top: 0, color: 'rgba(255,255,255,.9)', fontWeight: 500, fontSize: `${S.portrait ? 26 : 34}px`, whiteSpace: 'nowrap' } });
    const sparks = S.mk('canvas', { class: 'fill', width: W, height: H });
    const ctx = sparks.getContext('2d');
    const shade = S.mk('div', { class: 'fill', style: { background: 'linear-gradient(180deg, rgba(2,27,84,0) 55%, rgba(2,27,84,0.5) 100%)' } });
    root.append(hillHost, shade, wipe, sparks, tile, word, live, pill, sub);

    const liveBox = live.getBoundingClientRect();
    const pillBox = pill.getBoundingClientRect();
    const subBox = sub.getBoundingClientRect();
    const rowW = tileSize + tileSize * 0.28 + wordW;
    const rowX = (W - rowW) / 2;
    const rowY = S.portrait ? H * 0.2 : H * 0.15;
    const liveY = rowY + tileSize + (S.portrait ? 90 : 84);
    const pillY = S.portrait ? H * 0.66 : H * 0.735;
    const subY = pillY + pillBox.height + (S.portrait ? 34 : 30);

    return {
      update(lt, t) {
        const grow = inOutCubic(seg(lt, -0.55, 0.55));
        const fade = seg(lt, 0.02, 0.4, inOutCubic);
        place(wipe, { x: W / 2, y: H / 2, s: (diag * 1.35 * grow) / 100 + 0.02, o: 1 - fade });

        hills.layers.forEach((L, i) => {
          const e = outExpo(seg(lt, i * 0.09, 0.9));
          const drift = Math.sin(t * 0.4 + i) * 6;
          L.g.style.transform = `translate(${drift}px,${(1 - e) * hills.height * 0.6}px)`;
        });

        const tE = spring(0.5, 14)(seg(lt, 0.06, 0.7));
        place(tile, { x: rowX, y: rowY, s: 0.3 + 0.7 * tE, rz: (1 - tE) * -14, o: Math.min(1, tE * 3) });
        const wE = outExpo(seg(lt, 0.22, 0.55));
        word.style.width = `${wordW * 1.05 * wE}px`;
        place(word, { x: rowX + tileSize + tileSize * 0.28, y: rowY + tileSize / 2 - (wordSize * 1.3) / 2 });
        word.firstChild.style.transform = `translateX(${-(1 - wE) * 50}px)`;

        liveLetters.forEach((el, k) => {
          const e = outExpo(seg(lt, 0.46 + k * 0.03, 0.4));
          place(el, { y: (1 - e) * liveSize * 1.55, rz: (1 - e) * 7 });
        });
        place(live, { x: (W - liveBox.width) / 2, y: liveY });

        const pE = outExpo(seg(lt, 0.85, 0.5));
        place(pill, { x: (W - pillBox.width) / 2, y: pillY + (1 - pE) * 60, o: pE, s: 0.94 + 0.06 * pE });
        const sE = outExpo(seg(lt, 1.05, 0.5));
        place(sub, { x: (W - subBox.width) / 2, y: subY + (1 - sE) * 24, o: sE });

        ctx.clearRect(0, 0, W, H);
        drawBurst(ctx, lt, {
          t0: 0.5, x: W / 2, y: liveY + liveSize * 0.5, n: 70, speed: 1300, life: 1.3, size: 22, gravity: 700, drag: 2.6, seed: 31,
          colors: ['#ffffff', S.c('gold'), S.c('pink'), S.c('skyDeep'), S.c('mint')],
        });
      },
    };
  },
};
