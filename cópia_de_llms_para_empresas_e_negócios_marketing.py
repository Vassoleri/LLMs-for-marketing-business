# -*- coding: utf-8 -*-

# Projeto para Departamento de Marketing

Nosso objetivo com esse projeto é criar um assistente de geração de conteúdo automatizado, que adapta o texto ao público e ao canal de divulgação. Confira os slides para mais detalhes sobre a proposta desse estudo de caso.


> **Importante:** Caso dê algum erro no processo de instalação e que impeça de prosseguir com a execução do código, confira o Colab da aula e verifique se fez uma cópia do mais atualizado, pois atualizaremos essas etapas de instalação com os comandos atualizados (caso seja necessária alguma mudança no comando de instalação).

Vamos usar primeiro o ipynb no Colab para desenvolver e validar a lógica com LLMs, onde aprenderemos a deixar uma aplicação funcional dentro do próprio Colab usando ipywidgets. Ao final, veremos como adaptar isso para uma interface profissional usando o framework Streamlit, pronto para publicar. Isso evita retrabalho, ajuda a testar ideias com rapidez e foca primeiro no que importa: o núcleo funcional, a lógica e conceitos.

## Instalação das bibliotecas

Abaixo instalaremos algumas bibliotecas essenciais para o desenvolvimento de nosso projeto.

Para instalação usaremos o comando pip install. Passaremos o parâmetro -q (quiet) para reduzir a verbosidade da saída no terminal, exibindo apenas erros e mensagens essenciais. É usado para simplificar a visualização durante instalações automatizadas ou em ambientes onde logs detalhados não são necessários.
"""

!pip install -q "requests==2.32.4" langchain-community langchain-groq ipywidgets

"""### Importar bibliotecas  

"""

from google.colab import widgets
import ipywidgets as widgets

from langchain_groq import ChatGroq
import os
import getpass

"""# Criação dos campos - Interface

Antes de partirmos para o código, é importante definirmos com clareza os campos que a aplicação irá utilizar. Essa etapa é essencial para evitar dispersão e garantir que o desenvolvimento seja focado nas necessidades reais da empresa.

> Campos *(conforme discutido na apresentação do estudo de caso)*
 * Plataforma de destino (ex: Blog, Instagram, LinkedIn, E-mail)
 * Tom da mensagem (ex: Informativo, Inspirador, Urgente, Informal)
 * Comprimento do texto (ex: Curto, Médio, Longo)
 * Tema ou tópico (ex: alimentação, saúde mental, exames de rotina, cuidados, etc.)
 * Público-alvo (Jovens adultos, Famílias, Idosos, Geral, etc.)
 * Opções adicionais:
  * Incluir chamada para ação (ex: “Agendar consulta” ou “Converse com um especialista”)
  * Retornar hashtags
  * Inserir palavras-chave para incluir no meio do texto


Vamos começar criando um campo em formato de texto. O `widgets.Text` cria um campo livre para digitação, onde o usuário insere o conteúdo manualmente.

* `description`: texto que aparece como rótulo do campo (ajuda a identificar sua função).
* `placeholder`: texto que aparece dentro do campo antes do preenchimento, como sugestão ou exemplo. Vamos aproveitar para colocar uma sugestão já do que o usuário pode digitar, o que é uma boa prática de user experience (UX)

Obs: Pensando nas boas práticas, também vamos aproveitar para definir os nomes das variáveis em inglês (tema vai ser *topic*, público-alvo vai ser *audience*, etc.)


"""

topic = widgets.Text(
    description = 'Tema:',
    placeholder = 'Ex: saúde mental, alimentação saudável, prevenção, etc.'
)

"""### Exibindo o widget

Para exibir os campos/widgets que criamos vamos usar o método display(). Com isso o campo vai aparecer dentro da saída do bloco de código abaixo, assim exibindo tudo de forma interativa dentro desse notebook.
"""

display(topic)

topic.value

"""### Ajustando propriedades do campo

Por padrão, o widget Text do ipywidgets cria um campo de entrada relativamente estreito, o que pode não ser ideal quando esperamos que o usuário digite frases ou trechos mais longos.

Com `layout=widgets.Layout(width='500px')` definimos explicitamente a largura do campo como 500 pixels, o que é mais apropriado quando esperamos frases completas.

* Você pode ajustar esse valor conforme a necessidade - ex: '100%' para ocupar toda a largura do container (deixando responsivo), ou '700px' para um campo ainda maior.

"""

topic = widgets.Text(
    description = 'Tema:',
    placeholder = 'Ex: saúde mental, alimentação saudável, prevenção, etc.',
    layout = widgets.Layout(width='500px')
)
display(topic)

"""### Outros formatos de campos

Para adicionar campos de seleção práticos e dinâmicos à nossa aplicação, utilizaremos a função widgets.Dropdown, que exibe opções em formato de lista suspensa. Passaremos as escolhas disponíveis através do parâmetro options e, para otimizar a interface e facilitar futuras alterações, definiremos uma largura padrão para esses campos usando uma variável, permitindo ajustes globais de tamanho de forma simples, o que pode ser muito útil caso os valores pré-definidos sejam extensos.

"""

w_dropdown = '250px'

platform = widgets.Dropdown(
    options = ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'],
    description = 'Plataforma',
    layout = widgets.Layout(width = w_dropdown)
)

tone = widgets.Dropdown(
    options=['Normal', 'Informativo', 'Inspirador', 'Urgente', 'Informal'],
    description='Tom:',
    layout=widgets.Layout(width=w_dropdown)
)

length = widgets.Dropdown(
    options=['Curto', 'Médio', 'Longo'],
    description='Tamanho:',
    layout=widgets.Layout(width=w_dropdown)
)

audience = widgets.Dropdown(
    options=['Geral', 'Jovens adultos', 'Famílias', 'Idosos', 'Adolescentes'],
    description='Público-alvo:',
    layout=widgets.Layout(width=w_dropdown)
)


display(platform, tone, length, audience)

platform.value

"""Para incorporar opções de ativar/desativar funcionalidades, como incluir uma Chamada para Ação (CTA) ou solicitar sugestões de hashtags, utilizaremos widgets.Checkbox.

Estes campos booleanos (Verdadeiro/Falso) serão configurados com um valor inicial (por padrão, desmarcado) e uma descrição clara de sua função, permitindo ao usuário controlar facilmente aspectos específicos da geração de conteúdo.
"""

cta = widgets.Checkbox(
    value = False,
    description = 'Incluir CTA'
)

hashtags = widgets.Checkbox(
    value=False,
    description='Retornar Hashtags',
)

display(cta)

cta.value

"""Para permitir a inserção de textos mais longos, como listas de palavras-chave para SEO, implementaremos um campo do tipo Textarea. Este campo opcional dará ao usuário a flexibilidade de especificar termos que a IA deve incorporar naturalmente ao conteúdo, e seu tamanho pode ser ajustado em largura e altura para melhor acomodar o texto inserido, utilizando `widgets.Layout` para definir dimensões como height."""

keywords = widgets.Textarea(
    description = 'Palavras-chave (SEO)',
    placeholder = 'Ex: bem-estar, medicina preventiva...',
    layout = widgets.Layout(width = '500px', height = '50px')
)

display(keywords)

"""## Criando o botão de geração

Vamos agora adicionar um botão à interface. Esse botão será clicado para gerar o conteúdo com base nos campos preenchidos. O parâmetro description aqui é o texto que aparece no botão.

"""

generate_button = widgets.Button(
    description = 'Gerar conteúdo',
)

display(generate_button)

"""## Exibição do resultado

Precisamos criar um espaço para exibir o output, que é o resultado gerado pela LLM.

Usamos o Output() para mostrar o resultado da geração de conteúdo. Ele cria uma “área de resposta”, onde vamos exibir o conteúdo gerado. Tudo que for mostrado com display() ou print() dentro dele aparecerá aqui.

"""

output = widgets.Output()

"""### Definindo ação do botão

Por enquanto o botão não faz nada, precisamos criar uma função que será executada quando ele for clicado.

Explicando os parâmetros:

* `b` é o próprio botão sendo passado como argumento (padrão do on_click).

* `with output`: garante que tudo dentro desse bloco apareça na área de saída.

* `clear_output()` limpa o resultado anterior, evitando sobreposição de textos.

"""

def generate_result(b):
  with output:
    output.clear_output()
    print("Ok!")

"""**Ligando o botão à função**

`.on_click()` define que nossa função será executada quando o botão for pressionado
"""

generate_button.on_click(generate_result)

"""**Testando**

Execute o bloco de código abaixo e clique no botão para verificar se nosso método está funcionando.
"""

display(generate_button, output)

"""## Exibindo os campos juntos na interface

Por fim, precisamos organizar os campos e exibi-los num layout final junto ao botão.
Antes de chamarmos a função display (para exibir tudo de forma interativa dentro desse notebook) vamos usar a função `VBox()`, para organizar os elementos na vertical, na ordem em que forem listados.

E para evitar a repetição, coloque dentro de uma função chamada "create_form", que retorne esse VBox com os widgets. Assim seu código fica mais limpo e reutilizável, pois usaremos mais tarde esses campos novamente
"""

def create_form():
  return widgets.VBox([
      topic,
      platform,
      tone,
      length,
      audience,
      cta,
      hashtags,
      keywords,
      generate_button,
      output
  ])

form = create_form()

display(form)

"""# Conectando com a LLM

Para integrar a LLM à nossa aplicação, precisamos definir o modelo e a forma de implementação, que pode ser via download (para modelos open source, garantindo execução local e privacidade) ou através de API (simplificando a integração, oferecendo boa performance em qualquer máquina, mas com processamento de dados em servidores externos).

## Escolhendo o modelo

Na fase inicial de testes, recomenda-se começar com um modelo open source acessível via API gratuita, o que simplifica a implementação e reduz custos. Mesmo após a aplicação estar funcionando, esses modelos seguem vantajosos pela flexibilidade e economia. Neste curso, iniciaremos com o uso via API para evitar a complexidade da configuração local. Mais adiante, ensinaremos como rodar modelos localmente, permitindo que você compare as abordagens e escolha a mais adequada ao seu caso.

Usaremos a biblioteca LangChain para integrar com a Groq, aproveitando seu módulo nativo de conexão e os benefícios que ela oferece no desenvolvimento.

Para escolher bons modelos, recomendamos consultar leaderboards comparativos, como:
 * o https://lmarena.ai/?leaderboard
 * ou ranking específico para português na Hugging Face - https://huggingface.co/spaces/eduagarcia/open_pt_llm_leaderboard

**Adicionando a key**

Antes de começar com o código, você deve colar no campo a sua key gerada dentro do painel do Groq: https://console.groq.com/keys
"""

os.environ["GROQ_API_KEY"] = getpass.getpass()

"""Lembre-se que não precisamos pagar para usar modelos disponibilizados gratuitamente pelo provedor.

* Essa próxima linha usa o método ChatGroq para configuração do modelo via API do Groq.

* Escolhemos um modelo gratuito, dentro da aba *free tier* https://console.groq.com/docs/rate-limits. Copie o ID do modelo e adicione no campo a seguir


"""

id_model = "llama-3.1-8b-instant" #@param {type: "string"}

llm = ChatGroq(
    model = id_model,
    temperature = 0.7,
    max_tokens=None,
    timeout = None,
    max_retries = 2,
)

"""### Explicações do método

Para este teste definimos a temperatura como 0.7.
A temperatura é um hiperparâmetro que ajusta a aleatoriedade da resposta da LLM.

* Temperaturas mais altas (0.8-1.0) geram saídas mais criativas, ideais para brainstorming, enquanto temperaturas baixas (0.0-0.4) produzem respostas mais focadas e determinísticas, adequadas para tarefas técnicas;
* valores médios (0.5-0.7) oferecem um equilíbrio, sendo um bom ponto de partida para geração de conteúdo geral, embora seja recomendável experimentar diferentes valores conforme o objetivo e o modelo.
Além da temperatura, outros parâmetros como max_tokens (limite de tokens), timeout (tempo máximo de resposta) e max_retries (tentativas em caso de falha) podem ser configurados para otimizar o comportamento da LLM, com a documentação da LangChain para Groq oferecendo detalhes sobre todas as opções disponíveis.

https://python.langchain.com/api_reference/groq/chat_models/langchain_groq.chat_models.ChatGroq.html

### Formato das mensagens

Ao interagir com a LLM, estruturamos o prompt como uma troca de mensagens, cada uma com uma função (ou *role*, como "human" para nossa entrada e "system" para instruções gerais que garantem consistência) e um conteúdo (a mensagem em si, seja texto ou dados estruturados).

O prompt de sistema é crucial para definir o comportamento base da LLM, como atribuir um papel ou instruções padrão, e embora um prompt genérico possa funcionar, um prompt de sistema específico para a aplicação melhora significativamente a consistência dos resultados.
"""

prompt = "Olá! Quem é você?" # @param {type:"string"}

template = [
    ("system", "Você é um redator profissional."),
    ("human", prompt)
]

res = llm.invoke(template)
res

prompt = "Olá! Quem é você?" # @param {type:"string"}

template = [
    ("system", "Você é um redator profissional."),
    ("human", prompt)
]

res = llm.invoke(template)
res

res.content

"""**Usando com método de template do LangChain**

Para criar prompts dinâmicos e organizados, especialmente em aplicações maiores e reutilizáveis com LangChain, utilizamos `ChatPromptTemplate.from_messages()`, que permite inserir de forma organizada variáveis (como {input}) e separar a lógica do prompt, tornando o código mais limpo e escalável.

Em vez de invocar a LLM diretamente, criamos uma "chain" que combina este template de prompt com o modelo.

> Para contextualizar, o que são **chains**: Chain do LangChain (Corrente, Cadeias ou ainda Sequencias) é uma composição de etapas que processam dados em sequência — aqui, a entrada é formatada pelo prompt e enviada ao modelo. A vantagem é que chains permitem combinar várias ações (como formatar, gerar, filtrar, armazenar) de forma modular e reutilizável, facilitando aplicações mais robustas. Elas funcionam ao encadear componentes, onde a saída de um se torna a entrada do próximo, criando uma sequência lógica de operações.
"""

from langchain_core.prompts import ChatPromptTemplate

prompt = "Olá! quem é você?"  # @param {type:"string"}

template = ChatPromptTemplate.from_messages([
    ("system", "Você é um redator profissional"),
    ("human", "{prompt}")
])

chain = template | llm

res = chain.invoke({"prompt": prompt})
res.content

"""### Estendendo a chain / Output parser

Para trabalhar com a saída de sequência "crua" da mensagem, Langchain oferece "Output Parsers", como o StrOutputParser, que processa a saída do modelo em um formato mais acessível, convertendo-a em uma string.

Se o modelo (LLM) já produz uma string, o StrOutputParser simplesmente a repassa; se for um ChatModel que produz uma mensagem, ele extrai o conteúdo do atributo `.content`. Embora res.content possa ser usado diretamente no caso de modelos LLM que já retornam string, incluir o StrOutputParser na chain é uma boa prática para obter o valor string diretamente, tornando-se especialmente útil ao integrar ChatModels.


"""

from langchain_core.output_parsers import StrOutputParser

prompt = "Olá! quem é você?"  # @param {type:"string"}

template = ChatPromptTemplate.from_messages([
    ("system", "Você é um redator profissional"),
    ("human", "{prompt}")
])

chain = template | llm | StrOutputParser()

res = chain.invoke({"prompt": prompt})
res

"""## Melhorando a exibição do resultado

Note acima que o resultado não ficou tão apresentável no Colab, podemos melhorar a sua visualização usando **Markdown**.
* Markdown é uma linguagem de marcação simples e leve que facilita a formatação de texto usando símbolos como asteriscos e hashtags, sem precisar de HTML. No Google Colab, ele melhora a organização e a legibilidade, permitindo destacar textos em *itálico* , **negrito** e criar títulos com #, ## ou ### para diferentes níveis.

* Caso queira explorar mais, aqui está um guia da sintaxe: https://www.markdownguide.org/basic-syntax/

"""

def show_res(res):
  from IPython.display import Markdown
  display(Markdown(res))

show_res(res)

"""## Juntando em uma função

Reunir tudo em uma função facilita a reutilização, organização e manutenção do código, evitando repetições durante nossos testes. Vamos chamar essa função no bloco de código seguinte

"""

def llm_generate(llm, prompt):
  template = ChatPromptTemplate.from_messages([
      ("system", "Você é um redator profissional."),
      ("human", "{prompt}"),
  ])

  chain = template | llm | StrOutputParser()

  res = chain.invoke({"prompt": prompt})
  show_res(res)

prompt = "escreva 5 dicas de saúde"  # @param {type:"string"}

llm_generate(llm, prompt)

"""### Outros Modelos Open Source


 * Modelos disponíveis pelo Groq https://console.groq.com/docs/rate-limits (ver os gratuitos - dentro da aba *free tier*)

 Durante a fase de experimentação é uma boa ideia testar diferentes modelos.

Após validar a nossa solução e fazer os testes iniciais, você pode optar também por modelos pagos e proprietários quando o modelo estiver em produção, já que agora não estará mais desperdiçando alguns centavos de dólar em testes.

### Modelos proprietários (exemplo: ChatGPT da OpenAI)

Recomenda-se iniciar os testes com modelos open source e, após a validação, migrar para soluções pagas, como ChatGPT (OpenAI) ou Claude (Anthropic), para evitar custos desnecessários durante o desenvolvimento.

Soluções pagas oferecem modelos de ponta com alta performance e suporte via API, ideais para robustez e facilidade, mas o custo escala com o uso de tokens (segmentos de texto processados); em contraste, modelos open source, executáveis localmente ou em servidores próprios, proporcionam maior controle, privacidade e custo reduzido para larga escala, exigindo, no entanto, mais conhecimento técnico para configuração e manutenção.

A decisão entre API paga e open source deve considerar o volume de uso esperado e a necessidade de personalização.

Para testar a implementação, faremos um exemplo com o ChatGPT, lembrando que os custos da OpenAI são baseados em tokens (consulte openai.com/api/pricing/).

A grande vantagem de usar LangChain é que toda a sintaxe e lógica de chains criadas são reaproveitáveis, alterando-se apenas a forma como a LLM é carregada, enquanto o restante da aplicação permanece o mesmo.

* Valores: https://openai.com/api/pricing/

> Como gerar uma API key

Para utilizar os modelos da OpenAI, é necessário obter uma chave de API. Siga as etapas abaixo para gerar a sua:

1. Acesse o site da OpenAI e faça login na sua conta.
2. Navegue até a seção de chaves de API e clique em "Criar nova chave secreta" - https://platform.openai.com/api-keys
3. Copie a chave gerada e armazene-a em um local seguro. Importante: nunca compartilhe sua chave

> Conferir o uso https://platform.openai.com/usage
"""

!pip install -q langchain-openai

os.environ["OPENAI_API_KEY"] = getpass.getpass()

# https://platform.openai.com/docs/models
from langchain_openai import ChatOpenAI
chatgpt = ChatOpenAI(model = "gpt-4.1-mini")

chatgpt = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2
)

chain_chatgpt = template | chatgpt

res = chain_chatgpt.invoke({"prompt": "Gere um texto de 2 parágrafos sobre dicas de saúde"})
show_res(res.content)

"""# Construindo o prompt de aplicação

Agora que já interagimos com o modelo de forma básica, vamos começar a explorar a **engenharia de prompt**. Isso significa aprender a formular perguntas ou instruções de forma clara e específica para obter respostas mais precisas e úteis.

### Estrutura de um prompt

Existem várias técnicas de engenharia de prompt, onde muitas delas se baseiam em princípios parecidos. Uma abordagem simples para construir um prompt mais completo é adicionar a ele alguns 'blocos' (componentes), que no caso seriam:
* Papel (Role) - "quem" ele deve interpretar (mais sobre isso abaixo)
* Tarefa (Task) - tarefa que deve realizar
* Entrada (Input) - informação que pode ser usada como contexto para gerar uma resposta (por exemplo o faturamento mensal de uma empresa, ou um dado específico sobre algo ou alguém)
* Saída (Output) - como quer que seja o resultado. Podemos especificar também regras, como como tamanho do resultado (medido em quantidade de palavras ou parágrafos por exemplo)
* Restrições (Constraints) - o que queremos evitar na resposta. Por exemplo: "evite jargões ou linguagem muito técnica". "Não inclua sua análise ou opinião".

### Interpretação de papéis - Role Prompting

A técnica de role prompting consiste em instruir o modelo de IA a assumir um papel específico, como um especialista em determinada área (o modo mais comum, conhecido como "O Especialista", para obter explicações técnicas), uma figura histórica ou um personagem fictício, o que influencia significativamente o estilo e o conteúdo da resposta, mesmo que o restante do prompt seja idêntico.

Utilizar frases como "Você é um redator" ou "Aja como um historiador" no prompt de sistema são exemplos práticos dessa técnica, que molda a persona da LLM para gerar resultados mais alinhados com o contexto desejado.
"""

prompt = "fale sobre chocolate em 1 parágrafo"

template = ChatPromptTemplate.from_messages([
    ("system", "Você é um historiador"),
    ("human", "{prompt}")
])

chain = template | llm | StrOutputParser()

res = chain.invoke({"prompt": prompt})
show_res(res)

"""Aqui vemos então como o tipo de especialista pode impactar totalmente no resultado. Portanto precisamos pedir algo que seja alinhado ao nosso propósito (copiamos o mesmo código do bloco acima, mudando apenas o prompt do system)"""

template = ChatPromptTemplate.from_messages([
    ("system", "Você é um especialista em marketing digital."),
    ("human", "{prompt}"),
])

chain = template | llm | StrOutputParser()

res = chain.invoke({"prompt": prompt})
show_res(res)

"""Ser mais específico geralmente é mais indicado. No contexto da nossa aplicação o prompt abaixo funciona melhor porque direciona o modelo não apenas para produzir textos bem escritos, mas com foco estratégico (como conversão, engajamento e SEO, que são essenciais em campanhas de marketing)."""

template = ChatPromptTemplate.from_messages([
    ("system", "Você é um especialista em marketing digital com foco em SEO e escrita persuasiva."),
    ("human", "{prompt}"),
])

chain = template | llm | StrOutputParser()

res = chain.invoke({"prompt": prompt})
show_res(res)

"""### Usando exemplos - One-Shot e Few-Shot Prompting

 * Zero-Shot – O modelo responde sem exemplos, confiando apenas no treinamento
 * One-Shot – Um exemplo é fornecido para orientar a resposta.
 * Few-Shot – Vários exemplos ajudam o modelo a reconhecer padrões e melhorar a precisão.


"""

assunto = 'chocolate'

one_shot = f"""
Exemplo:
Título: Você sabia que beber mais água pode melhorar sua concentração?
Texto: A desidratação leve já é suficiente para reduzir seu foco e energia no dia a dia. Mantenha uma garrafinha por perto e lembre-se de se hidratar ao longo do dia.
Hashtags: #hidratação #foconasaude

Agora gere um novo texto que fale sobre {assunto}
"""

#print(one_shot)

res = chain.invoke({"prompt": one_shot})
show_res(res)

"""O few-shot prompting, ou prompt com exemplos, demonstra à IA a estrutura, estilo e abordagem desejados para a resposta, como a inclusão de hashtags ou a formulação de títulos como perguntas, tornando o processo de instrução mais intuitivo e eficiente do que apenas fornecer instruções textuais. Embora exemplos possam ser combinados com texto para maior precisão, o few-shot prompting com múltiplos exemplos, como o que veremos a seguir, ajuda a IA a generalizar melhor o padrão esperado."""

few_shot = f"""
Exemplo 1:
Título: Você sabia que beber mais água pode melhorar sua concentração?
Texto: A desidratação leve já é suficiente para reduzir seu foco e energia no dia a dia. Mantenha uma garrafinha por perto e lembre-se de se hidratar ao longo do dia.
Hashtags: #hidratação #foconasaude

Exemplo 2:
Título: Comer carboidratos à noite engorda: Mito ou verdade?
Texto: Esse é um mito comum. O que realmente importa é o total calórico do dia e a qualidade dos alimentos. Com orientação certa, dá sim para comer bem à noite sem culpa!
Hashtags: #nutricaosemmitos #equilibrioalimentar

Agora gere um novo texto que fale sobre {assunto}
"""

res = chain.invoke({"prompt": few_shot})
show_res(res)

"""### Guiando o resultado com uma estrutura - Structured Prompting

Para o prompt final de nossa aplicação, usaremos também o conceito de Prompting estruturado (Structured Prompting), cuja premissa envolve a codificação cuidadosa de instruções, exemplos e restrições personalizadas para direcionar propositalmente comportamentos de modelos de linguagem para tarefas de um nicho específicos.


"""

form = create_form()
display(form)

prompt = f"""
Crie um post para {platform.value} com a seguinte estrutura:
1. Comece com uma pergunta provocativa.
2. Apresente um benefício claro relacionado ao tema.
3. Finalize com uma chamada para ação (CTA) encorajando o leitor a buscar mais informações.

Tema: {topic.value}
Público-alvo: {audience.value}
Tom: {tone.value}
"""

print(prompt)

res = chain.invoke({"prompt": prompt})
show_res(res)

"""Para dar mais liberdade à IA na escolha da estrutura do texto, especialmente considerando que a aplicação aceitará diversos parâmetros como plataforma e comprimento, optaremos por um prompt final dinâmico em vez de um structured prompting rígido, que seria mais adequado para resultados muito específicos e poderia levar a publicações repetitivas.

### Construindo o prompt final dinamicamente


Este prompt final será construído a partir das variáveis do formulário, organizado em itens legíveis com `-` para fácil modificação e escalabilidade.

Cada linha fornecerá instruções claras (canal, tom, público...), e opções como hashtags ou CTAs serão incluídas condicionalmente usando expressões inline em Python, adaptando o prompt às escolhas do usuário.

Adicionaremos também a instrução para garantir que a saída seja limpa e pronta para uso.


"""

prompt = f"""
Escreva um texto com SEO otimizado sobre o tema '{topic.value}'.
Retorne em sua resposta apenas o texto final.
- Onde será publicado: {platform.value}.
- Tom: {tone.value}.
- Público-alvo: {audience.value}.
- Comprimento: {length.value}.
- {"Inclua uma chamada para ação clara." if cta.value else "Não inclua chamada para ação"}
- {"Retorne ao final do texto hashtags relevantes." if hashtags.value else "Não inclua hashtags."}
{"- Palavras-chave que devem estar presentes nesse texto (para SEO): " + keywords.value if keywords.value else ""}
"""
print(prompt)

res = chain.invoke({"prompt": prompt})
show_res(res)

"""### Sobre o prompt e melhorias

Não existe um “melhor prompt” universal — o mais eficaz depende sempre do seu objetivo e do contexto da aplicação. A melhor forma de descobrir o que funciona é testando variações e analisando os resultados.

Para encontrar boas alternativas, você pode:

* Pesquisar por prompt books gratuitos disponíveis na internet

* Usar sites que reúnem templates prontos, como PromptHero ou FlowGPT

* Pedir sugestões diretamente à própria LLM (“Como posso melhorar esse prompt para torná-lo mais persuasivo?”)

* Analisar exemplos de prompts usados em casos reais ou estudos de caso

* Ajustar pequenos trechos do prompt e observar o impacto (tom, foco, estrutura)

* Extra: Combinar técnicas (por exemplo Structured Prompting com few-shot prompting) pode aprimorar ainda mais a qualidade e a relevância dos conteúdos gerados.

Essas estratégias ajudam a refinar continuamente a performance e alinhar melhor o conteúdo gerado aos seus objetivos.

# Concluindo a aplicação final

Agora que concluímos a criação do prompt final de nossa aplicação, podemos partir para a finalização.
Precisamos juntar os formulários ao prompt e à LLM.
"""

def llm_generate(llm, prompt):
  template = ChatPromptTemplate.from_messages([
      ("system", "Você é um especialista em marketing digital com foco em SEO e escrita persuasiva."),
      ("human", "{prompt}"),
  ])

  chain = template | llm | StrOutputParser()

  res = chain.invoke({"prompt": prompt})
  return res

def generate_result(b):
  with output:
    output.clear_output()
    prompt = f"""
    Escreva um texto com SEO otimizado sobre o tema '{topic.value}'.
    Retorne em sua resposta apenas o texto final e não inclua ela dentro de aspas.
    - Onde será publicado: {platform.value}.
    - Tom: {tone.value}.
    - Público-alvo: {audience.value}.
    - Comprimento: {length.value}.
    - {"Inclua uma chamada para ação clara." if cta.value else "Não inclua chamada para ação"}
    - {"Retorne ao final do texto hashtags relevantes." if hashtags.value else "Não inclua hashtags."}
    {"- Palavras-chave que devem estar presentes nesse texto (para SEO): " + keywords.value if keywords.value else ""}
    """
    try:
      res = llm_generate(llm, prompt)
      show_res(res)
    except Exception as e:
      print(f"Erro: {e}")

"""Para executar a função de geração de conteúdo ao clicar no botão, precisamos primeiro desvincular qualquer callback anterior para evitar execuções duplicadas, especialmente em ambientes como o Colab onde o parâmetro remove=True pode apresentar instabilidades. A solução mais simples e robusta é redeclarar o output, o generate_button (associando o on_click à nova função) e a variável form chamando create_form(), garantindo uma configuração limpa a cada execução da célula."""

output = widgets.Output()
generate_button = widgets.Button(description = "Gerar conteúdo")
generate_button.on_click(generate_result)
form = create_form()

display(form)

"""**Pronto!** Finalizamos nossa aplicação.

Aqui você pode reunir todo o código desenvolvido em um único bloco, já pronto para ser executado e utilizado por quem for operar o sistema.

Para deixar o código recolhido por padrão, utilize o comando `#@title` no início do bloco — por exemplo: `#@title Rodar Aplicação`
Isso além de criar uma seção com título e facilitar a organização vai permitir que o código fique escondido. Para exibir ou ocultar o conteúdo, basta dar dois cliques sobre o título ("Rodar Aplicação").

## Escalando para outras áreas e adicionando mais campos

Para aumentar a flexibilidade na definição das opções dos campos Dropdown, em vez de fixá-las no código, utilizaremos os formulários do Colab com a anotação `@param {type:"string"}`. Isso permite que o usuário insira uma lista de valores separados por vírgula diretamente em um campo ao lado da célula de código, que é então convertida em uma lista Python e usada dinamicamente no parâmetro options do widget.

Dessa forma, o formulário se torna totalmente configurável, permitindo fácil adição ou modificação das opções dos dropdowns, como as do campo "comprimento", sem alterar o código principal.
"""

opt_length = "Curto, Médio, Longo, 1 parágrafo, 1 página" # @param {type:"string"}
print(opt_length)

options_length = [x.strip() for x in opt_length.split(",")]

options_length

length = widgets.Dropdown(
    options = opt_length,
    description="Tamanho",
    layout=widgets.Layout(width=w_dropdown)
)

form = create_form()
output.clear_output()
display(form)

"""---

## Construção de interface com Streamlit

Após validar que nossa aplicação está funcionando corretamente, podemos aprimorar ainda mais a interface.

Embora o uso de ipywidgets pode ser funcional, conseguimos criar uma experiência mais amigável e visual com o **Streamlit** — uma ferramenta focada em interfaces interativas para aplicações em Python. Além disso, o Streamlit facilita o deploy da aplicação, tornando-a mais acessível para equipes de atendimento ou até mesmo clientes finais.

### 1. Instalação do Streamlit

Para começarmos, precisamos instalar o **Streamlit**

Por estarmos rodando no Colab, precisa também instalar o **Localtunnel** para conseguirmos nos conectar à aplicação gerada com o streamlit. Ao executar em seu próprio computador ela não é necessária, pois após rodar o comando de launch do streamlit ("streamlit run ...") será aberto automaticamente uma aba em seu navegador com a aplicação.

Além disso, vamos instalar a biblioteca **dotenv**, usada para simplificar a gestão de variáveis de ambiente ao armazená-las em um arquivo .env.
"""

!pip install -q streamlit
!npm install -q localtunnel
!pip install -q python-dotenv

"""### 2. Criação do arquivo da aplicação

Crie um arquivo chamado `app.py` (ou outro nome que preferir) com o conteúdo do seu código adaptado para Streamlit.

Antes de colocarmos o código nesse arquivo, vamos criar o arquivo .env, para carregar as variáveis de ambiente. Aqui basta colocarmos a key do Groq, a mesma que usamos anteriormente. Deixe nesse formato: `GROQ_API_KEY=CHAVE_AQUI`

* Obs: o comando `%%writefile` no início desse bloco de código permite que a célula do notebook seja salva como um arquivo externo, com o nome especificado. Ou seja, estamos criando um arquivo com esse nome e o conteúdo será tudo a partir da segunda linha do bloco abaixo

"""

# Commented out IPython magic to ensure Python compatibility.
# %%writefile .env
# GROQ_API_KEY=

"""Foi necessário fazer algumas adaptações ao código, pois até então usamos ipywidgets mas agora no Streamlit usaremos funções da própria biblioteca para criar os campos."""

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# from langchain_groq import ChatGroq
# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
# load_dotenv()
# 
# ## conexão com a LLM
# id_model = "llama3-70b-8192"
# llm = ChatGroq(
#     model=id_model,
#     temperature=0.7,
#     max_tokens=None,
#     timeout=None,
#     max_retries=2,
# )
# 
# ## função de geração
# def llm_generate(llm, prompt):
#   template = ChatPromptTemplate.from_messages([
#       ("system", "Você é um especialista em marketing digital com foco em SEO e escrita persuasiva."),
#       ("human", "{prompt}"),
#   ])
# 
#   chain = template | llm | StrOutputParser()
# 
#   res = chain.invoke({"prompt": prompt})
#   return res
# 
# st.set_page_config(page_title = "Gerador de conteúdo 🤖", page_icon="🤖")
# st.title("Gerador de conteúdo")
# 
# # Campos do formulário
# topic = st.text_input("Tema:", placeholder="Ex: saúde mental, alimentação saudável, prevenção, etc.")
# platform = st.selectbox("Plataforma:", ['Instagram', 'Facebook', 'LinkedIn', 'Blog', 'E-mail'])
# tone = st.selectbox("Tom:", ['Normal', 'Informativo', 'Inspirador', 'Urgente', 'Informal'])
# length = st.selectbox("Tamanho:", ['Curto', 'Médio', 'Longo'])
# audience = st.selectbox("Público-alvo:", ['Geral', 'Jovens adultos', 'Famílias', 'Idosos', 'Adolescentes'])
# cta = st.checkbox("Incluir CTA")
# hashtags = st.checkbox("Retornar Hashtags")
# keywords = st.text_area("Palavras-chave (SEO):", placeholder="Ex: bem-estar, medicina preventiva...")
# 
# if st.button("Gerar conteúdo"):
#   prompt = f"""
#   Escreva um texto com SEO otimizado sobre o tema '{topic}'.
#   Retorne em sua resposta apenas o texto final e não inclua ela dentro de aspas.
#   - Onde será publicado: {platform}.
#   - Tom: {tone}.
#   - Público-alvo: {audience}.
#   - Comprimento: {length}.
#   - {"Inclua uma chamada para ação clara." if cta else "Não inclua chamada para ação"}
#   - {"Retorne ao final do texto hashtags relevantes." if hashtags else "Não inclua hashtags."}
#   {"- Palavras-chave que devem estar presentes nesse texto (para SEO): " + keywords if keywords else ""}
#   """
#   try:
#       res = llm_generate(llm, prompt)
#       st.markdown(res)
#   except Exception as e:
#       st.error(f"Erro: {e}")

"""### 3. Execução do Streamlit

Tendo nosso script pronto, basta executar o comando abaixo para rodar a nossa aplicação pelo streamlit.
Isso fará com que a aplicação do Streamlit seja executada em segundo plano.
"""

!streamlit run app.py &>/content/logs.txt &

"""> **Como abrir a interface**

> Importante: caso esse código não funcione corretamente use o ngrok, cujo código você encontra mais abaixo (para mais detalhes, veja a aula 'Aviso sobre uso no Colab')

* Antes de conectar com o localtunnel, você precisa obter o IP externo (usando esse comando `!wget -q -O - ipv4.icanhazip.com`). Copie esse número, que vai aparecer na saída do bloco abaixo (após rodar)
* Então, entre no link que aparece na saída do bloco abaixo e informe esse IP no campo Tunnel Password. Logo em seguida, clique no botão e aguarde a interface ser inicializada


Esse comando usa npx localtunnel para "expor" o aplicativo Streamlit em execução local para a internet. O aplicativo é hospedado na porta 8501, e o localtunnel fornece uma URL pública por meio da qual o aplicativo pode ser acessado.

**Caso não abra, reinicie a sessão e espere alguns segundos antes de clicar no link. Ou, reinicie o ambiente de execução e rode os comandos novamente.**
"""

!wget -q -O - ipv4.icanhazip.com
!npx localtunnel --port 8501

"""> **Importante:** Caso o comando acima com localtunnel não funcione, use o código abaixo (Para mais detalhes, consulte a aula "Aviso sobre uso no Colab" da seção 2)

### Alternativa com ngrok
"""

!pip install pyngrok

from pyngrok import ngrok

!ngrok config add-authtoken SEU_TOKEN_AQUI
!streamlit run app.py --server.port 8501 &>/content/logs.txt &

public_url = ngrok.connect(8501)
public_url

"""---

## Rodando a LLM localmente

Se for um modelo open source nós podemos fazer o download e rodar localmente em um provedor cloud (como nesse caso o colab) ou em nosso próprio computador.

### -> Para executar no Colab

**Importante:** Antes de realizar os próximos passos, mude o ambiente de execução no Colab para usar GPU, que será necessário já que todo o processamento será feito direto localmente no ambiente de execução do Colab. Para isso, selecione 'Ambiente de execução > Alterar o tipo de ambiente de execução' e na opção 'Acelerador de hardware' selecione 'GPU'.

Além das bibliotecas do langchain que instalamos, vamos precisar também da biblioteca `langchain-huggingface`, `transformers` e `bitsandbytes`
"""

!pip install -q langchain langchain-community langchain-huggingface transformers

!pip install bitsandbytes-cuda110 bitsandbytes

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch

"""**Quantização**

A execução de LLMs pode ser desafiadora devido aos recursos limitados, especialmente na versão gratuita do Google Colab. Para contornar essa limitação, além de escolher modelos com menos parâmetros podemos usar técnicas de quantização, como o `BitsAndBytesConfig` da biblioteca `transformers`, que permitem carregar e executar modelos massivos de forma eficiente sem comprometer significativamente o desempenho.
* Essas técnicas reduzem os custos de memória e computação ao representar pesos e ativações com tipos de dados de menor precisão, como inteiros de 8 bits (int8) ou até 4 bits, tornando viável o uso de modelos grandes mesmo em hardware limitado.
* Alternativas ao BitsAndBytesConfig: AutoGPTQ, AutoAWQ, etc.
* Para quem prefere evitar configurações complexas de otimização e manter a máxima qualidade, considere o uso via API.
* Mais detalhes sobre quantização: https://huggingface.co/blog/4bit-transformers-bitsandbytes
"""

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

"""**Download do modelo**

Agora faremos o download e a configuração de um modelo do HuggingFace usando o método `AutoModelForCausalLM.from_pretrained`. Este processo pode levar alguns minutos, pois o modelo tem alguns GB - mas no geral o download no Colab deve ser relativamente rápido.

> Para ver todos os modelos disponíveis no Hugging Face, acesse: https://huggingface.co/models?pipeline_tag=text-generation

Escolhemos o Phi 3 (microsoft/Phi-3-mini-4k-instruct), um modelo menor mas que demonstrou ser muito interessante e com ótimo custo benefício
 - https://huggingface.co/microsoft/Phi-3-mini-4k-instruct


"""

model_id = "microsoft/Phi-3-mini-4k-instruct"

model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=quantization_config)
tokenizer = AutoTokenizer.from_pretrained(model_id)

"""**Criação do Pipeline**

Agora criaremos um pipeline para geração de texto usando nosso modelo e tokenizer carregados anteriormente. A função de pipeline HuggingFace simplifica o processo de execução de várias tarefas de processamento de linguagem natural ao fornecer uma interface de alto nível.

Parâmetros:
* `model`: Modelo de linguagem a ser usado (definido por model_id).

* `tokenizer`: Tokenizador correspondente ao modelo para processar o texto.

* `task`: Tipo de tarefa (ex.: "text-generation" para geração de texto).

* `temperature`: Controla a aleatoriedade (lembre-se de variar o valor, conforme as dicas que passamos).

* `max_new_tokens`: Número máximo de tokens gerados na saída.

* `do_sample`: Habilita/desabilita amostragem estocástica (geração não determinística).

* `repetition_penalty`: Penaliza repetições (valores >1 reduzem repetições).

* `return_full_text`: Se False, retorna apenas o texto gerado (ignorando o prompt).
"""

pipe = pipeline(
    model = model,
    tokenizer = tokenizer,
    task = "text-generation",
    temperature = 0.1,
    max_new_tokens = 500,
    do_sample = True,
    repetition_penalty = 1.1,
    return_full_text = False
)

"""Para carregar a LLM"""

llm = HuggingFacePipeline(pipeline = pipe)

input = "Gere um texto sobre alimentação saudável, em 1 parágrafo"

"""**Geração do resultado**"""

output = llm.invoke(input)
print(output)

"""**Adequando o prompt com Templates (quando necessário)**

Talvez o resultado acima ficou um pouco estranho, ou ele inventou algum texto antes de fornecer o resultado.
Para evitar alucinações ou geração infinita de texto, use o template oficial do modelo Phi 3, que inclui tokens especiais como:

* <|system|>, <|user|>, <|assistant|>: definem os papéis da mensagem.

* <|end|>: marca o fim do texto (equivalente ao token EOS).

Na dúvida, acesse a página do modelo no Hugging Face, se houver um template recomendável para o modelo ele estará na descrição.

Para outras implementações pode não ser necessário fornecer o prompt, como por exemplo a implementação via API que usamos anteriormente.


"""

prompt = """
<|system|>
Você é um especialista em marketing digital com foco em SEO e escrita persuasiva.<|end|>
<|user|>
"{}"<|end|>
<|assistant|>
""".format(input)

prompt

output = llm.invoke(prompt)
output

"""* Considerações finais: A vantagem de usarmos o LangChain é que toda a sintaxe e lógca que criamos para esse projeto (por exemplo chains) é reaproveitada, o que muda é a parte de carregar a llm, o resto pode permanecer igual. Então, bastaria substituir o método de carregamento da LLM do LangChain (por exemplo, ao invés de ChatGroq usar o HuggingFacePipeline ou o ChatHuggingFace) e com isso você teria a aplicação funcionando o mesmo modo, porém rodando tudo localmente (seja cloud ou no computador local)

### -> Para rodar em seu computador

Para usar a LLM localmente via API: use o mesmo código desse Colab, fazendo a instalação das bibliotecas instaladas (no comando de instalação, ao início desse Colab).

Para usar a LLM baixando o modelo localmente:
Para maior compatibilidade de execução de LLMs em máquina local nós sugerimos a biblioteca [Ollama](https://ollama.com), que possui integração direta com o LangChain.

* Rode o arquivo llm_local.py e instale todas as bibliotecas necessárias conforme consta nos comentários ao início do .py

Recomendamos usar pelo Colab pelo menos no início e para não atrapalhar o fluxo de aprendizado deste curso. Ao executar localmente podem ocorrer outros problemas de instalação ou incompatibilidade, e de início pode perder tempo desnecessário. O método que mostraremos tenta evitar esses tipos de erro mas ainda assim é impossível garantir 100%, portanto sugerimos primeiro testar pelo Colab e depois (se quiser) executar em sua máquina local.
"""
