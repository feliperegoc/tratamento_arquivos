# Processador de Arquivos CSV em Larga Escala

Este é um script Python desenvolvido para processar grandes arquivos CSV, realizando transformações de texto e otimizando o uso de memória através do processamento em chunks. O script realiza normalizações como remoção de acentos e padronização de texto.

## 🚀 Funcionalidades

- Processamento de arquivos CSV de grande porte
- Transformação de texto (remoção de acentos, conversão para maiúsculas)
- Processamento em chunks para otimização de memória
- Processamento de múltiplos diretórios
- Barra de progresso para acompanhamento do processamento
- Tamanho de chunk adaptativo baseado no tamanho do arquivo

## 📋 Pré-requisitos

- Python 3.6 ou superior
- pip (gerenciador de pacotes Python)

## 📦 Bibliotecas Necessárias

```bash
pip install pandas
pip install unidecode
pip install tqdm
```

## ⚙️ Configuração

1. No exemplo do código, os diretórios processados são:
   - Cnaes
   - Empresas
   - Estabelecimentos
   - Motivos
   - Municipios
   - Naturezas
   - Paises
   - Qualificacoes
   - Simples
   - Socios

   Nota: Estes diretórios são apenas exemplos do caso de uso específico. Você pode adaptar o código para processar qualquer estrutura de diretórios conforme sua necessidade.

2. Ajuste o caminho base no script conforme sua necessidade:
```python
base_dir = r"C:\seu\caminho\aqui"
```

## 🚀 Uso

1. Execute o script principal:
```bash
python app.py
```

2. O script irá:
   - Processar todos os diretórios configurados
   - Criar diretórios "_Processados" para cada pasta de entrada
   - Mostrar o progresso do processamento em tempo real
   - Gerar relatórios de sucesso/falha para cada arquivo

## 📊 Estrutura do Projeto

```
├── app.py               # Script principal
└── diretórios_entrada/  # Seus diretórios com arquivos CSV
    ├── DiretorioA/
    ├── DiretorioB/
    └── ...
```

## 🔍 Detalhes Técnicos

- Encoding: Configurável conforme necessidade (no exemplo usa-se latin1)
- Separador CSV: ponto e vírgula (;)
- Processamento em chunks para otimização de memória
- Tamanho do chunk adaptativo baseado no tamanho do arquivo:
  - < 250MB: 25.000 linhas
  - < 500MB: 50.000 linhas
  - < 1GB: 100.000 linhas
  - E assim por diante...

## 📝 Transformações Aplicadas

Cada linha do arquivo passa pelas seguintes transformações:
1. Remoção de acentos
2. Conversão para maiúsculas
3. Normalização de espaços múltiplos

## ⚠️ Observações Importantes

- Certifique-se de ter espaço em disco suficiente para os arquivos processados
- O script substitui arquivos de saída existentes
- Em caso de erro durante o processamento, o arquivo específico é marcado como falha e o script continua com os próximos
- O encoding e a estrutura de diretórios podem ser adaptados conforme sua necessidade específica