import operator
import argparse
import json
import spacy


def getModalAnswer(answers):
    candidates = {}
    for i in range(10):
        candidates[answers[i]['answer']] = 1

    for i in range(10):
        candidates[answers[i]['answer']] += 1

    return max(candidates.items(), key=operator.itemgetter(1))[0]


def getAllAnswer(answers):
    answer_list = []
    for i in range(10):
        answer_list.append(answers[i]['answer'])

    return ';'.join(answer_list)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-split', type=str, default='train',
                        help='Specify which part of the dataset you want to dump to text. Your options are: train, val, test, test-dev')
    parser.add_argument('-answers', type=str, default='modal',
                        help='Specify if you want to dump just the most frequent answer for each questions (modal), or all the answers (all)')
    args = parser.parse_args()

    nlp = spacy.load('en_core_web_md')  # used for conting number of tokens

    if args.split == 'train':
        annFile = '../checkpoints/mscoco_train2014_annotations.json'
        quesFile = '../checkpoints/OpenEnded_mscoco_train2014_questions.json'
        questions_file = open('../checkpoints/preprocessed/questions_train2014.txt', 'wb')
        questions_id_file = open('../checkpoints/preprocessed/questions_id_train2014.txt', 'wb')
        questions_lengths_file = open('../checkpoints/preprocessed/questions_lengths_train2014.txt', 'wb')
        if args.answers == 'modal':
            answers_file = open('../checkpoints/preprocessed/answers_train2014_modal.txt', 'wb')
        elif args.answers == 'all':
            answers_file = open('../checkpoints/preprocessed/answers_train2014_all.txt', 'wb')
        coco_image_id = open('../checkpoints/preprocessed/images_train2014.txt', 'wb')
        data_split = 'training checkpoints'
    elif args.split == 'val':
        annFile = '../checkpoints/mscoco_val2014_annotations.json'
        quesFile = '../checkpoints/OpenEnded_mscoco_val2014_questions.json'
        questions_file = open('../checkpoints/preprocessed/questions_val2014.txt', 'wb')
        questions_id_file = open('../checkpoints/preprocessed/questions_id_val2014.txt', 'wb')
        questions_lengths_file = open('../checkpoints/preprocessed/questions_lengths_val2014.txt', 'wb')
        if args.answers == 'modal':
            answers_file = open('../checkpoints/preprocessed/answers_val2014_modal.txt', 'wb')
        elif args.answers == 'all':
            answers_file = open('../checkpoints/preprocessed/answers_val2014_all.txt', 'wb')
        coco_image_id = open('../checkpoints/preprocessed/images_val2014_all.txt', 'wb')
        data_split = 'validation checkpoints'
    elif args.split == 'test-dev':
        quesFile = '../checkpoints/OpenEnded_mscoco_test-dev2015_questions.json'
        questions_file = open('../checkpoints/preprocessed/questions_test-dev2015.txt', 'wb')
        questions_id_file = open('../checkpoints/preprocessed/questions_id_test-dev2015.txt', 'wb')
        questions_lengths_file = open('../checkpoints/preprocessed/questions_lengths_test-dev2015.txt', 'wb')
        coco_image_id = open('../checkpoints/preprocessed/images_test-dev2015.txt', 'wb')
        data_split = 'test-dev checkpoints'
    elif args.split == 'test':
        quesFile = '../checkpoints/OpenEnded_mscoco_test2015_questions.json'
        questions_file = open('../checkpoints/preprocessed/questions_test2015.txt', 'wb')
        questions_id_file = open('../checkpoints/preprocessed/questions_id_test2015.txt', 'wb')
        questions_lengths_file = open('../checkpoints/preprocessed/questions_lengths_test2015.txt', 'wb')
        coco_image_id = open('../checkpoints/preprocessed/images_test2015.txt', 'wb')
        data_split = 'test checkpoints'
    else:
        raise RuntimeError('Incorrect split. Your choices are:\ntrain\nval\ntest-dev\ntest')

    # initialize VQA api for QA annotations
    # vqa=VQA(annFile, quesFile)
    questions = json.load(open(quesFile, 'r'))
    ques = questions['questions']
    if args.split == 'train' or args.split == 'val':
        qa = json.load(open(annFile, 'r'))
        qa = qa['annotations']

    print('Dumping questions, answers, questionIDs, imageIDs, and questions lengths to text files...')
    for i, q in zip(range(len(ques)), ques):
        questions_file.write((q['question'] + '\n').encode('utf8'))
        questions_lengths_file.write((str(len(nlp(q['question']))) + '\n').encode('utf8'))
        questions_id_file.write((str(q['question_id']) + '\n').encode('utf8'))
        coco_image_id.write((str(q['image_id']) + '\n').encode('utf8'))
        if args.split == 'train' or args.split == 'val':
            if args.answers == 'modal':
                answers_file.write(getModalAnswer(qa[i]['answers']).encode('utf8'))
            elif args.answers == 'all':
                answers_file.write(getAllAnswer(qa[i]['answers']).encode('utf8'))
            answers_file.write('\n'.encode('utf8'))

    print('completed dumping', data_split)


if __name__ == "__main__":
    main()
