import os
import re
import pandas as pd
from collections import defaultdict
try:
    import keyring
except ImportError:
    keyring = None
    
service_name ="GITHUB_TOKEN"
username = "LAB_EXPERIMENTACAO"

# Função para obter o token do GitHub
def get_github_token():
    """
    Recupera o token do GitHub de forma segura:
    - Primeiro tenta via variável de ambiente GITHUB_TOKEN
    - Depois tenta via keyring (se disponível)
    """
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token

    if keyring:
        token = keyring.get_password(service_name, username)
        if token:
            return token

    raise EnvironmentError(
        "Nenhum token do GitHub encontrado. "
        "Configure no keyring ou na variável de ambiente 'GITHUB_TOKEN'."
    )

# Função para gerar CSV de comentários por classe a partir de um repositório clonado
def generate_comments_by_class(repo_dir, class_csv_path, output_dir):
    """
    Lê class.csv (gerado pelo CK), percorre os arquivos .java do repo e conta
    comentários por classe. Gera um CSV separado em output_dir/comments_by_class.csv.

    Estratégia:
    - Para cada arquivo listado em class.csv, abre o arquivo e localiza comentários
      via regex (// ... ou /* ... */).
    - Localiza declarações de classes/interfaces/enums e determina o bloco da classe
      via busca do '{' e brace-matching simples.
    - Atribui cada comentário à classe mais interna que o contém (por posição).
    - Escreve CSV com colunas: file, class, line_comments, block_comments, comment_lines, total_comments
    """
    try:
        df_class = pd.read_csv(class_csv_path, encoding="utf-8", encoding_errors="ignore")
    except Exception as e:
        print(f"[!] Não foi possível ler {class_csv_path}: {e}")
        return None

    comment_re = re.compile(r'//.*?$|/\*.*?\*/', re.DOTALL | re.MULTILINE)
    class_decl_re = re.compile(r'\b(class|interface|enum)\s+([A-Za-z_][A-Za-z0-9_$]*)', re.MULTILINE)

    # mapping: (file_rel, class_name) -> counters
    counters = defaultdict(lambda: {"line_comments": 0, "block_comments": 0, "comment_lines": 0, "total_comments": 0})

    processed_files = set()

    for _, row in df_class.iterrows():
        file_rel = row.get('file')
        class_name_ck = row.get('class')
        if not isinstance(file_rel, str) or not isinstance(class_name_ck, str):
            continue

        file_rel_norm = os.path.normpath(file_rel)
        abs_path = os.path.join(repo_dir, file_rel_norm)
        if not os.path.exists(abs_path):
            # tenta também sem normalização (algumas entradas do CK podem usar separadores diferentes)
            abs_path = os.path.join(repo_dir, file_rel)
            if not os.path.exists(abs_path):
                # arquivo não encontrado; pula
                continue

        if abs_path in processed_files:
            # já processado o arquivo, mas garantimos que exista a chave para esta classe
            _ = counters[(file_rel_norm, class_name_ck)]
            continue

        processed_files.add(abs_path)

        try:
            with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"[!] Não foi possível abrir {abs_path}: {e}")
            continue

        # Encontra ranges de classes no arquivo
        class_ranges = []
        for m in class_decl_re.finditer(content):
            cname = m.group(2)
            # procurar '{' após a declaração
            brace_idx = content.find('{', m.end())
            if brace_idx == -1:
                continue
            # brace matching simples
            depth = 0
            i = brace_idx
            end_idx = None
            L = len(content)
            while i < L:
                ch = content[i]
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        end_idx = i + 1
                        break
                i += 1
            if end_idx:
                # armazena (nome, start, end)
                class_ranges.append((cname, brace_idx, end_idx))

        # ordena por tamanho do range (menor primeiro) para escolher a classe interna mais específica
        class_ranges.sort(key=lambda x: (x[2] - x[1]))

        # percorre comentários
        for cm in comment_re.finditer(content):
            start_pos = cm.start()
            text = cm.group(0)
            lines = text.count('\n') + 1
            is_block = text.startswith('/*')
            assigned = False
            # encontra the classe mais interna que contém este comentário
            for cname, s, e in class_ranges:
                if s <= start_pos < e:
                    key = (file_rel_norm, cname)
                    if is_block:
                        counters[key]["block_comments"] += 1
                    else:
                        counters[key]["line_comments"] += 1
                    counters[key]["comment_lines"] += lines
                    counters[key]["total_comments"] += 1
                    assigned = True
                    break
            if not assigned:
                # comentário fora de classes: atribui a entrada com class '<file_level>'
                key = (file_rel_norm, '<file_level>')
                if is_block:
                    counters[key]["block_comments"] += 1
                else:
                    counters[key]["line_comments"] += 1
                counters[key]["comment_lines"] += lines
                counters[key]["total_comments"] += 1

    # Garante que todas as classes listadas no class.csv apareçam (mesmo que 0)
    for _, row in df_class.iterrows():
        file_rel = row.get('file')
        class_name_ck = row.get('class')
        if isinstance(file_rel, str) and isinstance(class_name_ck, str):
            key = (os.path.normpath(file_rel), class_name_ck)
            if key not in counters:
                counters[key]  # inicializa com zeros

    # Prepara output
    os.makedirs(output_dir, exist_ok=True)
    out_csv = os.path.join(output_dir, 'comments_by_class.csv')
    try:
        import csv
        with open(out_csv, 'w', newline='', encoding='utf-8') as fout:
            writer = csv.writer(fout)
            writer.writerow(['file', 'class', 'line_comments', 'block_comments', 'comment_lines', 'total_comments'])
            for (file_rel, cname), vals in sorted(counters.items()):
                writer.writerow([file_rel, cname, vals["line_comments"], vals["block_comments"], vals["comment_lines"], vals["total_comments"]])
        print(f"[✓] CSV de comentários gerado em: {out_csv}")
        return out_csv
    except Exception as e:
        print(f"[!] Falha ao gravar {out_csv}: {e}")
        return None