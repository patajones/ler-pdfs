#!/usr/bin/env python3
"""
PDF to Markdown Converter

Esta aplicação converte arquivos PDF em formato Markdown,
preservando a estrutura e formatação do texto.
"""

import fitz  # PyMuPDF
import os
import re
import argparse
from pathlib import Path


class PDFToMarkdownConverter:
    def __init__(self):
        self.font_sizes = {}
        self.header_threshold = 0.8  # Threshold para identificar cabeçalhos
        
    def analyze_font_sizes(self, doc):
        """Analisa os tamanhos de fonte no documento para identificar hierarquia"""
        font_sizes = {}
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text_dict = page.get_text("dict")
            
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            size = round(span["size"], 1)
                            if size in font_sizes:
                                font_sizes[size] += len(span["text"])
                            else:
                                font_sizes[size] = len(span["text"])
        
        # Ordena por frequência para identificar texto principal
        sorted_sizes = sorted(font_sizes.items(), key=lambda x: x[1], reverse=True)
        self.font_sizes = dict(sorted_sizes)
        
        # Define tamanho principal (mais comum)
        if sorted_sizes:
            self.main_font_size = sorted_sizes[0][0]
        else:
            self.main_font_size = 12.0
    
    def get_header_level(self, font_size):
        """Determina o nível do cabeçalho baseado no tamanho da fonte"""
        if font_size <= self.main_font_size:
            return 0  # Texto normal
        
        # Calcula a diferença relativa
        size_diff = font_size - self.main_font_size
        
        if size_diff >= 6:
            return 1  # H1
        elif size_diff >= 4:
            return 2  # H2
        elif size_diff >= 2:
            return 3  # H3
        elif size_diff >= 1:
            return 4  # H4
        else:
            return 0  # Texto normal
    
    def clean_text(self, text):
        """Limpa e normaliza o texto"""
        # Remove múltiplos espaços
        text = re.sub(r'\s+', ' ', text)
        # Remove espaços no início e fim
        text = text.strip()
        return text
    
    def is_likely_header(self, text, font_size, flags):
        """Determina se um texto é provavelmente um cabeçalho"""
        text = text.strip()
        
        # Verifica se está vazio
        if not text:
            return False
        
        # Verifica tamanho da fonte
        if font_size <= self.main_font_size:
            return False
        
        # Verifica se é muito longo para ser cabeçalho
        if len(text) > 100:
            return False
        
        # Verifica se termina com ponto (menos provável ser cabeçalho)
        if text.endswith('.') and len(text) > 50:
            return False
        
        return True
    
    def extract_text_with_formatting(self, page):
        """Extrai texto com informações de formatação"""
        text_dict = page.get_text("dict")
        formatted_text = []
        
        for block in text_dict["blocks"]:
            if "lines" in block:
                block_text = []
                
                for line in block["lines"]:
                    line_text = []
                    
                    for span in line["spans"]:
                        text = span["text"]
                        if not text.strip():
                            continue
                            
                        font_size = round(span["size"], 1)
                        flags = span["flags"]
                        
                        # Verifica se é cabeçalho
                        if self.is_likely_header(text, font_size, flags):
                            header_level = self.get_header_level(font_size)
                            if header_level > 0:
                                text = f"{'#' * header_level} {text}"
                        
                        # Adiciona formatação para negrito e itálico
                        if flags & 2**4:  # Bold
                            text = f"**{text}**"
                        if flags & 2**1:  # Italic
                            text = f"*{text}*"
                        
                        line_text.append(text)
                    
                    if line_text:
                        block_text.append(" ".join(line_text))
                
                if block_text:
                    # Junta as linhas do bloco
                    block_content = "\n".join(block_text)
                    formatted_text.append(block_content)
        
        return "\n\n".join(formatted_text)
    
    def convert_pdf_to_markdown(self, pdf_path, output_path=None):
        """Converte PDF para Markdown"""
        try:
            # Abre o PDF
            doc = fitz.open(pdf_path)
            
            # Analisa tamanhos de fonte
            self.analyze_font_sizes(doc)
            
            # Extrai texto formatado de todas as páginas
            markdown_content = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                
                # Adiciona separador de página (exceto primeira)
                if page_num > 0:
                    markdown_content.append("\n---\n")
                
                # Adiciona número da página como comentário
                markdown_content.append(f"<!-- Página {page_num + 1} -->")
                
                # Extrai texto formatado
                page_text = self.extract_text_with_formatting(page)
                
                if page_text.strip():
                    markdown_content.append(page_text)
            
            # Junta todo o conteúdo
            full_markdown = "\n\n".join(markdown_content)
            
            # Limpa o markdown
            full_markdown = self.clean_markdown(full_markdown)
            
            # Define caminho de saída
            if output_path is None:
                pdf_name = Path(pdf_path).stem
                output_path = f"{pdf_name}.md"
            
            # Salva o arquivo markdown
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(full_markdown)
            
            doc.close()
            
            return output_path
            
        except Exception as e:
            print(f"Erro ao converter PDF: {e}")
            return None
    
    def clean_markdown(self, text):
        """Limpa e melhora o markdown gerado"""
        # Remove múltiplas linhas vazias
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        # Remove espaços extras no final das linhas
        text = re.sub(r' +\n', '\n', text)
        
        # Corrige cabeçalhos mal formatados
        text = re.sub(r'^(#{1,6})\s*$', '', text, flags=re.MULTILINE)
        
        return text.strip()


def main():
    parser = argparse.ArgumentParser(description='Converte PDF para Markdown')
    parser.add_argument('pdf_file', help='Caminho para o arquivo PDF')
    parser.add_argument('-o', '--output', help='Caminho para o arquivo de saída (opcional)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Modo verboso')
    
    args = parser.parse_args()
    
    # Verifica se o arquivo PDF existe
    if not os.path.exists(args.pdf_file):
        print(f"Erro: Arquivo '{args.pdf_file}' não encontrado.")
        return 1
    
    # Cria o conversor
    converter = PDFToMarkdownConverter()
    
    if args.verbose:
        print(f"Convertendo '{args.pdf_file}' para Markdown...")
    
    # Converte o PDF
    output_file = converter.convert_pdf_to_markdown(args.pdf_file, args.output)
    
    if output_file:
        print(f"✅ Conversão concluída! Arquivo salvo como: {output_file}")
        
        # Mostra estatísticas se verbose
        if args.verbose:
            file_size = os.path.getsize(output_file)
            print(f"📊 Tamanho do arquivo gerado: {file_size} bytes")
            
            with open(output_file, 'r', encoding='utf-8') as f:
                lines = len(f.readlines())
            print(f"📄 Número de linhas: {lines}")
        
        return 0
    else:
        print("❌ Falha na conversão.")
        return 1


if __name__ == "__main__":
    exit(main())