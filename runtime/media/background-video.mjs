export function createBackgroundVideo({ video, src, poster, onState = () => {}, window: view = globalThis.window }) {
  if (!video?.play || !video?.pause || !src || !poster) throw new TypeError('Video öğesi, video adresi ve poster gerekiyor.');
  const document = view.document;
  const reduced = view.matchMedia('(prefers-reduced-motion: reduce)');
  const connection = view.navigator.connection;
  let visible = false;
  let paused = false;
  let failed = false;
  let destroyed = false;
  let generation = 0;
  video.muted = true;
  video.loop = true;
  video.playsInline = true;
  video.preload = 'none';
  video.poster = poster;

  function setState(state) {
    video.dataset.state = state;
    onState(state);
  }

  async function refresh() {
    const revision = ++generation;
    if (destroyed) return;
    if (reduced.matches || connection?.saveData || paused || failed) {
      video.pause();
      if (video.hasAttribute('src')) {
        video.removeAttribute('src');
        video.load();
      }
      setState(failed ? 'error' : 'poster');
      return;
    }
    if (!visible || document.hidden) {
      video.pause();
      setState('idle');
      return;
    }
    if (!video.hasAttribute('src')) video.src = src;
    setState('loading');
    try {
      await video.play();
      if (!destroyed && revision === generation) setState('playing');
    } catch {
      if (!destroyed && revision === generation) {
        failed = true;
        void refresh();
      }
    }
  }

  const observer = new view.IntersectionObserver(entries => {
    visible = entries.some(entry => entry.isIntersecting);
    void refresh();
  });
  observer.observe(video);
  const refreshListener = () => { void refresh(); };
  const errorListener = () => { failed = true; void refresh(); };
  reduced.addEventListener('change', refreshListener);
  connection?.addEventListener('change', refreshListener);
  document.addEventListener('visibilitychange', refreshListener);
  video.addEventListener('error', errorListener);
  setState('poster');
  return {
    setPaused(value) { paused = Boolean(value); void refresh(); },
    retry() { failed = false; void refresh(); },
    destroy() {
      if (destroyed) return;
      destroyed = true;
      generation += 1;
      observer.disconnect();
      reduced.removeEventListener('change', refreshListener);
      connection?.removeEventListener('change', refreshListener);
      document.removeEventListener('visibilitychange', refreshListener);
      video.removeEventListener('error', errorListener);
      video.pause();
      video.removeAttribute('src');
      video.load();
    },
  };
}
