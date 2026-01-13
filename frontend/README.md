# PrazoNaMão — Frontend

Frontend em React + TypeScript + Vite + Tailwind.

Para rodar localmente:

1. Start backend (na raiz):

   ```bash
   uvicorn application.main:app --reload --port 8000
   ```

2. No diretório `frontend`:

   ```bash
   npm install
   npm run dev
   ```

3. Abra http://localhost:5173 e use a busca por advogado.

Observações:
- Ajuste `VITE_API_BASE_URL` se seu backend estiver em outra URL/porta.
- Para produção, gere build e sirva os arquivos estáticos ou configure um proxy/reverse proxy.
