# objective

Verificar as regras oficiais do **BNB Hack: Tokenized Stocks Edition**, mapear a Binance Web3 API para uma investigação read-only e uma demo vertical, corrigir excessos do anexo de Grok e avaliar dois repositórios GitHub. `checked_at=2026-10-01`.

# work done

Li o manual operativo, o contexto local, os recursos, o plano, os relatórios, o contrato documental da RWA Data API e o texto colado atribuído ao Grok. Não editei ficheiros, não instalei nada e não fiz chamadas autenticadas.

Consultei diretamente as páginas oficiais do hackathon, o blog oficial, a documentação Binance Web3 API, a documentação Agentic Wallet e dois repositórios GitHub.

# official rule matrix with dated URLs

| Tema | Verificação oficial |
|---|---|
| Nome, datas e timezone | **BNB Hack: Tokenized Stocks Edition**, 16 de setembro a 11 de outubro de 2026, UTC+0. Submissões fecham em 11 de outubro às 12:00 UTC. [Página oficial](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=overview), `checked_at=2026-10-01` |
| Elegibilidade | Equipas e participantes individuais. Uma entrada por equipa. Repo, demo e link publicado têm de permanecer acessíveis durante o julgamento. Há restrições para residentes, cidadãos ou pessoas localizadas nos EUA, Canadá, Países Baixos, Irão, Cuba, Coreia do Norte, Crimeia, Donetsk, Luhansk, Reino Unido e Japão, além de sanções aplicáveis. [Página oficial](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=overview), `checked_at=2026-10-01` |
| Track e activos | Uma track. Pelo menos um de **bStocks, Ondo ou xStocks** tem de ser central. Produtos cross-asset são permitidos. [Tracks oficiais](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=tracks), `checked_at=2026-10-01` |
| Execução | Apenas spot. Perps estão excluídos. O alvo é BSC mainnet. A página recomenda dry-run com Transaction API durante o build e uma demo live com montantes pequenos. [Tracks oficiais](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=tracks), `checked_at=2026-10-01` |
| Binance Web3 API | O projecto tem de usar um ou mais módulos Binance Web3 API. Agentic Wallet e Wallet Skills são opcionais. [Overview oficial](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=overview), `checked_at=2026-10-01` |
| Entregáveis | Projecto funcional, repo público, vídeo até quatro minutos, recomendado mas explicitamente opcional, e link publicado ou instruções reproduzíveis. [Overview oficial](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=overview), `checked_at=2026-10-01` |
| DevEx Report | É obrigatório e vale 25%. Deve documentar onboarding, problemas da documentação, erros, edge cases, latência, liquidez, slippage, comportamento fora do horário tradicional e diferenças práticas entre bStocks, Ondo e xStocks. Relatórios vagos ou gerados sem experiência real não são aceites. [Overview oficial](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=overview), `checked_at=2026-10-01` |
| Pesos | Implementação técnica 30%, criatividade e originalidade 25%, DevEx Report 25%, qualidade de produto e UX 20%. [Overview oficial](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=overview), `checked_at=2026-10-01` |
| Tie-break | Profundidade do uso da Web3 API primeiro, seguida da qualidade do DevEx Report. [Blog oficial](https://www.bnbchain.org/en/blog/bnb-hack-tokenized-stocks-edition-with-binance-web3-wallet), `checked_at=2026-10-01` |
| Prémios especiais | US$2.000 para Best Use of Agentic Wallet / Wallet Skills, financiado pela Binance Web3 Wallet, e US$2.000 para Best Use of BNB Agent Studio, financiado pela BNB Chain. [Prizes oficiais](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=prizes), `checked_at=2026-10-01` |
| Agent Studio | Opcional. Está ligado ao prémio especial, não à elegibilidade geral. [Tracks oficiais](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=tracks), `checked_at=2026-10-01` |
| UID e campos privados | A página pública não especifica UID, campos internos do formulário, permissões individuais da conta API ou requisitos privados de payout. Estado: desconhecido. [Formulário de submissão](https://forms.gle/yToDUzaDMwWnq6R6A), `checked_at=2026-10-01` |

# API map

| Caminho | Endpoints documentados | Acesso esperado | Estado |
|---|---|---|---|
| Investigação read-only | RWA `platforms`, `search`, `price`, `underlying-profile`, `underlying-market` | API Key, Secret Key e assinatura HMAC-SHA256. A documentação não declara scopes read-only granulares. [RWA Data](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data), [Authentication](https://web3.binance.com/en/dev-docs/authentication), `checked_at=2026-10-01` | Documentado. Não testado |
| Quote candidato | Trading API `GET /quote` | API Key, Secret Key, assinatura e `userWalletAddress`. Para equity/RWA, a rota documenta `executionMode=RFQ`. [Trading API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api), `checked_at=2026-10-01` | Documentado. Não testado |
| Construção da operação | `GET /swap`, depois assinatura EIP-712 do `typedDataToSign` | Credenciais API e carteira capaz de assinar. [Trading API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/trading-api), `checked_at=2026-10-01` | Documentado. Não executar nesta fase |
| Simulação | Transaction API `POST /simulate` com `evmTx` | API Key, Secret Key e assinatura. A documentação prevê resultado simulado, alterações de saldo e allowances. [Transaction API](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/transaction-api), `checked_at=2026-10-01` | Documentado. Compatibilidade com uma ordem RFQ concreta permanece não testada |
| Agentic Wallet | Pesquisa e negociação de bStock e Ondo por ticker ou nome | Agentic Wallet instalado, sessão autenticada, Wallet Skill e USDT mais gas para trading. [Stock Trading oficial](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading), `checked_at=2026-10-01` | Documentado. Não instalado nem usado |
| xStocks | A track aceita xStocks, mas a RWA Data API consultada documenta `platformId` `ondo` e `bstock`, sem enum xStocks. [RWA Data](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data), `checked_at=2026-10-01` | Cobertura xStocks pela mesma rota: desconhecida |

Vertical slice recomendado: `search` ou lista de plataforma, `underlying-profile`, `price`, estado de mercado, quote para um montante fixo e simulação da transacção. Deve mostrar contrato, emissor/plataforma, timestamp, estado, unidade, quote, erro e motivo de falha. Nenhum desses comportamentos foi testado live.

# facts

A API exige credenciais e assinatura em todos os endpoints documentados. A assinatura usa Secret Key e o caminho assinado inclui `/build`. [Authentication](https://web3.binance.com/en/dev-docs/authentication), `checked_at=2026-10-01`.

`referencePrice` é documentado como preço por acção convertido a partir do preço on-chain do token, não como cotação oficial independente do mercado tradicional. [RWA Data](https://web3.binance.com/en/dev-docs/catalog/web3-wallet/api/rest-api/rwa-data), `checked_at=2026-10-01`.

O uso oficial Agentic Wallet já cobre pesquisa e trading conversacional de bStock e Ondo. [Stock Trading](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading), `checked_at=2026-10-01`.

# inferences

A melhor fatia read-only é um verificador de elegibilidade, estado de mercado, referência e quote, com explicação das diferenças entre representações. Um simples agente “compra AAPL” tem diferenciação limitada porque já existe como caso de uso oficial.

A ausência de xStocks na enumeração RWA não prova que xStocks esteja excluído de toda a Binance Web3 API. Exige teste separado ou confirmação dos organizadores.

# unknowns

Continuam desconhecidos: scopes reais da API, limites da conta, cobertura live por ticker e emissor, latência, erros concretos, disponibilidade RFQ fora do horário tradicional, suporte xStocks, campos privados do formulário, UID, regras de payout e compatibilidade entre simulação e ordens RFQ.

# counterevidence

O evento já publica Agentic Wallet para stocks, o BNB Agent Studio tem referência própria e a página oficial lista monitorização de preço, arbitragem, DCA, baskets e onboarding como ideias. Um dashboard genérico ou um chatbot de ticker enfrenta substitutos oficiais. [Stock Trading](https://developers.binance.com/en/docs/products/agentic-wallet/use-cases/trading/stock-trading), `checked_at=2026-10-01`.

# Grok corrections

- **Sponsor:** a página identifica Binance Web3 Wallet como sponsor e diz que o pool é financiado por BNB Chain e Binance Web3 Wallet. Isso não torna Ondo ou xStocks sponsors. [Overview](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=overview), `checked_at=2026-10-01`.
- **Issuer:** bStocks, Ondo e xStocks são famílias de activos ou emissores distintos. O requisito é centralidade no projecto, não uma relação contratual entre os três e Binance. [Tracks](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=tracks), `checked_at=2026-10-01`.
- **25% DevEx:** é peso de avaliação, não permissão API, papel de sponsor ou requisito de Agent Studio. [Overview](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=overview), `checked_at=2026-10-01`.
- **Agent Studio:** é opcional e ligado a um prémio especial. Não é obrigatório para a track principal. [Tracks](https://www.bnbchain.org/en/hackathons/tokenized-stocks?tab=tracks), `checked_at=2026-10-01`.
- **CZ, YZi Labs e júri:** o anexo não fornece base oficial para os apresentar como sponsors, jurados ou decisores. Não usei essas relações.

# skill options

- [binance/binance-skills-hub](https://github.com/binance/binance-skills-hub): cerca de 1.000 stars, MIT nas skills, actividade recente visível em pull requests de setembro de 2026. É directamente relevante para Agentic Wallet e tokenized securities. Compatibilidade com Codex é possível ao nível de instruções Markdown, mas o repositório pede CLI própria e instalação, por isso recomendo apenas leitura nesta fase. `checked_at=2026-10-01`.
- [github/gh-aw](https://github.com/github/gh-aw): cerca de 5,2 mil stars, MIT, actividade recente e suporte documentado para OpenAI Codex como engine. É útil para workflows GitHub repetíveis, não para a pesquisa API em si. Rejeitar para o slice inicial porque acrescenta infraestrutura e não resolve a cobertura, autenticação ou teste da Binance API. [Documentação oficial](https://github.github.com/gh-aw/about/), `checked_at=2026-10-01`.

# recommendation

Escolher um slice read-only com RWA Data API e, depois de credenciais seguras e autorização explícita, acrescentar uma quote RFQ sem submissão de ordem. Não adoptar Agent Studio antes de provar que identidade, runtime e x402 melhoram a tarefa.

# strongest counterargument

A avaliação dá grande peso à profundidade da API e tem um prémio para Agentic Wallet e outro para Agent Studio. Uma integração read-only pode perder pontos face a um projecto que demonstre execução autónoma. A resposta é medir primeiro a cobertura e os erros, para evitar construir uma demo que não consegue cotar ou explicar um activo real.

# impact on decision

A escolha deve ser um produto de verificação e decisão de execução, não um agente de PnL. A decisão permanece condicional à obtenção de uma credencial API de baixo risco e à confirmação de uma quote reproduzível para pelo menos um activo elegível.

# next checks

1. Obter credencial própria com permissões mínimas, sem reutilizar segredos existentes.
2. Testar apenas `search`, `profile`, `price` e `market status`.
3. Medir quote RFQ em montante fixo, sem assinar nem submeter.
4. Confirmar xStocks e campos privados diretamente com os organizadores.
5. Registar tempos, erros e documentação para o DevEx Report.

# limitations

A pesquisa não fez chamadas autenticadas, não testou endpoints, não verificou o formulário privado, não instalou skills e não confirmou comportamento live de qualquer emissor. Consultei páginas oficiais e GitHub diretamente, sem Firecrawl.