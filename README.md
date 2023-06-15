# Atividade-Avaliada-Inteli-Video-Streaming-M6

## Demonstração do funcionamento

https://github.com/Lemos1347/Atividade-Avaliada-Inteli-Video-Streaming-M6/assets/99190347/48c3a53b-5147-4bdc-9225-cd016995be6d

## Objetivo

Este repositório contém o código para um servidor [back-end](/api/)(localizado na pasta `/api`) que permite aos usuários criar e fazer upload de vídeos. O servidor é construído com o Sanic, um framework web Python 3.7+ assíncrono, e utiliza o OpenCV para processar imagens e vídeos, e o Supabase para armazenamento os vídeos. Além disso, nesse repositório ainda é possível encontrar um [script em python](/video_capture/)(localizado na pasta `/video_capture`) que realizará a captura de imagens da webcam do usuário e enviará para o servidor, o qual ao final será o vídeo que será armaenado no Supabase.

## Dependências

- Python 3.7+
- Sanic
- OpenCV
- Supabase
- python-dotenv

Você pode instalar todas as dependências do servidor executando o comando abaixo no terminal na root do projeto:

```shell
pip install -r api/requirements.txt
```

Caso você queira instalar as dependências do script python para criar o vídeo, execute o comando abaixo no terminal na root do projeto:

```shell
pip install -r video_capture/requirements.txt
```

## Configuração

O servidor utiliza variáveis de ambiente para armazenar as credenciais do Supabase e o nome do bucket. Para configurar o servidor, siga as etapas abaixo:

1. Crie um arquivo `.env` em `/api`.
2. Adicione as seguintes variáveis de ambiente ao arquivo `.env` com as suas credencias do Supabase (lembre-se de criar e configurar o bucket corretamente em seu Supabase):

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
BUCKET_NAME=your_bucket_name
```

Substitua `your_supabase_url`, `your_supabase_key` e `your_bucket_name` pelos valores apropriados.

## Execução

Para executar o servidor, navegue até a pasta raiz do projeto e execute o seguinte comando:

```shell
python api/app.py
```

## Endpoints

O servidor oferece três endpoints:

1. `GET video/create_video`: Cria uma nova pasta para armazenar as imagens capturadas pelo usuário, pasta a qual é temporária.
2. `POST video/video_upload`: Recebe uma imagem do usuário, transforma-a em um array de bytes e a armazena na pasta do vídeo mais recente.
3. `GET video/finish_video`: Cria um vídeo a partir das imagens armazenadas, faz o upload do vídeo para o Supabase, retorna a URL do vídeo e apaga a pasta e os frames armazenados.

## Observações

- As imagens devem ser enviadas como arquivos no corpo da solicitação `POST video/video_upload`.
- As imagens são salvas com um timestamp para evitar conflitos de nomes.
- O vídeo é criado com uma resolução de 1280x720 e uma taxa de quadros de 27 FPS.
- Todos os quadros de imagem são removidos após a criação do vídeo.
- A pasta de quadros de imagem é removida após o upload do vídeo para o Supabase.
- O vídeo é nomeado com um timestamp para evitar conflitos de nomes no Supabase.
- É necessário seguir as chamadas de endpoint na ordem correta para que o servidor funcione corretamente (consulte [script de demosntração](./video_capture/main.py)).
