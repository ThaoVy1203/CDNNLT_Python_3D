import { defineConfig } from 'vite';
import path from 'path';

// Vite config riêng để build Three.js viewer thành standalone bundle
export default defineConfig({
  build: {
    lib: {
      entry: path.resolve(__dirname, 'src/three/index.ts'),
      name: 'ThreeViewer',
      fileName: (format) => `three-viewer.${format}.js`,
      formats: ['umd', 'es']
    },
    rollupOptions: {
      external: [],
      output: {
        globals: {}
      }
    },
    outDir: 'dist/three',
    emptyOutDir: true
  }
});
