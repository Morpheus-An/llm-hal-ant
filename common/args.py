# -*- coding: utf-8 -*-
# @Date    : 2023-10-26 19:51:58
# @Author  : Shangyu.Xing (starreeze@foxmail.com)

import argparse

parser = argparse.ArgumentParser()
# data
## path
parser.add_argument("--vqa_prompt_path", type=str, default="dataset/vqa_prompt.txt")
parser.add_argument("--vqa_data_path", type=str, default="dataset/rlhf.json")
parser.add_argument("--caption_prompt_path", type=str, default="dataset/caption_prompt_finetune.txt")
parser.add_argument("--caption_data_path", type=str, default="dataset/captions.txt")
parser.add_argument("--annotation_path", type=str, default="dataset/captions_train2014.json")
parser.add_argument("--object_data_path", type=str, default="dataset/objects.txt")
parser.add_argument("--image_dir_path", type=str, default="dataset/images")
parser.add_argument("--hal_result_path", type=str, default="dataset/hal.npy")
parser.add_argument("--image_prefix", type=str, default="COCO_train2014_")
parser.add_argument("--norm_result_path", type=str, default="dataset/norm.npy")
parser.add_argument("--pos_neg_data_path", type=str, default="dataset/pos_neg.json")
parser.add_argument("--sentence_data_path", type=str, default="dataset/sentences.json")
## format
parser.add_argument("--column_splitter", type=str, default=" ### ")
parser.add_argument("--object_splitter", type=str, default=", ")
parser.add_argument("--subsentence_splitter_set", type=str, default=",.;!?:")
parser.add_argument("--clip_prompt", type=str, default="A photo containing ")

# insight
## model
### llm for object extraction
parser.add_argument("--llama_path", type=str, default="/home/nfs02/model/llama2/hf/Llama-2-7b-chat-hf")
parser.add_argument("--llama_8bit", action="store_true")
llama_instruction_placeholder = "$$$"
llama_sys_prompt = (
    "<<SYS>>\nYou are a helpful, respectful and honest assistant. "
    "Strictly follow the instruction and always answer as helpfully as possible.\n"
    f"<</SYS>>\n\n</s> [INST] {llama_instruction_placeholder} [/INST] "
)
parser.add_argument("--llama_instruction_placeholder", type=str, default=llama_instruction_placeholder)
parser.add_argument("--llama_sys_prompt", type=str, default=llama_sys_prompt)

parser.add_argument("--prompt_input_label", type=str, default="(Input)")
parser.add_argument("--prompt_output_label", type=str, default="(Output)")
### methods for insight
parser.add_argument("--patch_size", type=int, default=48)
parser.add_argument("--window_size", type=int, default=4)  # number of patches
parser.add_argument("--average_top_k", type=int, default=4)
## others
parser.add_argument("--least_data_size", type=int, default=50)
parser.add_argument("--sample_policy", type=str, default="random")

# finetune
parser.add_argument("--unlearn_target", type=str, default="subsentence", help="object or subsentence")
parser.add_argument(
    "--hal_clip_thres", type=float, default=23, help="clip score < thres will be regraded as hal"
)  # 30k
parser.add_argument(
    "--norm_clip_thres", type=float, default=32, help="clip score > thres will be regraded as norm"
)  # 21k
parser.add_argument(
    "--sentence_clip_thres",
    type=float,
    default=27.5,
    help="sentences with mean clip score > thres will be used as whole-sentence positive sample",
)  # 27k
parser.add_argument("--gold_clip_score", type=float, default=40, help="clip score of the gold caption")

parser.add_argument("--neg_w_start", type=float, default=0.2)
parser.add_argument("--neg_w_end", type=float, default=0)
parser.add_argument("--neg_w_start_step_pos", type=float, default=0.2)
parser.add_argument("--neg_w_sched_type", type=str, default="linear")
parser.add_argument("--pos_w_start", type=float, default=1)
parser.add_argument("--pos_w_end", type=float, default=0.5)
parser.add_argument("--pos_w_start_step_pos", type=float, default=0)
parser.add_argument("--pos_w_sched_type", type=str, default="linear")
parser.add_argument("--gold_w", type=float, default=0.6)
parser.add_argument("--sent_w", type=float, default=0.6)

parser.add_argument("--max_new_tokens", type=int, default=200, help="max number of generated tokens")
parser.add_argument("--infer_dataloader_worker", type=int, default=0)
parser.add_argument("--valid_data_split", type=float, default=0.05)
parser.add_argument("--wandb_user", type=str, default="starreeze")
parser.add_argument("--print_per_n_step", type=int, default=1)
parser.add_argument("--eval_per_epoch", type=int, default=10)

## models
### minigpt
parser.add_argument(
    "--minigpt_infer_cfg", default="configs/minigpt4_infer_fp16.yaml", help="path to configuration file."
)
parser.add_argument(
    "--minigpt_train_cfg", default="configs/minigpt4_train_fp16.yaml", help="path to configuration file."
)
parser.add_argument(
    "--minigpt_infer_prompt",
    type=str,
    default="<Img><ImageHere></Img> Please describe the image in no more than 50 words. Make sure to be brief and concise.",
)
parser.add_argument("--train_dataloader_worker", type=int, default=0)
# as context should not be counted in instruction, we need to remove prompt template from cfg and add it here
parser.add_argument(
    "--minigpt_train_prompt", type=str, default="[INST] <Img><ImageHere></Img> Please describe the image. [/INST]"
)
parser.add_argument(
    "--minigpt_eval_caption_prompt",
    type=str,
    default="[INST] <Img><ImageHere></Img> Please describe the image in great detail. Your response should have at least 50 words. [/INST]",
)
parser.add_argument(
    "--minigpt_eval_pope_prompt",
    type=str,
    default="[INST] <Img><ImageHere></Img> According to the given image, answer yes or no to the question faithfully: {question} [/INST]",
)
parser.add_argument("--minigpt_infer_bs_multiply", type=int, default=2)
parser.add_argument("--minigpt_infer_retry", type=int, default=3)
parser.add_argument(
    "--minigpt_train_bs_pos",
    type=int,
    default=3,
    help="number of positive samples (normal objects predicted by clip) in a batch",
)
parser.add_argument(
    "--minigpt_train_bs_gold",
    type=int,
    default=3,
    help="number of positive samples (gold caption of COCO) in a batch",
)
parser.add_argument(
    "--minigpt_train_bs_sent",
    type=int,
    default=3,
    help="number of positive samples (generated complete sentence) in a batch",
)
parser.add_argument("--minigpt_train_bs_neg", type=int, default=3, help="number of negative samples in a batch")
parser.add_argument("--minigpt_train_lr", type=float, default=1e-5)
parser.add_argument("--minigpt_train_wd", type=float, default=0.05)
parser.add_argument("--minigpt_train_epoch", type=int, default=1)
parser.add_argument("--minigpt_ckpt_load_path", type=str, default="checkpoints/pretrained_minigpt4_llama2_7b.pth")
parser.add_argument("--minigpt_ckpt_save_path", type=str, default="checkpoints/minigpt4_llama2_7b")

# eval
parser.add_argument("--pope_result_path", type=str, default="evaluate/pope/result")
parser.add_argument("--pope_max_new_tokens", type=int, default=20)

# common control
parser.add_argument("--device", type=str, default="cuda:0")
parser.add_argument("--restart", action="store_true")
parser.add_argument("--seed", type=int, default=28509)
parser.add_argument("--start_pos", type=int, default=0)
parser.add_argument("--end_pos", type=int, default=int(1e10))
parser.add_argument("--output_path", type=str, default="output.txt")
parser.add_argument("--proxy", type=str, default="")

args = parser.parse_args()
args.minigpt_infer_bs_pos = args.minigpt_train_bs_pos * args.minigpt_infer_bs_multiply
args.minigpt_infer_bs_sent = args.minigpt_train_bs_sent * args.minigpt_infer_bs_multiply
args.minigpt_infer_bs_neg = args.minigpt_train_bs_neg * args.minigpt_infer_bs_multiply
args.minigpt_infer_bs_gold = args.minigpt_train_bs_gold * args.minigpt_infer_bs_multiply
args.minigpt_infer_bs_total = (
    args.minigpt_infer_bs_pos + args.minigpt_infer_bs_sent + args.minigpt_infer_bs_neg + args.minigpt_infer_bs_gold
)
print(args)


# model provided parser
def minigpt4_finetune_parser():
    parser = argparse.ArgumentParser(description="finetune minigpt4")
    parser.add_argument("--cfg-path", default=args.minigpt_infer_cfg, help="path to configuration file.")
    parser.add_argument("--name", type=str, default="A2", help="evaluation name")
    parser.add_argument("--ckpt", type=str, help="path to configuration file.")
    parser.add_argument("--eval_opt", type=str, default="all", help="path to configuration file.")
    parser.add_argument(
        "--max_new_tokens", type=int, default=args.max_new_tokens, help="max number of generated tokens"
    )
    parser.add_argument("--batch_size", type=int, default=1)
    parser.add_argument("--lora_r", type=int, default=64, help="lora rank of the model")
    parser.add_argument("--lora_alpha", type=int, default=16, help="lora alpha")
    parser.add_argument(
        "--options",
        nargs="+",
        help="override some settings in the used config, the key-value pair "
        "in xxx=yyy format will be merged into config file (deprecate), "
        "change to --cfg-options instead.",
    )
    return parser
