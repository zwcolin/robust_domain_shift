import os, sys

# example: python train_run.py keyword temp_keyword _
if __name__ == '__main__':
    mode = sys.argv[1]
    control_mode = sys.argv[2]
    eval_split = sys.argv[3]
    model_file = None
    old_model = None
    MODEL_FILE = sys.argv[4]
    submit_job = (sys.argv[5] == 'yes')

    if mode == 'webnlg':
        Token_FILE = MODEL_FILE
        # gen_dir = 'webNLG_results'
        gen_dir = 'webNLG_results2'

        sub_model_name = os.path.basename(MODEL_FILE)

        if 'o=' in sub_model_name:
            o_idx = sub_model_name.index('o=')
            num_idx = sub_model_name[o_idx+2]
            print(num_idx)

        if 'prefixtune' in MODEL_FILE:
            tuning_mode = 'prefixtune'
            app = '--optim_prefix {} --preseqlen {} '.format('yes', 20)
            app += "--prefix_mode activation "
            if "_inf" in MODEL_FILE or 'infix' in MODEL_FILE:
                app += " --format_mode infix "
            elif "_cat" in MODEL_FILE:
                app += " --format_mode cat "
            elif "_pee" in MODEL_FILE:
                app += " --format_mode peek "

            MODEL_FILE2 = MODEL_FILE

            if 'large' in sub_model_name:
                MODEL_FILE = 'gpt2-large'
            else:
                MODEL_FILE = 'gpt2-medium'


    COMMANDLINE = "python run_generation.py \
        --model_type=gpt2 \
        --length 100 \
        --model_name_or_path={} \
        --num_return_sequences 5 \
        --stop_token [EOS] \
        --tokenizer_name={} \
        --task_mode={} \
        --control_mode={} --tuning_mode {} --gen_dir {} --eval_dataset {} \
    ".format(MODEL_FILE, Token_FILE, mode, control_mode, tuning_mode, gen_dir, eval_split)

    COMMANDLINE += app

    if tuning_mode == 'prefixtune':
        COMMANDLINE += ' --prefixModel_name_or_path {}'.format(MODEL_FILE2)
        name = os.path.basename(MODEL_FILE2)
    else:
        name = os.path.basename(MODEL_FILE)


    if MODEL_FILE == 'gpt2-large':
        COMMANDLINE += ' --cache_dir cache/gpt2-large-s3 '

    if MODEL_FILE == 'gpt2-medium':
        COMMANDLINE += ' --cache_dir cache/gpt2-medium-s3 '


    print(COMMANDLINE)

    if not submit_job:
        os.system(COMMANDLINE)
