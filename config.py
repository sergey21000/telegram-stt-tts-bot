MODEL_KWARGS = dict(
    repo_id='bartowski/gemma-2-2b-it-GGUF',
    filename='*8_0.gguf',
    local_dir='llm_model',
    n_gpu_layers=-1,
    verbose=False,
)

GENERATION_KWARGS = dict(
    temperature=0.2,
    top_p=0.95,
    top_k=40,
    repeat_penalty=1.0,
)

SYSTEM_PROMPT = ''
SAMPLE_RATE = 16000

speaker_names = ['Женский 1', 'Женский 2', 'Женский 3', 'Мужской 1', 'Мужской 2']
ALL_SPEAKERS = dict(enumerate(speaker_names))
CURR_SPEAKER = {'speaker_index': 2}

speakers_info = '\n'.join([f'**{key}**: _{value}_' for key, value in ALL_SPEAKERS.items()])
WELCOME_MESSAGE = rf'''
__Привет, это бот помощник, варианты использования:__
1\) Отправь голосовое или текст чтобы получить ответ текстом и голосом
2\) Для изменения голоса отправь число от 0 до 4:
{speakers_info}
'''
