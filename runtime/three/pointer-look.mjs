const clamp = value => Math.max(-1, Math.min(1, value));

export function samplePointerLook(x, y) {
  if (![x, y].every(Number.isFinite)) throw new TypeError('Fare konumu sonlu sayılar olmalı.');
  return { yaw: clamp(x) * 7 * Math.PI / 180, height: -clamp(y) * 0.18 };
}

export function observePointerLook({ element, onChange, window: view = globalThis.window }) {
  if (!element?.getBoundingClientRect || !element?.addEventListener || typeof onChange !== 'function') {
    throw new TypeError('Bakış hareketi için bir yüzey ve değişim callback’i gerekiyor.');
  }
  const finePointer = view.matchMedia('(hover: hover) and (pointer: fine)');
  const reducedMotion = view.matchMedia('(prefers-reduced-motion: reduce)');
  const document = view.document;
  let currentX = 0;
  let currentY = 0;
  let targetX = 0;
  let targetY = 0;
  let request = null;
  let previousTime = null;
  let disposed = false;

  function enabled() {
    return finePointer.matches && !reducedMotion.matches && !document.hidden;
  }

  function step(time) {
    request = null;
    if (disposed || document.hidden) return;
    const elapsed = previousTime === null ? 16 : Math.max(0, Math.min(64, time - previousTime));
    previousTime = time;
    const blend = 1 - Math.exp(-elapsed / 75);
    currentX += (targetX - currentX) * blend;
    currentY += (targetY - currentY) * blend;
    if (Math.abs(targetX - currentX) < 0.001) currentX = targetX;
    if (Math.abs(targetY - currentY) < 0.001) currentY = targetY;
    onChange(currentX, currentY);
    if (currentX !== targetX || currentY !== targetY) schedule();
    else previousTime = null;
  }

  function schedule() {
    if (request === null && !disposed && !document.hidden) request = view.requestAnimationFrame(step);
  }

  function reset() {
    targetX = 0;
    targetY = 0;
    if (document.hidden) {
      if (request !== null) view.cancelAnimationFrame(request);
      request = null;
      previousTime = null;
      currentX = 0;
      currentY = 0;
      onChange(0, 0);
    } else schedule();
  }

  function move(event) {
    if (!enabled()) return;
    const bounds = element.getBoundingClientRect();
    if (bounds.width <= 0 || bounds.height <= 0) return;
    targetX = clamp((event.clientX - bounds.left) * 2 / bounds.width - 1);
    targetY = clamp((event.clientY - bounds.top) * 2 / bounds.height - 1);
    schedule();
  }

  function policyChanged() {
    if (!enabled()) reset();
  }

  element.addEventListener('pointermove', move, { passive: true });
  element.addEventListener('pointerleave', reset);
  finePointer.addEventListener('change', policyChanged);
  reducedMotion.addEventListener('change', policyChanged);
  document.addEventListener('visibilitychange', policyChanged);
  return {
    destroy() {
      if (disposed) return;
      disposed = true;
      if (request !== null) view.cancelAnimationFrame(request);
      element.removeEventListener('pointermove', move);
      element.removeEventListener('pointerleave', reset);
      finePointer.removeEventListener('change', policyChanged);
      reducedMotion.removeEventListener('change', policyChanged);
      document.removeEventListener('visibilitychange', policyChanged);
    },
  };
}
