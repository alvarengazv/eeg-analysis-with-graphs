<a name="readme-topo"></a>

<div align='center'>
  <img src='#' width='350'>
</div>

<h1 align='center'>
  Aplicação da Teoria de Grafos na Análise de sinais de Eletroencefalograma (EEG)
</h1>

<div align='center'>

[![IDE][vscode-badge]][vscode-url]
[![Poetry][poetry-badge]][poetry-url]
[![Linguagem][python-badge]][python-url]

Algoritmos e Estruturas de Dados II

</div>

<details>
  <summary>
  <b style='font-size: 15px'>
    📑 Sumário
  </b>
  </summary>
  <ol>
    <li>
      <a href="#-Começando">🔨 Começando</a>
      <ul>
        <li><a href="#Pré-requisitos">Pré-requisitos</a></li>
        <li><a href="#Instalando">Instalando</a></li>
      </ul>
    </li>
    <li><a href="#-Ambiente-de-Compilação-e-Execução">🧪 Ambiente de Compilação e Execução</a></li>
    <li><a href="#-Contato">📨 Contato</a></li>
  </ol>
</details>

## 🔨 Começando

Nesta seção estão exemplificados os meios através dos quais se tornam possíveis a compilação e execução do programa apresentado.

### Pré-requisitos

Inicialmente, algumas considerações importantes sobre como se deve preparar o ambiente para compilar e executar o programa:

> [!NOTE]
> Recomenda-se usar uma distribuição de sistema operacional Linux ou o Windows Subsystem for Linux (WSL), pois a instalação abaixo foi baseada no funcionamento em um ambiente [_shell/bash_][bash-url].

Considerando um ambiente _shell_, garanta que os seguintes comandos já foram executados:
  - Atualize os pacotes antes da instalação dos compiladores:
  ```console
  sudo apt update
  ```
  - Instale a versão correta da linguagem `Python`: 
  ```console
  sudo apt-get install python3.12
  ```
  - Instale o gerenciador `pipx`, com os comandos:
  ```console
  sudo apt install pipx
  pipx ensurepath
  ```
  - Com o `pipx` instalado instale o [gerenciador de projetos `Poetry`](https://python-poetry.org/docs/):
  ```console
  pipx install poetry
  pipx upgrade poetry
  ```

### Instalando

Com o ambiente preparado, os seguintes passos são para a instalação, compilação e execução do programa localmente:

1. Clone o repositório no diretório desejado:
  ```console
  git clone https://github.com/alvarengazv/eeg-analysis-with-graphs.git
  cd eeg-analysis-with-graphs
  ```
2. Instale as dependências do projeto com o comando:
  ```console
  poetry install
  ```
3. Execute o arquivo `main.py` para gerar o arquivo .CSV dos nós (para isso, será necessário baixar a pasta derivatives que contém os dados .SET, diponíveis no [link](https://openneuro.org/datasets/ds004504/versions/1.0.8) e adicioná-la na pasta `datasets`), com o comando:
  ```console
  poetry run python src/main.py
  ```
2. Execute o arquivo `generate-edges.py` para gerar o arquivo .CSV das arestas, com o comando:
  ```console
  poetry run python src/generate-edges.py
  ```
3. Execute o arquivo `find-communities-louvain.py` para gerar as imagens .PNG dos grafos com as comunidades encontradas pelo método de Louvain e gráficos gerados para análise, com o comando:
  ```console
  poetry run python src/find-communities-louvain.py
  ```
4. Opcionalmente, pode-se acessar o arquivo `grafos-eeg.gephi` para visualizar os grafos gerados no software Gephi. Para tal, é necessário instalar o software Gephi, disponível no [link](https://gephi.org/).
  
O programa estará pronto para ser testado.

<p align="right">(<a href="#readme-topo">voltar ao topo</a>)</p>

## 🧪 Ambiente de Compilação e Execução

> [!IMPORTANT] 
> Para que os testes tenham validade, considere as especificações técnicas do computador utilizado

O trabalho foi desenvolvido, compilado e executado no ambiente com as configurações especificadas no quadro abaixo:

<div align='center'>

![Ubuntu][ubuntu-badge]
![Ryzen][ryzen5500-badge]
![Lenovo][lenovo-badge]

SO | Linguagem | Gerenciador de Depêndencias/Pacotes | CPU | RAM | Dispositivo de Armazenamento 
--- | --- | --- | --- | --- | ---
Ubuntu 22.04.4 LTS | Python 3.12.3 | Poetry (version 1.8.3) | Ryzen 5 5500U 2.1GHz | 2x4GB 3200MHz | SSD M.2 NVME 256GB (3500MB/s de Leitura x 1200MB/s de Escrita) 

</div>

<p align="right">(<a href="#readme-topo">voltar ao topo</a>)</p>

## 📨 Contato

<div align="center">
   <i>Guilherme Alvarenga de Azevedo - Graduando - 4º Período de Engenharia de Computação @ CEFET-MG</i>
<br><br>

[![Gmail][gmail-badge]][gmail-autor2]
[![Linkedin][linkedin-badge]][linkedin-autor2]
[![Telegram][telegram-badge]][telegram-autor2]
</div>

<p align="right">(<a href="#readme-topo">voltar ao topo</a>)</p>

[vscode-badge]: https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white
[vscode-url]: https://code.visualstudio.com/docs/?dv=linux64_deb
[make-badge]: https://img.shields.io/badge/_-MAKEFILE-427819.svg?style=for-the-badge
[make-url]: https://www.gnu.org/software/make/manual/make.html
[python-badge]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[python-url]: https://www.python.org/
[poetry-badge]: https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D
[poetry-url]: https://python-poetry.org/
[trabalho-url]: https://drive.google.com/file/d/1m3pVwTmCQPWp7HDzCqwcy_aB0x4A3yIx/view?usp=sharing
[github-prof]: https://github.com/mpiress
[medias-ref]: output/csv/medias.csv
[mediasFlag-ref]: output/csv/mediasComFlag.csv
[mediasPC-ref]: output/csv/mediasPC.csv
[graficoAO-ref]: output/img/graficoComparacaoAlgoritmosPorOrdem.png
[graficoOA-ref]: output/img/graficoComparacaoOrdensPorAlgoritmo.png
[graficoAOFlag-ref]: output/img/graficoComparacaoAlgoritmosPorOrdemComFlag.png
[graficoOAFlag-ref]: output/img/graficoComparacaoOrdensPorAlgoritmoComFlag.png
[graficoAOPC-ref]: output/img/graficoComparacaoAlgoritmosPorOrdemPC.png
[graficoOAPC-ref]: output/img/graficoComparacaoOrdensPorAlgoritmoPC.png
[main-ref]: src/main.cpp
[hppAMM-ref]: src/minMax.hpp
[cppAMM-ref]: src/minMax.cpp
[gnuAMM-ref]: src/mediasMinMax.p
[branchAMM-url]: https://github.com/alvarengazv/trabalhosAEDS1/tree/AlgoritmosMinMax
[makefile]: ./makefile
[bash-url]: https://www.hostgator.com.br/blog/o-que-e-bash/
[lenovo-badge]: https://img.shields.io/badge/lenovo%20laptop-E2231A?style=for-the-badge&logo=lenovo&logoColor=white
[ubuntu-badge]: https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white
[ryzen5500-badge]: https://img.shields.io/badge/AMD%20Ryzen_5_5500U-ED1C24?style=for-the-badge&logo=amd&logoColor=white
[ryzen3500-badge]: https://img.shields.io/badge/AMD%20Ryzen_5_3500X-ED1C24?style=for-the-badge&logo=amd&logoColor=white
[windows-badge]: https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white
[linkedin-autor1]: https://www.linkedin.com/in/%C3%A9lcio-amorim-0210532a2/
[telegram-autor1]: https://t.me/
[gmail-autor1]: mailto:elcioamorim12@gmail.com
[linkedin-autor2]: https://www.linkedin.com/in/guilherme-alvarenga-de-azevedo-959474201/
[telegram-autor2]: https://t.me/alvarengazv
[gmail-autor2]: mailto:gui.alvarengas234@gmail.com
[linkedin-autor3]: https://www.linkedin.com/in/jo%C3%A3o-paulo-cunha-faria-219584270/
[gmail-autor3]: mailto:joaopaulofaria98@gmail.com
[linkedin-badge]: https://img.shields.io/badge/-LinkedIn-0077B5?style=for-the-badge&logo=Linkedin&logoColor=white
[telegram-badge]: https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white
[gmail-badge]: https://img.shields.io/badge/-Gmail-D14836?style=for-the-badge&logo=Gmail&logoColor=white
[tupla-url]: https://www.ic.unicamp.br/~raquel.cabral/pdf/Aula15.pdf
[java-tutorial]: https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/How-do-I-install-Java-on-Ubuntu
