📺 Processador de Vídeos do YouTube (Flask)
📌 Visão geral

Este projeto é uma aplicação web desenvolvida em Python (Flask) que permite ao usuário inserir uma URL de vídeo do YouTube e processar o conteúdo localmente para gerar um arquivo PDF estruturado (preview/relatório).

O sistema foi criado com foco em execução local e estudos de backend, explorando automação de processos, execução em segundo plano e geração de arquivos.

⚙️ Tecnologias utilizadas
Python 
Flask
HTML / CSS
Threads (processamento em segundo plano)
Geração de PDF

🧠 Funcionalidades principais
Inserção de URL de vídeo do YouTube via interface web
Processamento assíncrono utilizando threads
Geração de PDF com base no conteúdo processado
Interface simples e leve baseada em Flask
Execução local (localhost

🔄 Como funciona
O usuário envia uma URL do YouTube pela interface
O Flask inicia um processo em segundo plano (thread)
O sistema realiza o processamento local dos dados
Um PDF é gerado como saída final
O usuário pode visualizar ou baixar o arquivo gerado

🚫 Limitações de execução

Este projeto foi desenvolvido exclusivamente para ambiente local (localhost).

Ao tentar executar em servidores externos ou VPS, podem ocorrer limitações como:

Bloqueios do YouTube para requisições automatizadas
Identificação de tráfego como bot (ex: erro 429 ou CAPTCHA)
Falta de otimizações para ambiente de produção

Por esse motivo, o projeto não é recomendado para deploy em produção sem alterações na arquitetura.

🧪 Objetivo do projeto

Este projeto foi desenvolvido com fins de estudo para prática de:

Desenvolvimento web com Flask
Processamento em segundo plano (threads)
Automação de fluxos de dados
Geração de arquivos PDF
Estruturação de aplicações backend simples
📊 Status
✅ Funciona em ambiente local
⚠️ Não preparado para produção
🧪 Projeto de estudo e experimentação
📦 Mantido como referência de aprendizado


Projeto desenvolvido para fins educacionais e prática de desenvolvimento backend com Python.
