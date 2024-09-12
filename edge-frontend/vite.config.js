import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),  // Facilita a referência à pasta 'src'
    }
  },
  server: {
    host: true,
    watch:{
      usePolling: true
    },
    fs: {
      allow: ['..']  // Permite que Vite acesse diretórios acima de onde está sendo executado
    }
  },
  build: {
    outDir: 'dist',  // Garante que o build saia na pasta correta
  }
});
