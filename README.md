# Da sua experiência à tecnologia

Landing page estática, em português, sem dependências, backend, coleta de leads ou pagamento interno.

## Executar

Na pasta do projeto: `python3 -m http.server 8000 --bind 0.0.0.0`.
Hospede o conteúdo desta pasta em qualquer hospedagem estática. Não há build.

## Configuração antes da publicação

Edite apenas `config.js` para definir checkout (HTTPS), preço, autoria, contato, capa, páginas internas e links institucionais. `CHECKOUT_URL` contém exatamente o placeholder solicitado. Sem URL válida, os links comerciais ficam indisponíveis, com mensagem acessível. Com URL configurada, todos levam diretamente ao checkout externo na mesma aba.

A capa original (`assets/capa.webp`) e três prévias reais foram extraídas do PDF fornecido pelo usuário, nas páginas 1, 6, 11 e 18. As prévias abrem a imagem ampliada em nova aba. As imagens são WebP locais e o PDF completo não faz parte dos arquivos públicos. Para substituí-las, atualize `coverUrl` e `previewImages` em `config.js`.

O preço não foi informado; a página orienta consultá-lo no checkout. Autoria, contato e links institucionais ficam ocultos até serem preenchidos. O arquivo fornecido está em PDF. Confirme os procedimentos de acesso na plataforma; ajuste o FAQ se necessário. Não há políticas de garantia ou entrega presumidas.

## Validação

Verifique em mobile e desktop, navegação por teclado e URLs antes de publicar. O layout usa fontes locais, imagens WebP otimizadas e respeita a preferência por movimento reduzido. Não há chamadas a APIs ou serviços externos durante o carregamento. Inclua URL canônica e metadados sociais quando o domínio e a capa final estiverem definidos.

Validação no Chromium concluída em 360, 390, 768 e 1440 pixels: sem rolagem horizontal, imagens carregadas, três prévias reais, FAQ funcional e checkout indisponível com placeholder. O redirecionamento e o preço configurável foram verificados com dados temporários de teste, não salvos.
