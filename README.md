# PDF to Markdown Converter

Uma aplicação Python que converte arquivos PDF em formato Markdown, preservando a estrutura e formatação do texto.

## Características

- ✅ Converte PDFs para Markdown mantendo a formatação
- ✅ Identifica cabeçalhos automaticamente baseado no tamanho da fonte
- ✅ Preserva texto em **negrito** e *itálico*
- ✅ Adiciona separadores entre páginas
- ✅ Interface de linha de comando fácil de usar
- ✅ Suporte para arquivos grandes

## Instalação

1. Clone ou baixe este repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Uso

### Uso Básico

```bash
python pdf_to_markdown.py arquivo.pdf
```

Isso criará um arquivo `arquivo.md` no mesmo diretório.

### Especificar arquivo de saída

```bash
python pdf_to_markdown.py arquivo.pdf -o saida.md
```

### Modo verboso

```bash
python pdf_to_markdown.py arquivo.pdf -v
```

### Ajuda

```bash
python pdf_to_markdown.py -h
```

## Exemplos

```bash
# Converter o PDF existente no diretório
python pdf_to_markdown.py meu-documento.pdf

# Converter com nome específico
python pdf_to_markdown.py meu-documento.pdf -o documento.md

# Converter com informações detalhadas
python pdf_to_markdown.py meu-documento.pdf -v
```

## Como Funciona

1. **Análise de Fontes**: A aplicação primeiro analisa todos os tamanhos de fonte no documento para identificar a hierarquia
2. **Identificação de Cabeçalhos**: Textos com fontes maiores são convertidos em cabeçalhos Markdown (H1, H2, H3, etc.)
3. **Preservação de Formatação**: Texto em negrito e itálico é preservado
4. **Estrutura**: Cada página é separada por uma linha horizontal (`---`)
5. **Limpeza**: O texto final é limpo e formatado adequadamente

## Dependências

- `pymupdf` (fitz): Para leitura e processamento de PDFs
- `python-markdown`: Para processamento adicional de Markdown

## Limitações

- A qualidade da conversão depende da estrutura do PDF original
- PDFs com muitas imagens ou layouts complexos podem não ser convertidos perfeitamente
- Tabelas complexas podem perder formatação

## Contribuição

Sinta-se livre para contribuir com melhorias, correções de bugs ou novas funcionalidades!

## Licença

Este projeto é de código aberto. Use livremente para seus projetos.