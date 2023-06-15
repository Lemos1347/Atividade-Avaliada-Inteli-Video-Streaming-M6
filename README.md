# Atividade-Avaliada-Inteli-Video-Streaming-M6

## Demonstração do funcionamento

https://github.com/Lemos1347/Atividade-Avaliada-Inteli-Video-Streaming-M6/assets/99190347/48c3a53b-5147-4bdc-9225-cd016995be6d

## Objetivo

Este repositório contém o código para um servidor [back-end](/api/)(localizado na pasta `/api`) que permite aos usuários criar e fazer upload de vídeos. O servidor é construído com o Sanic, um framework web Python 3.7+ assíncrono, e utiliza o OpenCV para processar imagens e vídeos, e o Supabase para armazenamento os vídeos. Além disso, nesse repositório ainda é possível encontrar um [script em python](/video_capture/)(localizado na pasta `/video_capture`) que realizará a captura de imagens da webcam do usuário e enviará para o servidor, o qual ao final será o vídeo que será armaenado no Supabase.

## Explicação da construção

### Captura do vídeo

* Para a captura do vídeo foi criado um script em Python que captura o vídeo de uma webcam do seu computador com a biblioteca OpenCV.
* É realizado um "while loop" para que a cada frame capturado é utilizado o método "imencode" para transformar o frame em uma imagem em um formato específico, no caso, transformamos em "jpg".
* Após a "criação da imagem jpg", é utilizado o método "tobytes( )" do próprio resultado da tranformação anterior efeturada. Esse método é responsável por converter a imagem codificada em uma sequência de bytes que pode ser enviada por uma conexão de rede.
* Assim que a imagem estiver pronta, ela é então enviada no body de uma solicitação do tipo POST.
* Nesse mesmo script é seguido toda sequência exigida pelo backend para que o "upload" do vídeo aconteça corretamente.

### Processamento e armazenamento dos frames

* Para evitar conflitos de arquivos e mistura de diferentes vídeos, foi criada a seguinte lógica (foram criadas uma rota para cada proceso descrito):1º - É criado uma pasta com uma nomeclatura única com base nas pasta já existentes. Essa pasta será responsável por armazenar todos os frames considerados do mesmo vídeo.
  2º - Todos os frames recebidos são armazenados na pasta mais recente.
  3º - Todos os frames são coletados e agrupados em um vídeo. Após um sucesso na criação do vídeo, todos os frames são apagados, o vídeo é salvo na pasta mais recente, o vídeo salvo é enviado para um bucket no Supabase e após o sucesso dessa operação, essa pasta mais recente é apagada.
* Quando o servidor recebe uma solicitação POST para o endpoint "/video_upload", ele primeiro transforma o array de bytes JPEG enviado na solicitação de volta em uma imagem.
* O servidor então armazena essa imagem na pasta de vídeo mais recente, usando o timestamp atual como o nome do arquivo para evitar conflitos de nomes.
* Esse processo é repetido para cada frame enviado pelo script de captura de vídeo.

### Criação e armazenamento do vídeo

1. Quando o servidor recebe uma solicitação GET para o endpoint "/finish_video", ele primeiro pega o nome da pasta de vídeo mais recente.
2. Em seguida, ele cria um objeto de vídeo usando a biblioteca OpenCV, especificando o codec, o fps, a resolução do vídeo e o caminho onde o vídeo será salvo.
3. O servidor então lê cada frame da pasta de vídeo mais recente e escreve no arquivo de vídeo.
4. Depois que todos os frames foram escritos no vídeo, o objeto de vídeo é fechado, finalizando a criação do arquivo de vídeo.
5. Todos os frames individuais que foram armazenados anteriormente são então excluídos, já que não são mais necessários.
6. O servidor então cria um cliente Supabase e faz o upload do vídeo para o Supabase.
7. Se o upload for bem-sucedido, o servidor retorna uma resposta JSON com o status "sucesso" e a URL do vídeo no Supabase. Se o upload falhar, ele retorna uma resposta com o status "erro".

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

Para executar a captura do vídeo com a webcam, basta rodar o seguinte comando na raíz do projeto:

```shell
python video_capture/main.py
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
