import os
import shutil
import subprocess
import sys
import pandas as pd
import requests
import zipfile
import time
from utils.utils import get_github_token, generate_comments_by_class
from datetime import timedelta
from urllib.parse import urlparse
from git import repo

def get_default_branch(repo_url):
    """
    Detecta a default branch de forma robusta:
    1. Tenta via git ls-remote
    2. Fallback para API GitHub (se possível)
    3. Fallback final: main/master/trunk
    """
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--symref", repo_url, "HEAD"],
            capture_output=True, text=True, timeout=30, check=True
        )
        for line in result.stdout.splitlines():
            if line.startswith("ref:"):
                parts = line.split()
                if len(parts) >= 3 and parts[1].startswith("refs/heads/"):
                    return parts[1].replace("refs/heads/", "")
    except Exception as e:
        print(f"[!] Falha com git ls-remote: {e}")

    try:
        if "github.com" in repo_url:
            parts = urlparse(repo_url).path.strip("/").split("/")
            if len(parts) >= 2:
                owner, repo_name = parts[0], parts[1].replace(".git", "")
                api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
                headers = {}
                token = get_github_token()
                if token:
                    headers["Authorization"] = f"token {token}"
                response = requests.get(api_url, headers=headers, timeout=30)
                if response.status_code == 200:
                    return response.json().get("default_branch", "main")
    except Exception as e:
        print(f"[!] Falha na API do GitHub: {e}")

    return "main"
    

def clone_repo(repo_url, dest_dir='repo'):
    import stat
    def remove_readonly(func, path, excinfo):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir, onerror=remove_readonly)
    
    print(f"[+] Baixando repositório de {repo_url} como ZIP...")
    
    try:
        if 'github.com' in repo_url:
            clean_url = repo_url.replace('.git', '')
            default_branch = get_default_branch(repo_url)
            zip_url = f"{clean_url}/archive/refs/heads/{default_branch}.zip"
            
            success = download_and_extract_zip(zip_url, dest_dir)
            
            if not success:
                print("[!] Download ZIP falhou, tentando git clone...")
                return clone_with_git(repo_url, dest_dir)
                
            return dest_dir
        else:
            return clone_with_git(repo_url, dest_dir)
            
    except Exception as e:
        print(f"[!] Erro no download ZIP: {e}")
        return clone_with_git(repo_url, dest_dir)

def download_and_extract_zip(zip_url, dest_dir):
    """
    Baixa e extrai um arquivo ZIP do repositório
    """
    try:
        # Download do ZIP
        print(f"[+] Baixando ZIP de {zip_url}...")
        response = requests.get(zip_url, stream=True, timeout=60)
        response.raise_for_status()
        
        zip_path = f"{dest_dir}.zip"
        
        # Salva o arquivo ZIP
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"[+] Extraindo ZIP...")
        
        # Extrai o ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('temp_extract')
        
        # Move o conteúdo da pasta extraída para o destino final
        extracted_folders = os.listdir('temp_extract')
        if extracted_folders:
            extracted_path = os.path.join('temp_extract', extracted_folders[0])
            shutil.move(extracted_path, dest_dir)
        
        # Limpa arquivos temporários
        os.remove(zip_path)
        if os.path.exists('temp_extract'):
            shutil.rmtree('temp_extract')
        
        print(f"[✓] Repositório extraído com sucesso para {dest_dir}")
        return True
        
    except Exception as e:
        print(f"[!] Erro no download/extração ZIP: {e}")
        # Limpa arquivos temporários em caso de erro
        for temp_file in [f"{dest_dir}.zip", 'temp_extract']:
            if os.path.exists(temp_file):
                try:
                    if os.path.isfile(temp_file):
                        os.remove(temp_file)
                    else:
                        shutil.rmtree(temp_file)
                except:
                    pass
        return False

def clone_with_git(repo_url, dest_dir):
    """
    Fallback para git clone tradicional
    """
    print(f"[+] Clonando com git de {repo_url}...")
    
    try:
        subprocess.run(['git', 'config', '--global', 'core.longpaths', 'true'], 
                      capture_output=True, check=False)
        repo.clone_from(repo_url, dest_dir, depth=1)
        return dest_dir
    except Exception as e:
        print(f"[!] Erro ao clonar {repo_url}: {e}")
        try:
            cmd = ['git', 'clone', '--depth', '1', repo_url, dest_dir]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return dest_dir
        except subprocess.CalledProcessError as git_error:
            print(f"[!] Falha no clone alternativo: {git_error.stderr}")
            raise e

def run_ck(jar_path, repo_dir, repo_name, output_base='ck_output'):
    """
    Executa o CK Tool para um repositório e salva os CSVs em uma subpasta.
    Se ocorrer erro, tenta retornar arquivos parciais.
    """
    output_dir = os.path.join(output_base, repo_name.replace("/", "_"))
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    print(f"[+] Executando CK Tool em {repo_dir} ...")

    cmd = [
        'java', '-jar', jar_path,
        repo_dir,
        'true',      # usar JARs
        '0',         # max files per partition = automático
        'true',      # extrair métricas de variáveis e campos
        output_dir + os.sep
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=300)
        print(f"[✓] CK executado com sucesso para {repo_name}")
    except subprocess.CalledProcessError as e:
        print(f"[!] CK retornou erro para {repo_name}: {e.stderr}")
    except subprocess.TimeoutExpired:
        print(f"[!] Timeout ao executar CK para {repo_name} (>5min). Pulando...")

    # Mesmo com erro, tenta pegar arquivos gerados
    files = {
        'class': os.path.join(output_dir, 'class.csv'),
        'field': os.path.join(output_dir, 'field.csv'),
        'method': os.path.join(output_dir, 'method.csv'),
        'variable': os.path.join(output_dir, 'variable.csv'),
    }

    # Filtra apenas arquivos existentes E não vazios
    existing_files = {}
    for k, v in files.items():
        if os.path.exists(v) and os.path.getsize(v) > 1:  # Arquivo existe e tem mais que 1 byte
            try:
                # Testa se o arquivo pode ser lido pelo pandas
                test_df = pd.read_csv(v, nrows=0)  # Lê apenas o header
                existing_files[k] = v
                print(f"[✓] Arquivo {k}.csv válido para {repo_name}")
            except Exception as csv_error:
                print(f"[!] Arquivo {k}.csv corrompido para {repo_name}: {csv_error}")
        else:
            print(f"[!] Arquivo {k}.csv não existe ou está vazio para {repo_name}")
    
    if not existing_files:
        print(f"[!] Nenhum CSV válido gerado para {repo_name}")
        return None

    return existing_files
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

def load_and_print_class_metrics(class_csv_path):
    """
    Carrega métricas por classe do CSV, seleciona colunas importantes e imprime as primeiras linhas.
    """
    print("\n[+] Lendo métricas por CLASSE ...")
    
    try:
        df_class = pd.read_csv(class_csv_path, encoding="utf-8", encoding_errors="ignore")
        
        if df_class.empty:
            print("[!] Arquivo class.csv está vazio")
            return
            
        print(f"[+] Encontradas {len(df_class)} classes")
        
        # Colunas baseadas no class.csv
        class_columns = [
            'file', 'class', 'type',

            # Acoplamento e dependência
            'cbo', 'cboModified', 'fanin', 'fanout',

            # Complexidade e herança
            'wmc', 'dit', 'noc', 'rfc',

            # Coesão
            'lcom', 'lcom*', 'tcc', 'lcc',

            # Quantidade de métodos e campos
            'totalMethodsQty', 'staticMethodsQty', 'publicMethodsQty', 'privateMethodsQty',
            'protectedMethodsQty', 'defaultMethodsQty', 'visibleMethodsQty', 'abstractMethodsQty',
            'finalMethodsQty', 'synchronizedMethodsQty', 'totalFieldsQty', 'staticFieldsQty',
            'publicFieldsQty', 'privateFieldsQty', 'protectedFieldsQty', 'defaultFieldsQty',
            'finalFieldsQty', 'synchronizedFieldsQty',

            # Uso e complexidade
            'nosi', 'loc', 'returnQty', 'loopQty', 'comparisonsQty', 'tryCatchQty', 'parenthesizedExpsQty',
            'stringLiteralsQty', 'numbersQty', 'assignmentsQty', 'mathOperationsQty', 'variablesQty',
            'maxNestedBlocksQty', 'anonymousClassesQty', 'innerClassesQty', 'lambdasQty',
            'uniqueWordsQty', 'modifiers', 'logStatementsQty'
        ]

        available_class_cols = [col for col in class_columns if col in df_class.columns]
        # print(df_class[available_class_cols].to_string(index=False))  # Sem índice numérico
        print(df_class[available_class_cols].head()) # Exibe as 5 primeiras linhas para visualização

    except pd.errors.EmptyDataError:
        print("[!] Arquivo class.csv está vazio ou corrompido")
    except Exception as e:
        print(f"[!] Erro ao ler class.csv: {e}")

def load_and_print_method_metrics(method_csv_path):
    """
    Carrega métricas por método do CSV, seleciona colunas importantes e imprime as primeiras linhas.
    """
    if not os.path.exists(method_csv_path):
        print("[!] method.csv não encontrado.")
        return

    print("\n[+] Lendo métricas por MÉTODO ...")
    df_method = pd.read_csv(method_csv_path, encoding="utf-8", encoding_errors="ignore")

    # Colunas baseadas no method.csv
    method_columns = [
        'file', 'class', 'method', 'constructor', 'line',

        # Acoplamento e dependência
        'cbo', 'cboModified', 'fanin', 'fanout',

        # Complexidade e herança
        'wmc', 'rfc', 'loc',

        # Uso e complexidade
        'returnsQty', 'variablesQty', 'parametersQty', 'methodsInvokedQty',
        'methodsInvokedLocalQty', 'methodsInvokedIndirectLocalQty',

        # Estruturas de controle
        'loopQty', 'comparisonsQty', 'tryCatchQty', 'parenthesizedExpsQty',

        # Literais, operadores e variáveis
        'stringLiteralsQty', 'numbersQty', 'assignmentsQty', 'mathOperationsQty',

        # Estruturas internas
        'maxNestedBlocksQty', 'anonymousClassesQty', 'innerClassesQty', 'lambdasQty',

        # Semântica e modificadores
        'uniqueWordsQty', 'modifiers', 'logStatementsQty', 'hasJavaDoc'
    ]

    available_method_cols = [col for col in method_columns if col in df_method.columns]
    # print(df_method[available_method_cols].to_string(index=False))  # Sem índice numérico
    print(df_method[available_method_cols].head()) # Exibe as 5 primeiras linhas para visualização

def load_and_print_field_metrics(field_csv_path):
    """
    Carrega métricas por campo do CSV e imprime as primeiras linhas.
    """
    if not os.path.exists(field_csv_path):
        print("[!] field.csv não encontrado.")
        return

    print("\n[+] Lendo métricas por CAMPO ...")
    df_field = pd.read_csv(field_csv_path, encoding="utf-8", encoding_errors="ignore")

    # Colunas conforme o field.csv
    field_columns = [
        'file', 'class', 'method', 'variable', 'usage'
    ]

    available_field_cols = [col for col in field_columns if col in df_field.columns]
    # print(df_field[available_field_cols].to_string(index=False))  # Sem índice numérico
    print(df_field[available_field_cols].head()) # Exibe as 5 primeiras linhas para visualização

def load_and_print_variable_metrics(variable_csv_path):
    """
    Carrega métricas por variável do CSV e imprime as primeiras linhas.
    """
    if not os.path.exists(variable_csv_path):
        print("[!] variable.csv não encontrado.")
        return

    print("\n[+] Lendo métricas por VARIÁVEL ...")
    df_variable = pd.read_csv(variable_csv_path, encoding="utf-8", encoding_errors="ignore")

    # Colunas conforme o variable.csv
    variable_columns = [
        'file', 'class', 'method', 'variable', 'usage'
    ]

    available_variable_cols = [col for col in variable_columns if col in df_variable.columns]
    # print(df_variable[available_variable_cols].to_string(index=False))  # Sem índice numérico
    print(df_variable[available_variable_cols].head()) # Exibe as 5 primeiras linhas para visualização 


def main():
    print("== CK Metrics Extractor ==")
    readCsv_repo_url = pd.read_csv("top_java_repos.csv")

    total_repos = len(readCsv_repo_url)
    start_time = time.time()
    repo_times = []
    success_count = 0

    for idx, row in readCsv_repo_url.iterrows():
        repo_start = time.time()
        repo_url = row['url']
        repo_name = row['name']

        processed = idx + 1
        if repo_times:
            avg_time = sum(repo_times) / len(repo_times)
            remaining = (total_repos - processed) * avg_time
            eta = str(timedelta(seconds=int(remaining)))
        else:
            eta = "calculando..."

        print(f"\n[📦 {processed}/{total_repos}] Usando repositório: {repo_name} ({repo_url})")
        print(f"   ⏳ Estimativa de tempo restante: {eta}")

        # verificação antes de processar
        output_dir = os.path.join("ck_output", repo_name.replace("/", "_"))
        if os.path.exists(output_dir) and any(
            os.path.exists(os.path.join(output_dir, f"{f}.csv")) 
            for f in ["class", "method", "field", "variable"]
        ):
            print(f"[⏭️] Repositório {repo_name} já processado. Pulando...")
            continue

        ck_jar_path = os.path.join("ck", "target", "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar")
        if not os.path.exists(ck_jar_path):
            print(f"Erro: {ck_jar_path} não encontrado.")
            sys.exit(1)

        repo_path = clone_repo(repo_url)

        try:
            csv_paths = run_ck(ck_jar_path, repo_path, repo_name)
        except Exception as e:
            print(f"[!] Falha ao rodar CK no repositório {repo_name}. Pulando. Erro: {e}")
            continue

        if not csv_paths:
            print(f"[!] Nenhum arquivo CSV válido gerado para {repo_name}. Pulando.")
            continue

        # Imprime métricas já existentes
        if 'class' in csv_paths:
            load_and_print_class_metrics(csv_paths['class'])
        if 'method' in csv_paths:
            load_and_print_method_metrics(csv_paths['method'])
        if 'field' in csv_paths:
            load_and_print_field_metrics(csv_paths['field'])
        if 'variable' in csv_paths:
            load_and_print_variable_metrics(csv_paths['variable'])

        # Gera CSV separado com contagem de comentários por classe (não modifica arquivos do CK)
        try:
            if 'class' in csv_paths:
                output_dir = os.path.join("ck_output", repo_name.replace("/", "_"))
                generate_comments_by_class(repo_path, csv_paths['class'], output_dir)
        except Exception as e:
            print(f"[!] Falha ao gerar CSV de comentários para {repo_name}: {e}")

        success_count += 1
        repo_duration = time.time() - repo_start
        repo_times.append(repo_duration)

        print(f"   ✅ Finalizado em: {str(timedelta(seconds=int(repo_duration)))}.")

    total_duration = time.time() - start_time
    print("\n=== Processo concluído ===")
    print(f"Tempo total de execução: {str(timedelta(seconds=int(total_duration)))}")
    print(f"Repositórios com CK processados: {success_count}/{total_repos}")
    print(f"Repositórios com CK falhados: {total_repos - success_count}/{total_repos}")

if __name__ == "__main__":
    main()

# Baixe o CK Tool e monte o JAR file (ck/target/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar):
# git clone https://github.com/mauricioaniche/ck.git
# cd ck
# mvn clean package
# Documentação: https://github.com/mauricioaniche/ck

# Instale as dependências necessárias deste projeto:
# pip install gitpython pandas

# Execute o script:
# python ck_metrics.py
# Repo de exemplo: https://github.com/spring-projects/spring-petclinic