from .chatkimi import chat_kimi

PROMPT_PATH = './prompts/prompt.txt'

with open(PROMPT_PATH, 'r', encoding='utf-8') as f:
    prompt = f.read()

def generate_practice(md_path, scq_num, mcq_num, tof_num, sa_num):
    """
    :param md_path: path of markdown
    :param scq_num: number of single choice questions
    :param mcq_num: number of multiple choice questions
    :param tof_num: number of true or false questions
    :param tof_num: number of short answer questions
    """
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    user_input = f'需要{scq_num}道单选题，{mcq_num}道多选题，{tof_num}道判断题，{sa_num}道简答题，makedown的内容是：{md_content}'
    questions = chat_kimi(user_input=user_input, prompt=prompt)
    return questions


if __name__ == '__main__':
    md_path = './test.md'
    scq_num = 2
    mcq_num = 1
    tof_num = 1
    sa_num = 1
    questions = generate_practice(md_path, scq_num, mcq_num, tof_num, sa_num)
    print(questions)