from tqdm import tqdm
import json
import sys


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: {} <udpipe_result_output_file> <output_file>".format(sys.argv[0]))
        # UDPIPE RUN EXAMPLE:
        # ./udpipe/bin-osx/udpipe --input generic_tokenizer \ 
        # --tag russian-syntagrus-ud-2.5-191206.udpipe corpus_file.txt --output epe --outfile output.txt
        sys.exit(1)

    data = []

    with open(sys.argv[1], 'r') as f:
        for l in tqdm(f.readlines()):
            sent = []
            j = json.loads(l)
            prev_propn = False
            case = '-'
            num = '-'
            for n in j['nodes']:
                if n['form'] == '.' and sent:
                    data.append(' '.join(sent))
                    sent = []
                    prev_propn = False
                    case = '-'
                    num = '-'
                    continue
                    
                if n['properties']['upos'] not in ['NUM', 'NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV']:
                    continue
                    
                add = True
                if n['properties']['upos'] == 'PROPN':
                    cur_case = n['properties'].get('Case', '')
                    cur_num = n['properties'].get('Number', '')
                    if prev_propn and case == cur_case and num == cur_num:
                        sent[-1] += '::' + n['properties']['lemma'].lower()
                        add = False
                    case = cur_case
                    num = cur_num
                    prev_propn = True
                else:
                    prev_propn = False
                    case = '-'
                    num = '-'
                if add:
                    sent.append(n['properties']['lemma'].lower())

    with open(sys.argv[2], 'w') as f:
        for l in data:
            f.write('{}\n'.format(l))
