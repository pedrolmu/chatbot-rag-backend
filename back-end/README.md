# Back-end RAG - Generative AI Advanced Net

**Aluno:** Pedro Leal Murad  
**RM:** 565460  
**Turma:** 2TIAPF 2026  
**Disciplina:** Generative AI Advanced Net

## 1. Visão geral

Este trabalho evolui o back-end de um chatbot RAG, mantendo a proposta original do projeto: receber uma pergunta do usuário, buscar trechos relevantes em uma base vetorial e gerar uma resposta contextualizada com apoio de um modelo de linguagem.

A implementação foi feita apenas no diretório `back-end`, preservando a compatibilidade com o front-end existente. O back-end foi organizado em camadas para facilitar manutenção, testes e futuras trocas de provedor, como trocar o modelo de linguagem ou substituir o banco vetorial.

## 2. Fluxo da solução

```text
Usuário -> FastAPI -> Embedding da pergunta -> Qdrant -> Contexto recuperado -> LLM -> Resposta final
```

Na prática, o sistema funciona assim:

1. O usuário envia uma pergunta para o endpoint `/chat`.
2. O back-end transforma a pergunta em embedding.
3. O Qdrant faz a busca semântica nos documentos indexados.
4. Os trechos mais relevantes são enviados como contexto para o modelo de linguagem.
5. A resposta é devolvida junto com as fontes recuperadas.

Esse desenho evita que o modelo responda apenas de forma genérica, porque a resposta passa a ser orientada pelo conteúdo armazenado no banco vetorial.

## 3. Tecnologias utilizadas

- **FastAPI**: criação dos endpoints do back-end.
- **Qdrant**: banco vetorial usado para armazenar embeddings e realizar busca semântica.
- **OpenAI**: geração de respostas conversacionais e geração de embeddings.
- **Docker / Docker Compose**: execução padronizada do back-end e do Qdrant.
- **Pydantic**: validação dos dados de entrada e saída.
- **Pytest**: testes automatizados básicos.

## 4. Estrutura do projeto

```text
back-end/
├── src/
│   ├── core/              # Configurações, segurança e logging
│   ├── models/            # Schemas Pydantic
│   ├── routes/            # Rotas HTTP
│   ├── services/          # LLM, Qdrant, ingestão e orquestração RAG
│   └── utils/             # Funções auxiliares, como chunking
├── data/docs/             # Documento real de exemplo
├── tests/                 # Testes automatizados
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── scripts_ingest_sample.py
```

## 5. Banco vetorial escolhido

O banco vetorial escolhido foi o **Qdrant**, executado localmente em contêiner Docker.

A escolha foi feita por três motivos principais:

1. O Qdrant é próprio para busca vetorial e suporta similaridade por cosseno.
2. A integração com Python é simples e estável.
3. Ele permite uma demonstração local sem depender de um cluster pago em nuvem.

A coleção padrão usada no projeto é:

```text
fiap_rag_docs
```

## 6. Modelo de linguagem escolhido

Foi utilizada a API da **OpenAI**.

Configuração padrão:

```text
Modelo conversacional: gpt-4o-mini
Modelo de embedding: text-embedding-3-small
Dimensão do embedding: 1536
```

A dimensão `1536` foi mantida no Qdrant para ser compatível com o modelo `text-embedding-3-small`.

## 7. Configuração das variáveis de ambiente

Copie o arquivo de exemplo:

```bash
cp .env.example .env
```

Preencha o arquivo `.env`:

```env
APP_NAME=RAG Backend - Generative AI Advanced Net
ENVIRONMENT=development
API_KEY=troque_esta_chave_para_proteger_a_api
OPENAI_API_KEY=sua_chave_openai_aqui
OPENAI_CHAT_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSION=1536
QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=fiap_rag_docs
TOP_K=4
MAX_CHUNK_SIZE=900
CHUNK_OVERLAP=150
```

Observação: ao executar pelo `docker compose`, o arquivo `docker-compose.yml` ajusta internamente o endereço do Qdrant para `http://qdrant:6333`. Para execução local fora do Docker, mantenha `QDRANT_URL=http://localhost:6333`.

## 8. Executar com Docker Compose

Com o `.env` configurado, execute:

```bash
docker compose up --build
```

A API ficará disponível em:

```text
http://localhost:8000
```

A documentação automática do FastAPI ficará em:

```text
http://localhost:8000/docs
```

## 9. Executar localmente sem Docker

Primeiro, suba apenas o Qdrant:

```bash
docker run -p 6333:6333 qdrant/qdrant:v1.12.5
```

Depois, em outro terminal:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

## 10. Indexação de documento real

O projeto já possui um documento de exemplo em:

```text
data/docs/exemplo_motor_eletrico.txt
```

Para indexar esse documento no Qdrant:

```bash
python scripts_ingest_sample.py
```

Esse script executa as seguintes etapas:

1. Lê o arquivo de texto.
2. Divide o conteúdo em chunks com sobreposição.
3. Gera embeddings para cada trecho.
4. Grava os vetores e metadados no Qdrant.

## 11. Exemplos de chamadas aos endpoints

### Health check

```bash
curl http://localhost:8000/health
```

Resposta esperada:

```json
{
  "status": "ok",
  "service": "RAG Backend - Generative AI Advanced Net"
}
```

### Consultar a coleção padrão

```bash
curl -H "X-API-Key: troque_esta_chave_para_proteger_a_api" \
http://localhost:8000/collections/default
```

### Indexar um documento manualmente

```bash
curl -X POST http://localhost:8000/collections/ingest \
  -H "Content-Type: application/json" \
  -H "X-API-Key: troque_esta_chave_para_proteger_a_api" \
  -d '{
    "source": "manual_motor.txt",
    "text": "Motores elétricos devem ser monitorados por temperatura, corrente elétrica, vibração e rotação. Alterações nesses sinais podem indicar falhas mecânicas, sobrecarga ou necessidade de manutenção preditiva."
  }'
```

### Conversar com recuperação semântica

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -H "X-API-Key: troque_esta_chave_para_proteger_a_api" \
  -d '{
    "message": "Quais sinais podem indicar falha em um motor elétrico?",
    "history": []
  }'
```

A resposta retorna dois pontos importantes:

- `answer`: resposta final gerada pelo modelo.
- `sources`: trechos recuperados do Qdrant, com fonte, score e conteúdo.

## 12. Melhorias de design implementadas

### 12.1 Separação de responsabilidades

O back-end foi dividido em `routes`, `services`, `models`, `core` e `utils`. Essa separação evita que a regra de negócio fique dentro das rotas e facilita manutenção. Por exemplo, a rota `/chat` apenas recebe a requisição e delega a execução para o orquestrador RAG.

### 12.2 Serviço único para LLM e embeddings

A integração com a OpenAI foi concentrada em `openai_service.py`. Isso deixa o projeto mais flexível, porque uma futura troca para Anthropic, Gemini, Azure, Bedrock ou Ollama exigiria alteração principalmente nessa camada.

### 12.3 Banco vetorial isolado em serviço próprio

A comunicação com o Qdrant fica em `qdrant_service.py`. A criação da coleção, o envio dos vetores e a busca semântica ficam centralizados, evitando duplicação de código.

### 12.4 Chunking com metadados

O texto é dividido em partes menores com sobreposição. Cada chunk recebe metadados como fonte, índice e quantidade de caracteres. Isso melhora a qualidade da busca semântica e permite rastrear de onde veio a resposta.

### 12.5 Segurança básica por API key

As rotas principais usam validação por `X-API-Key`. Em ambiente de desenvolvimento, a configuração pode ser mais simples, mas em produção a chave deve ser alterada no `.env`.

### 12.6 Logging e tratamento de erros

Foram adicionados logs estruturados e tratamento de exceções nas rotas. Isso ajuda a identificar falhas de configuração, erro no Qdrant, ausência de chave da OpenAI ou problema durante a geração da resposta.

### 12.7 Automação com Docker

O projeto possui `Dockerfile` e `docker-compose.yml`, permitindo subir o back-end e o Qdrant com um comando. Isso reduz erros de ambiente e facilita a avaliação do projeto.

### 12.8 Testes automatizados

Foram incluídos testes básicos para o health check e para a função de chunking. A cobertura não é completa, mas valida partes importantes da estrutura inicial.

## 13. Testes

Para rodar os testes:

```bash
pytest
```

Os testes cobrem:

- Endpoint `/health`.
- Criação de chunks a partir de texto.

## 14. Demonstração sugerida

Para demonstrar o funcionamento ponta a ponta:

1. Configurar o `.env`.
2. Subir a aplicação com `docker compose up --build`.
3. Rodar `python scripts_ingest_sample.py`.
4. Fazer uma pergunta pelo endpoint `/chat`.
5. Conferir o campo `sources` na resposta para validar que o conteúdo veio dos documentos indexados.

## 15. Considerações finais

A solução atende ao objetivo principal do trabalho: evoluir o back-end para um fluxo RAG funcional, usando banco vetorial real, modelo de linguagem integrado, variáveis de ambiente e melhorias arquiteturais justificadas. A estrutura também permite evolução futura, como adicionar autenticação mais robusta, ampliar testes, incluir novos formatos de documentos e trocar o provedor de modelo.
